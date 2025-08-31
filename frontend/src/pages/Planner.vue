<template>
  <section>
    <PreferencesForm @submitReq="onSubmit" />
    <hr />
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

const onSubmit = async (req) => {
  errMsg.value = ''
  resp.value = null
  lastRaw.value = '(等待响应...)'
  const data = await postPlan(req)
  lastRaw.value = JSON.stringify(data, null, 2)
  console.log('[plan response]', data)
  if (data && data.error) {
    errMsg.value = String(data.error)
    return
  }
  resp.value = data
}
</script>
