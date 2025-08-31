#!/usr/bin/env python3
"""
测试脚本：验证后端API功能
使用方法：python test_api.py
"""

import requests
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置
BASE_URL = "http://localhost:8000"
API_KEY = os.getenv("GAODE_API_KEY")

def test_health():
    """测试服务健康状态"""
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"✅ 服务健康检查: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ 服务健康检查失败: {e}")
        return False

def test_plan_api():
    """测试行程规划API"""
    if not API_KEY:
        print("❌ 未设置GAODE_API_KEY环境变量")
        return False
    
    print(f"🔑 使用API密钥: {API_KEY[:8]}...")
    
    # 测试数据
    test_cases = [
        {
            "name": "北京3天历史文化游",
            "data": {
                "city": "北京",
                "start_date": "2025-01-15",
                "days": 3,
                "interests": ["history", "food"],
                "pace": "normal",
                "starting_point": "天安门"
            }
        },
        {
            "name": "上海2天休闲游",
            "data": {
                "city": "上海",
                "start_date": "2025-01-15",
                "days": 2,
                "interests": ["nature", "shopping"],
                "pace": "leisurely",
                "starting_point": "人民广场"
            }
        },
        {
            "name": "杭州1天自然游",
            "data": {
                "city": "杭州",
                "start_date": "2025-01-15",
                "days": 1,
                "interests": ["nature"],
                "pace": "leisurely",
                "starting_point": "西湖"
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\n🧪 测试: {test_case['name']}")
        try:
            response = requests.post(
                f"{BASE_URL}/api/plan_km",
                json=test_case['data'],
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ API调用成功")
                print(f"   城市: {data.get('city')}")
                print(f"   天数: {data.get('days_total')}")
                print(f"   总POI数: {data.get('debug_info', {}).get('total_pois', 'N/A')}")
                print(f"   搜索成功: {data.get('debug_info', {}).get('search_success', 'N/A')}")
                
                # 检查是否有景点数据
                days = data.get('days', [])
                if days:
                    first_day = days[0]
                    items = first_day.get('items', [])
                    valid_items = [item for item in items if item.get('poi', {}).get('name') != '待定景点']
                    print(f"   第一天有效景点: {len(valid_items)}/{len(items)}")
                    
                    if valid_items:
                        print(f"   示例景点: {valid_items[0]['poi']['name']}")
                    else:
                        print(f"   ⚠️ 第一天没有有效景点")
                else:
                    print(f"   ❌ 没有返回天数数据")
                    
            else:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                
        except Exception as e:
            print(f"❌ 测试异常: {e}")

def test_amap_client():
    """测试高德地图客户端"""
    try:
        from app.services.gaode_mcp import AmapClient
        
        if not API_KEY:
            print("❌ 未设置GAODE_API_KEY环境变量")
            return False
            
        client = AmapClient()
        
        # 测试地理编码
        print("\n🧪 测试地理编码")
        result = client.geocode("天安门", "北京")
        print(f"   天安门坐标: {result}")
        
        # 测试POI搜索
        print("\n🧪 测试POI搜索")
        pois = client.search_poi("北京", "博物馆", page=1, offset=5)
        print(f"   北京博物馆搜索结果: {len(pois)}个")
        if pois:
            print(f"   示例: {pois[0]['name']} - {pois[0]['address']}")
            
        # 测试路径规划
        if result and pois:
            print("\n🧪 测试路径规划")
            route = client.route_time(result, pois[0]['location'], mode="walk", city="北京")
            print(f"   步行路径: {route}")
            
    except Exception as e:
        print(f"❌ 高德地图客户端测试失败: {e}")

def main():
    """主函数"""
    print("🚀 开始测试后端API功能")
    print("=" * 50)
    
    # 检查环境变量
    if not API_KEY:
        print("❌ 请在.env文件中设置GAODE_API_KEY")
        print("   参考: https://lbs.amap.com/ 申请API密钥")
        return
    
    # 测试服务健康状态
    if not test_health():
        print("❌ 服务未启动，请先运行: uvicorn app.main:app --reload --port 8000")
        return
    
    # 测试高德地图客户端
    test_amap_client()
    
    # 测试行程规划API
    test_plan_api()
    
    print("\n" + "=" * 50)
    print("🏁 测试完成")

if __name__ == "__main__":
    main() 