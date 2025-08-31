<template>
  <section>
    <PreferencesForm @submitReq="onSubmit" />
    <hr />
    
    <!-- 测试按钮 -->
    <div style="margin: 16px 0; padding: 16px; background: #f8f9fa; border-radius: 8px;">
      <h4 style="margin: 0 0 12px 0;">🧪 测试组件显示</h4>
      <button @click="testWithSampleData" style="margin-right: 8px; padding: 8px 16px; background: #28a745; color: white; border: none; border-radius: 4px; cursor: pointer;">
        测试KmTravel格式
      </button>
      <button @click="testWithRawData" style="padding: 8px 16px; background: #17a2b8; color: white; border: none; border-radius: 4px; cursor: pointer;">
        测试原始格式
      </button>
      <button @click="clearTestData" style="margin-left: 8px; padding: 8px 16px; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer;">
        清除测试数据
      </button>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" style="text-align: center; padding: 20px; color: #666;">
      <div style="margin-bottom: 10px;">🔄 正在生成行程，请稍候...</div>
      <div style="font-size: 14px;">这可能需要几秒钟时间，请耐心等待</div>
    </div>
    
    <p v-if="errMsg" style="color:#c00; padding:8px 0">{{ errMsg }}</p>

    <details style="margin:8px 0">
      <summary>调试：最后一次响应</summary>
      <pre style="white-space:pre-wrap; word-break:break-all">{{ lastRaw }}</pre>
    </details>

    <ItineraryView v-if="resp" :data="resp" />
  </section>
</template>

<script setup>
import { ref } from 'vue'
import PreferencesForm from '../components/PreferencesForm.vue'
import ItineraryView from '../components/ItineraryView.vue'
import { postPlan } from '../api'

const resp = ref(null)
const errMsg = ref('')
const lastRaw = ref('')
const loading = ref(false)

// 测试数据
const testTripData = {
  "title": "北京3天旅行攻略",
  "subtitle": "根据兴趣与相邻点路况自动生成（演示版）",
  "city": "北京",
  "days_total": 3,
  "overview": "为北京规划的3天行程，包含15个推荐景点。",
  "days": [
    {
      "title": "Day 1: 北京（2025-09-01）",
      "spots": [
        {
          "name": "中国国家博物馆",
          "desc": "博物馆",
          "stay_suggested_hours": 2,
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
          "nav_links": [
            {
              "text": "在高德看点位",
              "href": "https://uri.amap.com/marker?position=116.397128,39.916527&name=故宫博物院"
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
    "keywords_used": ["博物馆", "古迹", "历史文化"],
    "search_success": true
  }
};

const testRawData = {
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
          }
        }
      ]
    }
  ],
  "debug_info": {
    "total_pois": 3,
    "keywords_used": ["博物馆", "古迹"],
    "search_success": true
  }
};

const onSubmit = async (req) => {
  errMsg.value = ''
  resp.value = null
  loading.value = true
  lastRaw.value = '(等待响应...)'
  
  try {
    const data = await postPlan(req)
    lastRaw.value = JSON.stringify(data, null, 2)
    console.log('[plan response]', data)
    
    if (data && data.error) {
      errMsg.value = String(data.error)
      return
    }
    
    resp.value = data
  } catch (error) {
    console.error('请求异常:', error)
    errMsg.value = '请求发生异常，请稍后重试'
    lastRaw.value = `Error: ${error.message}`
  } finally {
    loading.value = false
  }
}

const testWithSampleData = () => {
  resp.value = testTripData
  lastRaw.value = JSON.stringify(testTripData, null, 2)
  errMsg.value = ''
}

const testWithRawData = () => {
  resp.value = testRawData
  lastRaw.value = JSON.stringify(testRawData, null, 2)
  errMsg.value = ''
}

const clearTestData = () => {
  resp.value = null
  lastRaw.value = ''
  errMsg.value = ''
}
</script>
