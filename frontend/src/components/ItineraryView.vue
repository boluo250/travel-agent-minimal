<template>
  <section v-if="data">
    <h2>{{ data.title || `${data.city} · 共 ${data.days_total} 天` }}</h2>
    <p>{{ data.overview }}</p>
    
    <!-- 调试信息 -->
    <details v-if="data.debug_info" style="margin: 12px 0; padding: 12px; background: #f5f5f5; border-radius: 4px;">
      <summary style="cursor: pointer; font-weight: bold;">🔍 调试信息</summary>
      <div style="margin-top: 8px; font-size: 14px;">
        <p><strong>总POI数量:</strong> {{ data.debug_info.total_pois }}</p>
        <p><strong>搜索成功:</strong> {{ data.debug_info.search_success ? '✅ 是' : '❌ 否' }}</p>
        <p><strong>使用关键词:</strong> {{ data.debug_info.keywords_used?.join(', ') }}</p>
      </div>
    </details>

    <p v-if="!data.days || !data.days.length" style="opacity:.75">未找到合适的 POI，试试调整兴趣或天数。</p>

    <div v-for="(d, idx) in (data.days || [])" :key="idx" style="margin:12px 0; padding:12px; border:1px solid #eee; border-radius: 8px;">
      <h3>{{ d.title || `第 ${idx + 1} 天 · ${d.date || '待定日期'}` }}</h3>
      
      <!-- 兼容两种数据结构：items 和 spots -->
      <div v-if="d.items && d.items.length" class="day-items">
        <h4>行程安排</h4>
        <ul style="list-style: none; padding: 0;">
          <li v-for="(it, j) in d.items" :key="j" class="item-card">
            <div class="item-header">
              <span class="time-slot">{{ it.time_slot || `时段 ${j + 1}` }}</span>
              <span v-if="it.poi && it.poi.name" class="poi-name">{{ it.poi.name }}</span>
              <span v-else class="placeholder">待定景点</span>
            </div>
            
            <div v-if="it.poi && it.poi.category" class="poi-info">
              类型: {{ it.poi.category }}
            </div>
            
            <div v-if="it.poi && it.poi.address && it.poi.address !== '待定'" class="poi-info">
              地址: {{ it.poi.address }}
            </div>
            
            <div v-if="it.poi && it.poi.location && it.poi.location[0] !== 0" class="poi-info">
              坐标: {{ it.poi.location.join(', ') }}
            </div>
            
            <div v-if="it.move" class="move-info">
              <span>🚶 移动: {{ it.move.mode }} | 约 {{ it.move.est_duration_min }} 分钟 | {{ it.move.distance_km }} km</span>
            </div>
            
            <div v-if="it.notes" class="notes">
              📝 {{ it.notes }}
            </div>
            
            <!-- 占位景点提示 -->
            <div v-if="it.poi && it.poi.name === '待定景点'" class="placeholder-warning">
              ⚠️ 这个时段还没有安排景点，请手动添加您感兴趣的景点
            </div>
          </li>
        </ul>
      </div>
      
      <!-- 显示spots格式的数据 -->
      <div v-else-if="d.spots && d.spots.length" class="day-spots">
        <h4>景点推荐</h4>
        <ul style="list-style: none; padding: 0;">
          <li v-for="(spot, j) in d.spots" :key="j" class="spot-card">
            <div class="spot-header">
              <span class="spot-name">{{ spot.name }}</span>
              <span v-if="spot.stay_suggested_hours" class="stay-time">
                ⏱️ 建议停留: {{ spot.stay_suggested_hours }}小时
              </span>
            </div>
            
            <div v-if="spot.desc" class="spot-desc">
              类型: {{ spot.desc }}
            </div>
            
            <!-- 导航链接 -->
            <div v-if="spot.nav_links && spot.nav_links.length" class="nav-links">
              <a 
                v-for="(link, linkIdx) in spot.nav_links" 
                :key="linkIdx"
                :href="link.href" 
                target="_blank"
                class="nav-link"
              >
                {{ link.text }}
              </a>
            </div>
          </li>
        </ul>
      </div>
      
      <!-- 如果没有行程数据 -->
      <div v-else class="no-data">
        <p style="color: #999; font-style: italic;">暂无行程安排</p>
      </div>
      
      <!-- 交通提示 -->
      <div v-if="d.transport_note" class="transport-note">
        🚌 {{ d.transport_note }}
      </div>
    </div>
    
    <!-- 提示信息 -->
    <div v-if="data.tips && data.tips.length" class="tips-section">
      <h4>💡 旅行小贴士</h4>
      <ul>
        <li v-for="(tip, idx) in data.tips" :key="idx">
          {{ tip }}
        </li>
      </ul>
    </div>
    
    <!-- 行动链接 -->
    <div v-if="data.cta_links && data.cta_links.length" class="cta-section">
      <a 
        v-for="(link, idx) in data.cta_links" 
        :key="idx"
        :href="link.href" 
        target="_blank"
        class="cta-link"
      >
        {{ link.text }}
      </a>
    </div>
  </section>
