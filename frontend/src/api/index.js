import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 60000  // 增加到60秒
})

export async function postPlan(payload) {
  try {
    console.log('🚀 发送行程规划请求:', payload)
    const startTime = Date.now()
    
    const { data } = await client.post('/plan_km', payload)
    
    const duration = Date.now() - startTime
    console.log(`✅ 请求完成，耗时: ${duration}ms`)
    
    return data
  } catch (err) {
    const duration = Date.now() - startTime
    console.error(`❌ 请求失败，耗时: ${duration}ms`, err)
    
    if (err.code === 'ECONNABORTED') {
      return { error: '请求超时，请稍后重试。如果问题持续，请检查网络连接。' }
    }
    
    const msg = err?.response?.data?.detail || err?.message || '请求失败，请检查网络或后端服务'
    return { error: String(msg) }
  }
}
