from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class PlanRequest(BaseModel):
    city: str = Field(..., description="城市名")
    start_date: str = Field(..., description="开始日期 YYYY-MM-DD")
    days: int = Field(1, description="出行天数")
    interests: Optional[List[str]] = None
    pace: Optional[str] = None
    starting_point: Optional[str] = None

class PlanResponse(BaseModel):
    city: str
    days_total: int
    overview: str
    days: List[Dict[str, Any]]
    map: Dict[str, Any]

class KmImage(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None

class KmNavLink(BaseModel):
    text: str
    href: str

class KmSpot(BaseModel):
    name: str
    desc: Optional[str] = None
    stay_suggested_hours: Optional[float] = None
    image: Optional[KmImage] = None
    nav_links: List[KmNavLink] = []

class KmDay(BaseModel):
    title: str                 # e.g. "Day 1: 北京市区游 (2025-09-10)"
    intro: Optional[str] = None
    spots: List[KmSpot] = []
    transport_note: Optional[str] = None

class KmTravelResponse(BaseModel):
    title: str                 # e.g. "北京3天旅行攻略"
    subtitle: Optional[str] = None
    weather: Optional[List[Dict[str, Any]]] = None   # 预留：要接天气 API 再填
    tips: Optional[List[str]] = None
    days: List[KmDay]
    cta_links: Optional[List[KmNavLink]] = None      # 例如“一键生成你的专属地图”
