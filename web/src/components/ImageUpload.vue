<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'submit', content: string): void
}>()

const file = ref<File | null>(null)
const preview = ref('')
const error = ref('')
const MAX_SIZE = 10 * 1024 * 1024 // 10MB
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp']

function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement
  if (!input.files?.length) return

  const selectedFile = input.files[0]
  error.value = ''

  // Validate size
  if (selectedFile.size > MAX_SIZE) {
    error.value = '图片过大，最大支持 10MB'
    return
  }

  // Validate type
  if (!ALLOWED_TYPES.includes(selectedFile.type)) {
    error.value = '不支持的图片格式，请上传 JPEG、PNG 或 WebP'
    return
  }

  file.value = selectedFile

  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    preview.value = e.target?.result as string
  }
  reader.readAsDataURL(selectedFile)
}

async function handleSubmit() {
  if (!file.value) return

  // Convert to base64
  const base64 = await fileToBase64(file.value)
  emit('submit', base64)

  // Reset
  file.value = null
  preview.value = ''
}

function fileToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result as string)
    reader.onerror = reject
    reader.readAsDataURL(file)
  })
}
</script>

<template>
  <div class="image-upload">
    <div class="upload-area">
      <input
        type="file"
        accept="image/jpeg,image/png,image/webp"
        @change="handleFileSelect"
        id="image-input"
      />
      <label for="image-input" class="upload-label">
        <span class="icon">🖼️</span>
        <span class="text">点击选择图片</span>
        <span class="hint">支持 JPEG、PNG、WebP（最大 10MB）</span>
      </label>
    </div>

    <div v-if="preview" class="preview">
      <img :src="preview" alt="预览" />
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <button
      v-if="preview"
      class="submit-btn"
      @click="handleSubmit"
    >
      上传图片
    </button>
  </div>
</template>

<style scoped>
.image-upload {
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
  text-align: center;
}

.preview img {
  max-width: 100%;
  max-height: 300px;
  border-radius: 8px;
  object-fit: contain;
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
