<template>
  <form @submit.prevent="submit">
    <div class="form-grid">
      <div>
        <span class="label">城市</span>
        <input v-model="city" required placeholder="北京" class="input" />
        <small class="help-text">建议使用中文城市名，如：北京、上海、杭州</small>
      </div>
      <div>
        <span class="label">开始日期</span>
        <input v-model="startDate" required type="date" class="input" />
      </div>
      <div>
        <span class="label">天数</span>
        <input v-model.number="days" required type="number" min="1" max="14" class="input" />
        <small class="help-text">建议1-7天，最多14天</small>
      </div>
      <div>
        <span class="label">兴趣偏好</span>
        <div class="interests-container">
          <label v-for="interest in availableInterests" :key="interest.value" class="interest-checkbox">
            <input 
              type="checkbox" 
              :value="interest.value" 
              v-model="selectedInterests"
              @change="updateInterestsString"
            />
            <span>{{ interest.label }}</span>
          </label>
        </div>
        <input v-model="interestsStr" placeholder="或直接输入关键词，用逗号分隔" class="input" />
        <small class="help-text">选择兴趣或直接输入关键词，如：博物馆,美食,公园</small>
      </div>
      <div>
        <span class="label">节奏</span>
        <select v-model="pace" class="select">
          <option value="leisurely">休闲</option>
          <option value="normal">普通</option>
          <option value="tight">紧凑</option>
        </select>
        <small class="help-text">休闲：每天2-3个景点，紧凑：每天4-5个景点</small>
      </div>
      <div>
        <span class="label">起点</span>
        <input v-model="startingPoint" placeholder="首都机场、火车站等" class="input" />
        <small class="help-text">可选，留空则从城市中心开始</small>
      </div>
    </div>
    <button class="btn" style="margin-top:14px" :disabled="!city || !startDate || days < 1">
      生成行程
    </button>
  </form>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const city = ref('北京')
const startDate = ref('2025-09-10')
const days = ref(3)
const interestsStr = ref('history,food')
const pace = ref('leisurely')
const startingPoint = ref('首都机场')

// 预设兴趣选项
const availableInterests = [
  { value: 'history', label: '历史文化' },
  { value: 'art', label: '艺术展览' },
  { value: 'nature', label: '自然风光' },
  { value: 'food', label: '美食小吃' },
  { value: 'shopping', label: '购物娱乐' },
  { value: 'entertainment', label: '娱乐休闲' },
  { value: 'religion', label: '宗教建筑' },
  { value: 'education', label: '教育科技' }
]

const selectedInterests = ref(['history', 'food'])

const emit = defineEmits(['submitReq'])

// 更新兴趣字符串
const updateInterestsString = () => {
  interestsStr.value = selectedInterests.value.join(',')
}

// 监听兴趣字符串变化，同步复选框
const syncInterestsFromString = () => {
  if (interestsStr.value) {
    const interests = interestsStr.value.split(',').map(s => s.trim()).filter(Boolean)
    selectedInterests.value = interests.filter(interest => 
      availableInterests.some(ai => ai.value === interest)
    )
  }
}

onMounted(() => {
  // 设置默认日期为明天
  const tomorrow = new Date()
  tomorrow.setDate(tomorrow.getDate() + 1)
  startDate.value = tomorrow.toISOString().split('T')[0]
  
  // 同步兴趣选择
  syncInterestsFromString()
})

const submit = () => {
  const interests = interestsStr.value ? interestsStr.value.split(',').map(s => s.trim()).filter(Boolean) : []
  emit('submitReq', { 
    city: city.value, 
    start_date: startDate.value, 
    days: days.value, 
    interests, 
    pace: pace.value, 
    starting_point: startingPoint.value 
  })
}
</script>

<style scoped>
.interests-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 8px;
  margin-bottom: 8px;
}

.interest-checkbox {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 14px;
  cursor: pointer;
}

.interest-checkbox input[type="checkbox"] {
  margin: 0;
}

.help-text {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: #666;
  font-style: italic;
}
</style>
