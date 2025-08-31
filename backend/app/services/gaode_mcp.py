from __future__ import annotations

import httpx
from typing import Dict, Any, List, Optional, Tuple
from app.core import config
import logging

# 设置日志
logger = logging.getLogger(__name__)

AMAP_BASE = "https://restapi.amap.com/v3"

def _parse_lnglat(s: str) -> Optional[Tuple[float, float]]:
    try:
        lng, lat = s.split(",")
        return float(lng), float(lat)
    except Exception:
        return None

class AmapClient:
    """Minimal Amap REST client.
    默认使用高德 Web Service；如你部署了 MCP server，可在此类中扩展优先走 MCP 的分支。
    """

    def __init__(self, api_key: Optional[str] = None, timeout: int = None):
        self.api_key = api_key or config.GAODE_API_KEY
        self.timeout = timeout or config.REQUEST_TIMEOUT_SECONDS
        self.http = httpx.Client(timeout=self.timeout)
        
        if not self.api_key:
            logger.error("高德地图API密钥未设置！请在.env文件中设置GAODE_API_KEY")
        else:
            logger.info(f"高德地图客户端初始化完成，API密钥: {self.api_key[:8]}...")

    # --- Geocoding ---
    def geocode(self, address: str, city: Optional[str] = None) -> Optional[Tuple[float, float]]:
        if not self.api_key:
            logger.error("API密钥未设置，无法进行地理编码")
            return None
            
        params = {"key": self.api_key, "address": address}
        if city:
            params["city"] = city
            
        try:
            logger.info(f"地理编码请求: {address}, 城市: {city}")
            r = self.http.get(f"{AMAP_BASE}/geocode/geo", params=params)
            data = r.json()
            logger.info(f"地理编码响应状态: {data.get('status')}, 结果数: {data.get('count')}")
            
            if data.get("status") != "1" or int(data.get("count", "0")) < 1:
                logger.warning(f"地理编码失败: {data.get('info', '未知错误')}")
                return None
                
            loc = data["geocodes"][0].get("location")
            result = _parse_lnglat(loc) if loc else None
            logger.info(f"地理编码成功: {address} -> {result}")
            return result
            
        except Exception as e:
            logger.error(f"地理编码请求异常: {e}")
            return None

    # --- POI search ---
    def search_poi(self, city: str, keywords: str, page: int = 1, offset: int = 10, extensions: str = "base") -> List[Dict[str, Any]]:
        if not self.api_key:
            logger.error("API密钥未设置，无法进行POI搜索")
            return []
            
        params = {
            "key": self.api_key, 
            "city": city, 
            "keywords": keywords, 
            "page": page, 
            "offset": offset, 
            "extensions": extensions
        }
        
        try:
            logger.info(f"POI搜索请求: 城市={city}, 关键词={keywords}, 页码={page}, 数量={offset}")
            r = self.http.get(f"{AMAP_BASE}/place/text", params=params)
            data = r.json()
            logger.info(f"POI搜索响应状态: {data.get('status')}, 结果数: {data.get('count')}")
            
            if data.get("status") != "1":
                logger.warning(f"POI搜索失败: {data.get('info', '未知错误')}")
                return []
                
            pois = []
            raw_pois = data.get("pois", [])
            logger.info(f"原始POI数据: {len(raw_pois)}个")
            
            for p in raw_pois:
                loc = _parse_lnglat(p.get("location", ""))
                if not loc:
                    logger.warning(f"POI '{p.get('name')}' 位置信息无效: {p.get('location')}")
                    continue
                    
                poi_data = {
                    "id": p.get("id"), 
                    "name": p.get("name"), 
                    "category": p.get("type"), 
                    "location": [loc[0], loc[1]], 
                    "address": p.get("address"),
                    "tel": p.get("tel"),
                    "distance": p.get("distance"),
                    "rating": p.get("rating")
                }
                pois.append(poi_data)
                
            logger.info(f"POI搜索成功: 关键词'{keywords}'找到{len(pois)}个有效POI")
            return pois
            
        except Exception as e:
            logger.error(f"POI搜索请求异常: {e}")
            return []

    # --- Routing ---
    def route_time(self, origin: Tuple[float, float], destination: Tuple[float, float], mode: str = "walk", city: Optional[str] = None) -> Optional[Dict[str, Any]]:
        if not self.api_key:
            logger.error("API密钥未设置，无法进行路径规划")
            return None
            
        o = f"{origin[0]},{origin[1]}"
        d = f"{destination[0]},{destination[1]}"
        
        try:
            if mode == "drive":
                url = f"{AMAP_BASE}/direction/driving"
                params = {"origin": o, "destination": d, "key": self.api_key}
            elif mode == "transit":
                url = f"{AMAP_BASE}/direction/transit/integrated"
                params = {"origin": o, "destination": d, "key": self.api_key}
                if city:
                    params["city"] = city
            else:
                url = f"{AMAP_BASE}/direction/walking"
                params = {"origin": o, "destination": d, "key": self.api_key}
                
            logger.info(f"路径规划请求: {mode}模式, 从{origin}到{destination}")
            r = self.http.get(url, params=params)
            data = r.json()
            logger.info(f"路径规划响应状态: {data.get('status')}")
            
            if data.get("status") != "1":
                logger.warning(f"路径规划失败: {data.get('info', '未知错误')}")
                return None
                
            route = data.get("route") or {}
            
            if mode == "transit" and route.get("transits"):
                t = route["transits"][0]
                dist_m = float(t.get("distance", "0") or 0)
                dur_s = float(t.get("duration", "0") or 0)
            else:
                paths = route.get("paths") or []
                if not paths:
                    logger.warning("路径规划未找到有效路径")
                    return None
                p0 = paths[0]
                dist_m = float(p0.get("distance", "0") or 0)
                dur_s = float(p0.get("duration", "0") or 0)
                
            result = {
                "mode": mode, 
                "distance_km": round(dist_m/1000.0, 2), 
                "est_duration_min": int(round(dur_s/60.0))
            }
            logger.info(f"路径规划成功: {result}")
            return result
            
        except Exception as e:
            logger.error(f"路径规划请求异常: {e}")
            return None

    def __del__(self):
        """清理HTTP客户端"""
        if hasattr(self, 'http'):
            self.http.close()
