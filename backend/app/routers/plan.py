from fastapi import APIRouter, HTTPException
from app.schemas.plan import PlanRequest, KmTravelResponse
from app.services.gaode_mcp import AmapClient
from app.utils.itinerary import build_itinerary, to_km_travel
import logging

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/plan_km", response_model=KmTravelResponse)
def create_plan_km(req: PlanRequest):
    client = AmapClient()
    try:
        logger.info(f"开始规划行程: 城市={req.city}, 天数={req.days}, 兴趣={req.interests}")
        
        raw = build_itinerary(
            client=client,
            city=req.city,
            days=req.days,
            interests=req.interests,
            starting_point=req.starting_point,
            start_date=req.start_date,
        )
        
        logger.info(f"原始行程数据: {raw.get('debug_info', {})}")
        
        shaped = to_km_travel(raw)
        
        logger.info(f"转换后数据: 天数={len(shaped.get('days', []))}, 景点总数={sum(len(day.get('spots', [])) for day in shaped.get('days', []))}")
        
        return shaped
        
    except Exception as e:
        logger.error(f"行程规划失败: {e}")
        raise HTTPException(status_code=502, detail=f"Upstream error: {e}")


@router.get("/debug/amap")
async def debug_amap(city: str = "北京", keywords: str = "博物馆"):
    """调试高德地图API功能"""
    try:
        client = AmapClient()
        
        # 测试地理编码
        geocode_result = client.geocode(city)
        
        # 测试POI搜索
        poi_result = client.search_poi(city, keywords, page=1, offset=5)
        
        # 测试路径规划（如果有坐标的话）
        route_result = None
        if geocode_result and poi_result:
            route_result = client.route_time(geocode_result, poi_result[0]['location'], mode="walk", city=city)
        
        return {
            "status": "success",
            "geocode": {
                "city": city,
                "result": geocode_result,
                "success": geocode_result is not None
            },
            "poi_search": {
                "city": city,
                "keywords": keywords,
                "count": len(poi_result),
                "results": poi_result[:3],  # 只返回前3个结果
                "success": len(poi_result) > 0
            },
            "route_planning": {
                "success": route_result is not None,
                "result": route_result
            },
            "api_key_status": {
                "configured": bool(client.api_key),
                "key_preview": client.api_key[:8] + "..." if client.api_key else None
            }
        }
        
    except Exception as e:
        logger.error(f"调试API失败: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

