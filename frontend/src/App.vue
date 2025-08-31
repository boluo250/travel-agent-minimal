<template>
  <div class="container">
    <header class="header">
      <div class="title">
        <span>🗺️ Travel Agent</span>
        <span class="badge">MVP</span>
      </div>
    </header>

    <div class="card">
      <div class="card-inner">
        <h2 class="section-title">快速生成行程</h2>
        <p class="subtitle">填写目的地与偏好，点击生成即可得到每天的景点与移动时间估算。</p>
        <Planner />
      </div>
    </div>
  </div>
</template>

<script setup>
import Planner from './pages/Planner.vue'
</script>
