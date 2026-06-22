<script setup lang="ts">
import { ref, computed } from 'vue'

const emit = defineEmits<{
  (e: 'submit', content: string): void
}>()

const file = ref<File | null>(null)
const preview = ref('')
const error = ref('')
const MAX_SIZE = 10 * 1024 * 1024 // 10MB

function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  const selectedFile = input.files[0]
  error.value = ''

  // Validate size
  if (selectedFile.size > MAX_SIZE) {
    error.value = '文件过大，最大支持 10MB'
    return
  }

  // Validate type
  const ext = selectedFile.name.split('.').pop()?.toLowerCase()
  if (!['json', 'csv', 'txt'].includes(ext || '')) {
    error.value = '不支持的文件格式，请上传 JSON、CSV 或 TXT 文件'
    return
  }

  file.value = selectedFile

  // Read file content
  const reader = new FileReader()
  reader.onload = (e) => {
    preview.value = e.target?.result as string
  }
  reader.readAsText(selectedFile)
}

function handleSubmit() {
  if (preview.value) {
    emit('submit', preview.value)
    // Reset
    file.value = null
    preview.value = ''
  }
}

const fileType = computed(() => {
  if (!file.value) return ''
  return file.value.name.split('.').pop()?.toUpperCase() || ''
})
</script>

<template>
  <div class="file-upload">
    <div class="upload-area">
      <input
        type="file"
        accept=".json,.csv,.txt"
        @change="handleFileSelect"
        id="file-input"
      />
      <label for="file-input" class="upload-label">
        <span class="icon">📄</span>
        <span class="text">点击选择文件</span>
        <span class="hint">支持 JSON、CSV、TXT（最大 10MB）</span>
      </label>
    </div>

    <div v-if="file" class="preview">
      <div class="file-info">
        <span class="file-name">{{ file.name }}</span>
        <span class="file-type">{{ fileType }}</span>
      </div>
      <pre class="content-preview">{{ preview.substring(0, 500) }}{{ preview.length > 500 ? '...' : '' }}</pre>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <button
      v-if="preview"
      class="submit-btn"
      @click="handleSubmit"
    >
      上传文件
    </button>
  </div>
</template>

<style scoped>
.file-upload {
  background: white;
  border-radius: 12px;
  padding: 16px;
}

.upload-area input {
  display: none;
}

.upload-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 40px 20px;
  border: 2px dashed #ddd;
  border-radius: 12px;
  cursor: pointer;
  transition: border-color 0.2s;
}

.upload-label:hover {
  border-color: #667eea;
}

.icon {
  font-size: 40px;
}

.text {
  font-size: 16px;
  font-weight: 500;
  color: #333;
}

.hint {
  font-size: 12px;
  color: #999;
}

.preview {
  margin-top: 16px;
  padding: 12px;
  background: #f5f5f5;
  border-radius: 8px;
}

.file-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.file-name {
  font-weight: 500;
}

.file-type {
  background: #667eea;
  color: white;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}

.content-preview {
  font-size: 12px;
  color: #666;
  white-space: pre-wrap;
  word-break: break-all;
  max-height: 150px;
  overflow-y: auto;
}

.error {
  margin-top: 12px;
  padding: 12px;
  background: #fee;
  color: #c00;
  border-radius: 8px;
  font-size: 14px;
}

.submit-btn {
  width: 100%;
  margin-top: 16px;
  background: #667eea;
  color: white;
  font-weight: 500;
  padding: 14px;
}
</style>
