import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  timeout: 15000
})

export async function postPlan(payload) {
  try {
    const { data } = await client.post('/plan_km', payload)
    return data
  } catch (err) {
    const msg = err?.response?.data?.detail || err?.message || '请求失败，请检查网络或后端服务'
    return { error: String(msg) }
  }
}
