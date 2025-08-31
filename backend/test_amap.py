#!/usr/bin/env python3
"""
简单的高德地图API测试脚本
使用方法：python test_amap.py
"""

import os
import sys
from dotenv import load_dotenv

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

def test_amap_client():
    """测试高德地图客户端"""
    try:
        from app.services.gaode_mcp import AmapClient
        
        # 检查API密钥
        api_key = os.getenv("GAODE_API_KEY")
        if not api_key:
            print("❌ 未设置GAODE_API_KEY环境变量")
            print("请在backend目录下创建.env文件并设置GAODE_API_KEY")
            return False
        
        print(f"🔑 API密钥: {api_key[:8]}...")
        
        # 创建客户端
        client = AmapClient()
        
        # 测试地理编码
        print("\n🧪 测试地理编码")
        print("   城市: 北京")
        result = client.geocode("北京")
        if result:
            print(f"   ✅ 成功: 北京 -> {result}")
        else:
            print("   ❌ 失败: 无法获取北京坐标")
            return False
        
        # 测试POI搜索
        print("\n🧪 测试POI搜索")
        print("   城市: 北京, 关键词: 博物馆")
        pois = client.search_poi("北京", "博物馆", page=1, offset=5)
        if pois:
            print(f"   ✅ 成功: 找到{len(pois)}个POI")
            for i, poi in enumerate(pois[:3]):
                print(f"      {i+1}. {poi['name']} - {poi['address']}")
        else:
            print("   ❌ 失败: 未找到任何POI")
            return False
        
        # 测试路径规划
        if pois:
            print("\n🧪 测试路径规划")
            print(f"   从北京中心到{pois[0]['name']}")
            route = client.route_time(result, pois[0]['location'], mode="walk", city="北京")
            if route:
                print(f"   ✅ 成功: 步行{route['distance_km']}km, 约{route['est_duration_min']}分钟")
            else:
                print("   ❌ 失败: 无法计算路径")
        
        print("\n🎉 所有测试通过！高德地图API工作正常")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("🚀 开始测试高德地图API")
    print("=" * 50)
    
    success = test_amap_client()
    
    if success:
        print("\n✅ 建议:")
        print("1. 检查.env文件中的GAODE_API_KEY是否正确")
        print("2. 确保网络连接正常")
        print("3. 检查高德地图API使用量是否超限")
    else:
        print("\n❌ 问题排查:")
        print("1. 检查.env文件是否存在并包含正确的GAODE_API_KEY")
        print("2. 确保已安装所有依赖: pip install -r requirements.txt")
        print("3. 检查网络连接和防火墙设置")
        print("4. 查看高德开放平台API状态")

if __name__ == "__main__":
    main() 