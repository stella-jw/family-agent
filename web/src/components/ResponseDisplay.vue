<script setup lang="ts">
import type { AddResponse, SearchResult } from '../composables/useApi'

defineProps<{
  response: AddResponse | null
  searchResults: SearchResult[]
  searchMode: boolean
}>()
</script>

<template>
  <div class="response-display">
    <!-- Add response -->
    <div v-if="response" class="add-response" :class="{ success: response.success }">
      <div class="status-icon">
        {{ response.success ? '✅' : '❌' }}
      </div>
      <div class="message">{{ response.message }}</div>

      <div v-if="response.success && (response.added_count > 0 || response.updated_count > 0)" class="stats">
        <span v-if="response.added_count > 0" class="stat added">
          新增 {{ response.added_count }} 条
        </span>
        <span v-if="response.updated_count > 0" class="stat updated">
          更新 {{ response.updated_count }} 条
        </span>
      </div>

      <div v-if="response.details.length > 0" class="details">
        <div
          v-for="(detail, index) in response.details"
          :key="index"
          class="detail-item"
        >
          <span class="name">{{ detail.name || '(未知)' }}</span>
          <span class="action" :class="detail.action">
            {{ detail.action === 'added' ? '新增' : '更新' }}
          </span>
        </div>
      </div>
    </div>

    <!-- Search results -->
    <div v-if="searchMode && searchResults.length > 0" class="search-results">
      <div class="results-header">
        <span class="icon">🔍</span>
        <span class="count">找到 {{ searchResults.length }} 条相关记录</span>
      </div>

      <div class="results-list">
        <div
          v-for="(result, index) in searchResults"
          :key="index"
          class="result-item"
        >
          <div class="member-badge">{{ result.member_name }}</div>
          <div class="content">{{ result.content }}</div>
          <div class="meta">
            <span class="type">{{ result.attribute_type }}</span>
            <span class="time">{{ result.timestamp }}</span>
          </div>
        </div>
      </div>
    </div>

    <div v-if="searchMode && searchResults.length === 0 && response" class="no-results">
      <span class="icon">🤔</span>
      <span>没有找到相关信息</span>
    </div>
  </div>
</template>

<style scoped>
.response-display {
  margin-top: 20px;
}

.add-response {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.add-response.success {
  border-left: 4px solid #52c41a;
}

.status-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.message {
  font-size: 18px;
  color: #333;
  margin-bottom: 12px;
}

.stats {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin-bottom: 16px;
}

.stat {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 14px;
}

.stat.added {
  background: #e6f7ff;
  color: #1890ff;
}

.stat.updated {
  background: #fff7e6;
  color: #fa8c16;
}

.details {
  text-align: left;
  margin-top: 12px;
}

.detail-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 6px;
  margin-bottom: 6px;
}

.name {
  font-weight: 500;
  color: #333;
}

.action {
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
}

.action.added {
  background: #52c41a;
  color: white;
}

.action.updated {
  background: #fa8c16;
  color: white;
}

.search-results {
  background: white;
  border-radius: 12px;
  padding: 20px;
}

.results-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

.results-header .icon {
  font-size: 20px;
}

.results-header .count {
  font-size: 16px;
  color: #666;
}

.results-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.result-item {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 8px;
}

.member-badge {
  display: inline-block;
  padding: 2px 10px;
  background: #667eea;
  color: white;
  border-radius: 10px;
  font-size: 12px;
  margin-bottom: 8px;
}

.content {
  color: #333;
  margin-bottom: 8px;
  line-height: 1.5;
}

.meta {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: #999;
}

.type {
  background: #eee;
  padding: 2px 6px;
  border-radius: 4px;
}

.no-results {
  background: white;
  border-radius: 12px;
  padding: 40px;
  text-align: center;
  color: #999;
}

.no-results .icon {
  font-size: 40px;
  display: block;
  margin-bottom: 12px;
}
</style>
