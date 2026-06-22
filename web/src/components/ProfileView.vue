<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi, type ProfileResponse } from '../composables/useApi'

const props = defineProps<{
  name: string
}>()

const emit = defineEmits<{
  (e: 'back'): void
}>()

const { getProfile, loading } = useApi()
const profile = ref<ProfileResponse | null>(null)

onMounted(async () => {
  try {
    profile.value = await getProfile(props.name)
  } catch (e) {
    console.error('Failed to load profile:', e)
  }
})

function getTypeLabel(type: string): string {
  const labels: Record<string, string> = {
    basic_info: '基本信息',
    hobby: '兴趣爱好',
    work_experience: '工作经历',
    life_event: '生活事件',
    personality: '性格特点',
    ability: '能力特长',
    relationship: '家庭关系'
  }
  return labels[type] || type
}
</script>

<template>
  <div class="profile-view">
    <div class="header">
      <button class="back-btn" @click="emit('back')">‹ 返回</button>
      <h3>{{ name }} 的档案</h3>
    </div>

    <div v-if="loading" class="loading">
      加载中...
    </div>

    <div v-else-if="profile && profile.info.length > 0" class="info-list">
      <div
        v-for="(item, index) in profile.info"
        :key="index"
        class="info-item"
      >
        <div class="type-badge">{{ getTypeLabel(item.attribute_type) }}</div>
        <div class="content">{{ item.content }}</div>
        <div class="time">{{ item.timestamp }}</div>
      </div>
    </div>

    <div v-else class="empty">
      <span class="icon">📋</span>
      <span>暂无 {{ name }} 的信息</span>
    </div>
  </div>
</template>

<style scoped>
.profile-view {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.back-btn {
  background: transparent;
  color: #667eea;
  padding: 8px 12px;
  font-size: 24px;
}

.header h3 {
  flex: 1;
  font-size: 18px;
  margin: 0;
}

.loading,
.empty {
  padding: 40px;
  text-align: center;
  color: #999;
}

.empty .icon {
  font-size: 40px;
  display: block;
  margin-bottom: 12px;
}

.info-list {
  padding: 16px;
}

.info-item {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 10px;
  margin-bottom: 12px;
}

.info-item:last-child {
  margin-bottom: 0;
}

.type-badge {
  display: inline-block;
  padding: 4px 10px;
  background: #667eea;
  color: white;
  border-radius: 10px;
  font-size: 12px;
  margin-bottom: 8px;
}

.content {
  color: #333;
  font-size: 16px;
  line-height: 1.6;
}

.time {
  margin-top: 8px;
  font-size: 12px;
  color: #999;
}
</style>
