<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{
  (e: 'submit', content: string): void
}>()

type RecordingState = 'idle' | 'recording' | 'recorded'

const state = ref<RecordingState>('idle')
const audioUrl = ref('')
const error = ref('')
const duration = ref(0)
let mediaRecorder: MediaRecorder | null = null
let audioBlob: Blob | null = null
let timer: number | null = null
const MAX_DURATION = 30 // seconds

async function startRecording() {
  error.value = ''

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    mediaRecorder = new MediaRecorder(stream)
    audioBlob = null
    duration.value = 0

    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) {
        audioBlob = e.data
        audioUrl.value = URL.createObjectURL(e.data)
      }
    }

    mediaRecorder.onstop = () => {
      state.value = 'recorded'
      stream.getTracks().forEach(track => track.stop())
      if (timer) {
        clearInterval(timer)
        timer = null
      }
    }

    mediaRecorder.start()
    state.value = 'recording'

    // Start timer
    timer = window.setInterval(() => {
      duration.value++
      if (duration.value >= MAX_DURATION) {
        stopRecording()
      }
    }, 1000)

  } catch (e) {
    if (e instanceof Error && e.name === 'NotAllowedError') {
      error.value = '麦克风权限被拒绝，请在浏览器设置中允许使用麦克风'
    } else {
      error.value = '无法访问麦克风，请检查设备设置'
    }
  }
}

function stopRecording() {
  if (mediaRecorder && mediaRecorder.state === 'recording') {
    mediaRecorder.stop()
  }
}

function playAudio() {
  if (audioUrl.value) {
    const audio = new Audio(audioUrl.value)
    audio.play()
  }
}

function reset() {
  state.value = 'idle'
  audioUrl.value = ''
  audioBlob = null
  duration.value = 0
}

async function handleSubmit() {
  if (!audioBlob) return

  // Convert to base64
  const base64 = await blobToBase64(audioBlob)
  emit('submit', base64)
  reset()
}

function blobToBase64(blob: Blob): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => {
      const result = reader.result as string
      // Remove data URL prefix for API
      resolve(result.split(',')[1])
    }
    reader.onerror = reject
    reader.readAsDataURL(blob)
  })
}

function formatTime(seconds: number): string {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}
</script>

<template>
  <div class="voice-record">
    <div class="recorder">
      <!-- Idle state -->
      <div v-if="state === 'idle'" class="idle-state">
        <button class="record-btn" @click="startRecording">
          <span class="icon">🎤</span>
          <span class="text">开始录音</span>
        </button>
        <p class="hint">点击按钮开始录音，最长 30 秒</p>
      </div>

      <!-- Recording state -->
      <div v-if="state === 'recording'" class="recording-state">
        <div class="recording-indicator">
          <span class="dot"></span>
          <span class="time">{{ formatTime(duration) }} / {{ formatTime(MAX_DURATION) }}</span>
        </div>
        <button class="stop-btn" @click="stopRecording">
          <span class="icon">⏹️</span>
          <span class="text">停止录音</span>
        </button>
      </div>

      <!-- Recorded state -->
      <div v-if="state === 'recorded'" class="recorded-state">
        <div class="audio-preview">
          <audio :src="audioUrl" controls></audio>
        </div>
        <div class="actions">
          <button class="reset-btn" @click="reset">重新录音</button>
          <button class="submit-btn" @click="handleSubmit">发送</button>
        </div>
      </div>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
  </div>
</template>

<style scoped>
.voice-record {
  background: white;
  border-radius: 12px;
  padding: 16px;
}

.recorder {
  min-height: 150px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.idle-state,
.recording-state,
.recorded-state {
  width: 100%;
  text-align: center;
}

.record-btn,
.stop-btn {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 24px 40px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  width: 120px;
  height: 120px;
  border-radius: 60px;
}

.record-btn .icon,
.stop-btn .icon {
  font-size: 32px;
}

.record-btn .text,
.stop-btn .text {
  font-size: 14px;
  font-weight: 500;
}

.hint {
  margin-top: 16px;
  font-size: 14px;
  color: #999;
}

.recording-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.dot {
  width: 20px;
  height: 20px;
  background: #f00;
  border-radius: 50%;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.time {
  font-size: 24px;
  font-weight: 500;
  color: #333;
}

.audio-preview {
  margin-bottom: 16px;
}

.audio-preview audio {
  width: 100%;
  height: 40px;
}

.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
}

.reset-btn {
  background: #eee;
  color: #666;
}

.submit-btn {
  background: #667eea;
  color: white;
  flex: 1;
  max-width: 200px;
}

.error {
  margin-top: 12px;
  padding: 12px;
  background: #fee;
  color: #c00;
  border-radius: 8px;
  font-size: 14px;
}
</style>
