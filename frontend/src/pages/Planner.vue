<template>
  <section>
    <PreferencesForm @submitReq="onSubmit" />
    <hr />
    
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
</script>
