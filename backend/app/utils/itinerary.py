from __future__ import annotations
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from app.services.gaode_mcp import AmapClient
from datetime import datetime, timedelta
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Item:
    time_slot: str
    poi: Dict[str, Any]
    move: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None

SLOTS = ["morning", "noon", "afternoon"]

# 完善兴趣关键词映射，增加更多通用关键词
INTEREST_KEYWORDS = {
    "history": ["博物馆", "古迹", "历史文化", "城墙", "故宫", "天坛", "长城", "历史", "文化", "遗址", "古建筑"],
    "art": ["美术馆", "艺术中心", "展览馆", "艺术", "画廊", "创意园"],
    "nature": ["公园", "山", "湖", "湿地", "自然", "风景区", "植物园", "动物园"],
    "food": ["小吃", "美食街", "老字号", "餐馆", "美食", "特色菜", "小吃街", "美食广场"],
    "shopping": ["商场", "步行街", "购物中心", "购物", "商业街", "市场", "购物广场"],
    "entertainment": ["游乐园", "电影院", "剧院", "娱乐", "KTV", "游戏厅"],
    "religion": ["寺庙", "教堂", "清真寺", "宗教", "佛寺", "道观"],
    "education": ["大学", "图书馆", "科技馆", "教育", "学校", "研究院"],
}

# 通用关键词池，确保在任何城市都能找到景点
UNIVERSAL_KEYWORDS = [
    "公园", "博物馆", "景点", "旅游", "景区", "广场", "步行街", 
    "美食", "购物", "娱乐", "文化", "历史", "自然", "地标"
]

def build_itinerary(client: AmapClient, city: str, days: int, interests: Optional[List[str]], starting_point: Optional[str], start_date: str) -> Dict[str, Any]:
    logger.info(f"开始为{city}规划{days}天行程，兴趣: {interests}")
    
    # 1) 起点坐标（优先起点，否则用城市中心）
    start_lnglat = None
    if starting_point:
        start_lnglat = client.geocode(starting_point, city=city)
        logger.info(f"起点坐标: {start_lnglat}")
    if not start_lnglat:
        start_lnglat = client.geocode(city)
        logger.info(f"城市中心坐标: {start_lnglat}")

    # 2) 基于兴趣搜集候选 POI
    keywords_pool: List[str] = []
    if interests:
        for it in interests:
            if it in INTEREST_KEYWORDS:
                keywords_pool.extend(INTEREST_KEYWORDS[it])
            else:
                # 如果兴趣不在预定义列表中，直接使用作为关键词
                keywords_pool.append(it)
    
    # 如果没有兴趣或兴趣关键词为空，使用通用关键词
    if not keywords_pool:
        keywords_pool = UNIVERSAL_KEYWORDS.copy()
    
    logger.info(f"搜索关键词池: {keywords_pool}")

    seen = set()
    poi_list: List[Dict[str, Any]] = []
    
    # 改进POI搜索逻辑
    for kw in keywords_pool:
        logger.info(f"搜索关键词: {kw}")
        for page in range(1, 4):  # 增加搜索页数
            try:
                pois = client.search_poi(city, keywords=kw, page=page, offset=10)
                logger.info(f"关键词'{kw}'第{page}页找到{len(pois)}个POI")
                
                for p in pois:
                    key = (p["name"], tuple(p["location"]))
                    if key in seen:
                        continue
                    seen.add(key)
                    poi_list.append(p)
                    
                    # 如果已经收集足够的POI，提前退出
                    if len(poi_list) >= days * len(SLOTS) * 2:  # 多收集一些作为备选
                        break
                
                if len(poi_list) >= days * len(SLOTS) * 2:
                    break
                    
            except Exception as e:
                logger.error(f"搜索关键词'{kw}'第{page}页时出错: {e}")
                continue
        
        if len(poi_list) >= days * len(SLOTS) * 2:
            break
    
    logger.info(f"总共收集到{len(poi_list)}个POI")
    
    # 如果POI数量不足，尝试使用更通用的关键词
    if len(poi_list) < days * len(SLOTS):
        logger.info("POI数量不足，使用更通用的关键词搜索")
        fallback_keywords = ["景点", "旅游", "地标", "公园", "广场"]
        for kw in fallback_keywords:
            if kw not in keywords_pool:
                try:
                    pois = client.search_poi(city, keywords=kw, page=1, offset=20)
                    for p in pois:
                        key = (p["name"], tuple(p["location"]))
                        if key not in seen:
                            seen.add(key)
                            poi_list.append(p)
                            if len(poi_list) >= days * len(SLOTS):
                                break
                    if len(poi_list) >= days * len(SLOTS):
                        break
                except Exception as e:
                    logger.error(f"备用关键词'{kw}'搜索出错: {e}")
                    continue
    
    logger.info(f"最终POI数量: {len(poi_list)}")

    # 3) 按天填充 & 估算移动
    days_blocks: List[Dict[str, Any]] = []
    idx = 0
    prev = start_lnglat
    
    for d in range(days):
        items: List[Item] = []
        for s in SLOTS:
            if idx < len(poi_list):
                poi = poi_list[idx]
                curr = (poi["location"][0], poi["location"][1])
                move = client.route_time(prev, curr, mode="walk", city=city) if prev else None
                items.append(Item(time_slot=s, poi=poi, move=move, notes=None))
                prev = curr
                idx += 1
            else:
                # 如果POI不足，创建占位项
                placeholder_poi = {
                    "name": f"待定景点",
                    "category": "景点",
                    "location": [0, 0],
                    "address": "待定"
                }
                items.append(Item(time_slot=s, poi=placeholder_poi, move=None, notes="需要手动添加景点"))
        
        days_blocks.append({"date": _date_plus(start_date, d), "items": [i.__dict__ for i in items]})

    # 生成地图路线
    polylines = []
    if len(days_blocks) and len(days_blocks[0]["items"]) >= 2:
        first_day = days_blocks[0]["items"]
        valid_items = [item for item in first_day if item.get("poi", {}).get("location") != [0, 0]]
        if len(valid_items) >= 2:
            a = valid_items[0]["poi"]["location"]
            b = valid_items[1]["poi"]["location"]
            polylines.append({"coords": [a, b], "mode": "walk"})

    overview = f"为{city}规划的{days}天行程，包含{len(poi_list)}个推荐景点。"
    if len(poi_list) < days * len(SLOTS):
        overview += "部分时段需要手动添加景点。"

    return {
        "city": city, 
        "days_total": days, 
        "overview": overview, 
        "days": days_blocks, 
        "map": {"polylines": polylines},
        "debug_info": {
            "total_pois": len(poi_list),
            "keywords_used": keywords_pool[:10],  # 只显示前10个关键词
            "search_success": len(poi_list) > 0
        }
    }

