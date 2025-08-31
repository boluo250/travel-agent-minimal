// 测试数据：模拟后端返回的行程数据
export const testTripData = {
  "title": "北京3天旅行攻略",
  "subtitle": "根据兴趣与相邻点路况自动生成（演示版）",
  "city": "北京",
  "days_total": 3,
  "overview": "为北京规划的3天行程，包含15个推荐景点。",
  "weather": null,
  "tips": [
    "建议提前预约热门景点；合理安排行程与用餐。",
    "尽量错峰出行，注意当地天气与交通。"
  ],
  "days": [
    {
      "title": "Day 1: 北京（2025-09-01）",
      "intro": null,
      "spots": [
        {
          "name": "中国国家博物馆",
          "desc": "博物馆",
          "stay_suggested_hours": 2,
          "image": null,
          "nav_links": [
            {
              "text": "在高德看点位",
              "href": "https://uri.amap.com/marker?position=116.407387,39.904179&name=中国国家博物馆"
            }
          ]
        },
        {
          "name": "故宫博物院",
          "desc": "古迹",
          "stay_suggested_hours": 3,
          "image": null,
          "nav_links": [
            {
              "text": "在高德看点位",
              "href": "https://uri.amap.com/marker?position=116.397128,39.916527&name=故宫博物院"
            },
            {
              "text": "从上个点步行导航",
              "href": "https://uri.amap.com/direction?from=116.407387,39.904179&to=116.397128,39.916527&t=walk&name=故宫博物院"
            }
          ]
        },
        {
          "name": "天安门广场",
          "desc": "广场",
          "stay_suggested_hours": 1.5,
          "image": null,
          "nav_links": [
            {
              "text": "在高德看点位",
              "href": "https://uri.amap.com/marker?position=116.397128,39.903119&name=天安门广场"
            },
            {
              "text": "从上个点步行导航",
              "href": "https://uri.amap.com/direction?from=116.397128,39.916527&to=116.397128,39.903119&t=walk&name=天安门广场"
            }
          ]
        }
      ],
      "transport_note": "景点之间建议步行/打车，远距离可地铁/公交。"
    },
    {
      "title": "Day 2: 北京（2025-09-02）",
      "intro": null,
      "spots": [
        {
          "name": "颐和园",
          "desc": "公园",
          "stay_suggested_hours": 3,
          "image": null,
          "nav_links": [
            {
              "text": "在高德看点位",
              "href": "https://uri.amap.com/marker?position=116.2755,39.9999&name=颐和园"
            }
          ]
        },
        {
          "name": "圆明园遗址公园",
          "desc": "公园",
          "stay_suggested_hours": 2.5,
          "image": null,
          "nav_links": [
            {
              "text": "在高德看点位",
              "href": "https://uri.amap.com/marker?position=116.2995,39.9999&name=圆明园遗址公园"
            },
            {
              "text": "从上个点步行导航",
              "href": "https://uri.amap.com/direction?from=116.2755,39.9999&to=116.2995,39.9999&t=walk&name=圆明园遗址公园"
            }
          ]
        }
      ],
      "transport_note": "景点之间建议步行/打车，远距离可地铁/公交。"
    }
  ],
  "cta_links": [
    {
      "text": "在高德中查看首个景点",
      "href": "https://uri.amap.com/marker?position=116.407387,39.904179&name=中国国家博物馆"
    }
  ],
  "debug_info": {
    "total_pois": 15,
    "keywords_used": ["博物馆", "古迹", "历史文化", "故宫", "天坛"],
    "search_success": true
  }
};

// 测试数据：模拟原始后端数据结构
export const testRawData = {
  "city": "北京",
  "days_total": 1,
  "overview": "为北京规划的1天行程，包含3个推荐景点。",
  "days": [
    {
      "date": "2025-09-01",
      "items": [
        {
          "time_slot": "morning",
          "poi": {
            "name": "中国国家博物馆",
            "category": "博物馆",
            "location": [116.407387, 39.904179],
            "address": "东长安街16号天安门广场东侧"
          },
          "move": {
            "mode": "walk",
            "distance_km": 0.5,
            "est_duration_min": 8
          },
          "notes": null
        },
        {
          "time_slot": "noon",
          "poi": {
            "name": "故宫博物院",
            "category": "古迹",
            "location": [116.397128, 39.916527],
            "address": "景山前街4号"
          },
          "move": {
            "mode": "walk",
            "distance_km": 1.2,
            "est_duration_min": 15
          },
          "notes": null
        }
      ]
    }
  ],
  "map": {
    "polylines": [
      {
        "coords": [[116.407387, 39.904179], [116.397128, 39.916527]],
        "mode": "walk"
      }
    ]
  },
  "debug_info": {
    "total_pois": 3,
    "keywords_used": ["博物馆", "古迹"],
    "search_success": true
  }
}; 