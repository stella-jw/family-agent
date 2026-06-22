<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'submit', content: string): void
}>()

const text = ref('')

function handleSubmit() {
  if (text.value.trim()) {
    emit('submit', text.value.trim())
    text.value = ''
  }
}
</script>

<template>
  <div class="text-input">
    <textarea
      v-model="text"
      placeholder="请输入家庭成员信息，如：我老婆叫林月，今年35岁"
      rows="4"
      @keydown.enter.ctrl="handleSubmit"
    ></textarea>
    <div class="actions">
      <span class="hint">Ctrl + Enter 发送</span>
      <button class="submit-btn" @click="handleSubmit" :disabled="!text.trim()">
        发送
      </button>
    </div>
  </div>
</template>

<style scoped>
.text-input {
  background: white;
  border-radius: 12px;
  padding: 16px;
}

textarea {
  resize: none;
  font-family: inherit;
  min-height: 100px;
}

.actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.hint {
  font-size: 12px;
  color: #999;
}

.submit-btn {
  background: #667eea;
  color: white;
  font-weight: 500;
}
</style>
