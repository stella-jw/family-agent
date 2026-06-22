<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useApi, type MembersResponse } from '../composables/useApi'

const emit = defineEmits<{
  (e: 'select', name: string): void
}>()

const { getMembers, loading } = useApi()
const members = ref<MembersResponse | null>(null)

onMounted(async () => {
  try {
    members.value = await getMembers()
  } catch (e) {
    console.error('Failed to load members:', e)
  }
})
</script>

<template>
  <div class="members-list">
    <div class="header">
      <h3>👨‍👩‍👧‍👦 家庭成员</h3>
      <span v-if="members" class="count">{{ members.total }} 人</span>
    </div>

    <div v-if="loading" class="loading">
      加载中...
    </div>

    <div v-else-if="members && members.members.length > 0" class="list">
      <button
        v-for="member in members.members"
        :key="member"
        class="member-item"
        @click="emit('select', member)"
      >
        <span class="avatar">{{ member.charAt(0) }}</span>
        <span class="name">{{ member }}</span>
        <span class="arrow">›</span>
      </button>
    </div>

    <div v-else class="empty">
      <span class="icon">🏠</span>
      <span>暂无成员记录</span>
    </div>
  </div>
</template>

<style scoped>
.members-list {
  background: white;
  border-radius: 12px;
  overflow: hidden;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #eee;
}

.header h3 {
  font-size: 16px;
  margin: 0;
}

.count {
  background: #667eea;
  color: white;
  padding: 2px 10px;
  border-radius: 10px;
  font-size: 12px;
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

.list {
  padding: 8px;
}

.member-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: transparent;
  border-radius: 8px;
  text-align: left;
}

.member-item:hover {
  background: #f5f5f5;
}

.avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 500;
}

.name {
  flex: 1;
  font-size: 16px;
  color: #333;
}

.arrow {
  font-size: 20px;
  color: #ccc;
}
</style>
