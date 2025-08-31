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
      <h3>第 {{ idx + 1 }} 天 · {{ d.date }}</h3>
      <ul style="list-style: none; padding: 0;">
        <li v-for="(it, j) in (d.items || [])" :key="j" style="margin: 8px 0; padding: 8px; background: #fafafa; border-radius: 4px;">
          <div style="display: flex; align-items: center; margin-bottom: 4px;">
            <span style="font-weight: bold; color: #2c3e50; min-width: 80px;">{{ it.time_slot }}</span>
            <span v-if="it.poi && it.poi.name" style="font-weight: bold; color: #e74c3c;">{{ it.poi.name }}</span>
            <span v-else style="font-style: italic; color: #7f8c8d;">待定景点</span>
          </div>
          
          <div v-if="it.poi && it.poi.category" style="margin-left: 80px; color: #34495e; font-size: 14px;">
            类型: {{ it.poi.category }}
          </div>
          
          <div v-if="it.poi && it.poi.address && it.poi.address !== '待定'" style="margin-left: 80px; color: #7f8c8d; font-size: 14px;">
            地址: {{ it.poi.address }}
          </div>
          
          <div v-if="it.poi && it.poi.location && it.poi.location[0] !== 0" style="margin-left: 80px; color: #7f8c8d; font-size: 14px;">
            坐标: {{ it.poi.location.join(', ') }}
          </div>
          
          <div v-if="it.move" style="margin-left: 80px; margin-top: 4px; padding: 4px 8px; background: #e8f5e8; border-radius: 4px; display: inline-block;">
            <span style="color: #27ae60;">🚶 移动: {{ it.move.mode }} | 约 {{ it.move.est_duration_min }} 分钟 | {{ it.move.distance_km }} km</span>
          </div>
          
          <div v-if="it.notes" style="margin-left: 80px; margin-top: 4px; color: #e67e22; font-style: italic;">
            📝 {{ it.notes }}
          </div>
          
          <!-- 占位景点提示 -->
          <div v-if="it.poi && it.poi.name === '待定景点'" style="margin-left: 80px; margin-top: 8px; padding: 8px; background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 4px;">
            <span style="color: #856404;">⚠️ 这个时段还没有安排景点，请手动添加您感兴趣的景点</span>
          </div>
        </li>
      </ul>
    </div>
    
    <!-- 提示信息 -->
    <div v-if="data.tips && data.tips.length" style="margin-top: 20px; padding: 16px; background: #e3f2fd; border-radius: 8px; border-left: 4px solid #2196f3;">
      <h4 style="margin: 0 0 12px 0; color: #1976d2;">💡 旅行小贴士</h4>
      <ul style="margin: 0; padding-left: 20px;">
        <li v-for="(tip, idx) in data.tips" :key="idx" style="margin: 4px 0; color: #1565c0;">
          {{ tip }}
        </li>
      </ul>
    </div>
    
    <!-- 行动链接 -->
    <div v-if="data.cta_links && data.cta_links.length" style="margin-top: 20px; text-align: center;">
      <a 
        v-for="(link, idx) in data.cta_links" 
        :key="idx"
        :href="link.href" 
        target="_blank"
        style="display: inline-block; margin: 8px; padding: 12px 24px; background: #3498db; color: white; text-decoration: none; border-radius: 6px; font-weight: bold;"
      >
        {{ link.text }}
      </a>
    </div>
  </section>
</template>

<script setup>
defineProps({ data: { type: Object, required: true } })
</script>