</template>

<script setup>
defineProps({ data: { type: Object, required: true } })
</script>

<style scoped>
.day-items, .day-spots {
  margin: 16px 0;
}

.item-card, .spot-card {
  margin: 12px 0;
  padding: 16px;
  background: #fafafa;
  border-radius: 8px;
  border-left: 4px solid #3498db;
}

.item-header, .spot-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
  gap: 12px;
}

.time-slot {
  font-weight: bold;
  color: #2c3e50;
  min-width: 80px;
  background: #ecf0f1;
  padding: 4px 8px;
  border-radius: 4px;
  text-align: center;
}

.poi-name, .spot-name {
  font-weight: bold;
  color: #e74c3c;
  font-size: 16px;
}

.placeholder {
  font-style: italic;
  color: #7f8c8d;
}

.poi-info, .spot-desc {
  margin-left: 80px;
  color: #34495e;
  font-size: 14px;
  margin-bottom: 4px;
}

.move-info {
  margin-left: 80px;
  margin-top: 8px;
  padding: 8px 12px;
  background: #e8f5e8;
  border-radius: 6px;
  display: inline-block;
  color: #27ae60;
}

.notes {
  margin-left: 80px;
  margin-top: 8px;
  color: #e67e22;
  font-style: italic;
}

.placeholder-warning {
  margin-left: 80px;
  margin-top: 12px;
  padding: 12px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 6px;
  color: #856404;
}

.stay-time {
  font-size: 14px;
  color: #7f8c8d;
  background: #f8f9fa;
  padding: 4px 8px;
  border-radius: 4px;
}

.nav-links {
  margin-top: 12px;
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.nav-link {
  display: inline-block;
  padding: 6px 12px;
  background: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 4px;
  font-size: 14px;
  transition: background-color 0.2s;
}

.nav-link:hover {
  background: #2980b9;
}

.transport-note {
  margin-top: 16px;
  padding: 12px;
  background: #e3f2fd;
  border-radius: 6px;
  color: #1565c0;
  font-size: 14px;
}

.no-data {
  text-align: center;
  padding: 20px;
  color: #999;
}

.tips-section {
  margin-top: 24px;
  padding: 20px;
  background: #e3f2fd;
  border-radius: 8px;
  border-left: 4px solid #2196f3;
}

.tips-section h4 {
  margin: 0 0 16px 0;
  color: #1976d2;
}

.tips-section ul {
  margin: 0;
  padding-left: 20px;
}

.tips-section li {
  margin: 8px 0;
  color: #1565c0;
}

.cta-section {
  margin-top: 24px;
  text-align: center;
}

.cta-link {
  display: inline-block;
  margin: 8px;
  padding: 14px 28px;
  background: #3498db;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  font-weight: bold;
  font-size: 16px;
  transition: all 0.2s;
}

.cta-link:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}
</style>
