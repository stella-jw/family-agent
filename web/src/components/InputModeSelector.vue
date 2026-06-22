<script setup lang="ts">
defineProps<{
  currentMode: string
}>()

const emit = defineEmits<{
  (e: 'update:currentMode', mode: string): void
}>()

const modes = [
  { id: 'text', label: '文本', icon: '💬' },
  { id: 'file', label: '文件', icon: '📄' },
  { id: 'image', label: '图片', icon: '🖼️' },
  { id: 'voice', label: '语音', icon: '🎤' }
]
</script>

<template>
  <div class="mode-selector">
    <button
      v-for="mode in modes"
      :key="mode.id"
      :class="['mode-btn', { active: currentMode === mode.id }]"
      @click="emit('update:currentMode', mode.id)"
    >
      <span class="icon">{{ mode.icon }}</span>
      <span class="label">{{ mode.label }}</span>
    </button>
  </div>
</template>

<style scoped>
.mode-selector {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.mode-btn {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  padding: 16px 12px;
  background: white;
  color: #333;
  border: 2px solid transparent;
}

.mode-btn.active {
  border-color: #667eea;
  background: #f0f3ff;
}

.icon {
  font-size: 24px;
}

.label {
  font-size: 14px;
  font-weight: 500;
}

@media (max-width: 480px) {
  .mode-selector {
    gap: 8px;
  }

  .mode-btn {
    padding: 12px 8px;
  }

  .icon {
    font-size: 20px;
  }

  .label {
    font-size: 12px;
  }
}
</style>