def _date_plus(ymd: str, offset_days: int) -> str:
    dt = datetime.strptime(ymd, "%Y-%m-%d") + timedelta(days=offset_days)
    return dt.strftime("%Y-%m-%d")

from urllib.parse import quote

def _amap_marker_link(lng: float, lat: float, name: str) -> str:
    # Web端通用 marker 深链（AMap URI 在不同端略有差异，这里用网页链接便于通用）
    # 可换 surl.amap.com 短链服务做跳转
    return f"https://uri.amap.com/marker?position={lng},{lat}&name={quote(name)}"

def _amap_direction_link(origin: tuple, dest: tuple, tname: str) -> str:
    o = f"{origin[0]},{origin[1]}"
    d = f"{dest[0]},{dest[1]}"
    return f"https://uri.amap.com/direction?from={o}&to={d}&t=walk&name={quote(tname)}"

def to_km_travel(plan: Dict[str, Any]) -> Dict[str, Any]:
    """把 /api/plan 的返回（PlanResponse JSON） 转成 kmTravel 风格内容模型"""
    city = plan.get("city", "")
    days_total = plan.get("days_total", 0)
    out_days = []
    all_days = plan.get("days", [])

    for di, day in enumerate(all_days, start=1):
        date = day.get("date", "")
        items = day.get("items", [])
        spots = []
        prev_coord = None

        for it in items:
            poi = it.get("poi") or {}
            name = poi.get("name") or "POI"
            loc = poi.get("location") or []
            
            # 验证坐标有效性
            lng, lat = None, None
            if len(loc) == 2 and isinstance(loc[0], (int, float)) and isinstance(loc[1], (int, float)):
                if loc[0] != 0 and loc[1] != 0:  # 排除 (0,0) 无效坐标
                    lng, lat = loc[0], loc[1]

            # stay_suggested_hours：简易估算（可按品类定制；这里只做演示：2小时）
            stay = 2.0

            navs = []
            # 只有有效坐标才生成导航链接
            if lng is not None and lat is not None:
                navs.append({"text": "在高德看点位", "href": _amap_marker_link(lng, lat, name)})
                if prev_coord and prev_coord != (0, 0):  # 确保前一个坐标也有效
                    navs.append({"text": "从上个点步行导航", "href": _amap_direction_link(prev_coord, (lng, lat), name)})

            # 如果是占位景点，不生成导航链接
            if name == "待定景点":
                navs = []  # 清空导航链接
                name = "待定景点（需要手动添加）"

            spots.append({
                "name": name,
                "desc": poi.get("category") or "",      # 你可以在生成逻辑里注入更丰富的文案
                "stay_suggested_hours": stay,
                "image": None,                           # 预留图片位：后续可打接高德/小红书图
                "nav_links": navs,
            })
            
            # 只有有效坐标才更新前一个坐标
            if lng is not None and lat is not None:
                prev_coord = (lng, lat)

        out_days.append({
            "title": f"Day {di}: {city}（{date}）" if city else f"Day {di}（{date}）",
            "intro": None,
            "spots": spots,
            "transport_note": "景点之间建议步行/打车，远距离可地铁/公交。",
        })

    # 生成有效的CTA链接
    cta = []
    if out_days and out_days[0]["spots"]:
        # 找到第一个有效景点的第一个可用链接
        first_day = out_days[0]["spots"]
        for spot in first_day:
            if spot.get("nav_links") and len(spot["nav_links"]) > 0:
                first_link = spot["nav_links"][0]
                if first_link.get("href") and "position=0,0" not in first_link["href"]:
                    cta.append({
                        "text": "在高德中查看首个景点",
                        "href": first_link["href"]
                    })
                    break
        
        # 如果没有找到有效链接，提供通用提示
        if not cta:
            cta.append({
                "text": "添加景点到行程",
                "href": "#"
            })

    resp = {
        "title": f"{city}{days_total}天旅行攻略" if city else f"{days_total}天旅行攻略",
        "subtitle": "根据兴趣与相邻点路况自动生成（演示版）",
        "weather": None,   # 想接近示例页可接气象 API 填充
        "tips": [
            "建议提前预约热门景点；合理安排行程与用餐。",
            "尽量错峰出行，注意当地天气与交通。",
        ],
        "days": out_days,
        "cta_links": cta,
    }
    return resp

