<script setup lang="ts">
import { ref } from 'vue'
import InputModeSelector from './components/InputModeSelector.vue'
import TextInput from './components/TextInput.vue'
import FileUpload from './components/FileUpload.vue'
import ImageUpload from './components/ImageUpload.vue'
import VoiceRecord from './components/VoiceRecord.vue'
import ResponseDisplay from './components/ResponseDisplay.vue'
import MembersList from './components/MembersList.vue'
import ProfileView from './components/ProfileView.vue'
import { useApi, type AddResponse, type SearchResult } from './composables/useApi'

const { addMember, searchMember, loading } = useApi()

type ViewState = 'main' | 'members' | 'profile'

const currentView = ref<ViewState>('main')
const selectedMember = ref('')
const currentMode = ref('text')
const response = ref<AddResponse | null>(null)
const searchResults = ref<SearchResult[]>([])
const searchMode = ref(false)

async function handleSubmit(content: string) {
  searchMode.value = false
  response.value = null

  try {
    const result = await addMember({
      input_type: currentMode.value as 'text' | 'file' | 'image' | 'voice',
      content
    })
    response.value = result
  } catch (e) {
    response.value = {
      success: false,
      message: e instanceof Error ? e.message : '请求失败',
      added_count: 0,
      updated_count: 0,
      details: []
    }
  }
}

async function handleSearch(query: string) {
  searchMode.value = true
  response.value = null
  searchResults.value = []

  try {
    const result = await searchMember({ query })
    searchResults.value = result.results
  } catch (e) {
    console.error('Search failed:', e)
  }
}

function showMembers() {
  currentView.value = 'members'
  response.value = null
  searchResults.value = []
}

function showMemberProfile(name: string) {
  selectedMember.value = name
  currentView.value = 'profile'
  response.value = null
}

function goBack() {
  currentView.value = 'members'
  selectedMember.value = ''
}
</script>

<template>
  <div class="app">
    <header class="header">
      <h1>🏠 家庭信息记录</h1>
      <p class="subtitle">记录您家庭成员的点点滴滴</p>
    </header>

    <main class="main">
      <!-- Main input view -->
      <template v-if="currentView === 'main'">
        <InputModeSelector v-model:current-mode="currentMode" />

        <div class="input-panel">
          <TextInput
            v-if="currentMode === 'text'"
            @submit="handleSubmit"
          />
          <FileUpload
            v-else-if="currentMode === 'file'"
            @submit="handleSubmit"
          />
          <ImageUpload
            v-else-if="currentMode === 'image'"
            @submit="handleSubmit"
          />
          <VoiceRecord
            v-else-if="currentMode === 'voice'"
            @submit="handleSubmit"
          />
        </div>

        <div v-if="loading" class="loading">
          <span class="spinner"></span>
          <span>处理中...</span>
        </div>

        <ResponseDisplay
          v-if="!loading"
          :response="response"
          :search-results="searchResults"
          :search-mode="searchMode"
        />
      </template>

      <!-- Members list view -->
      <MembersList
        v-else-if="currentView === 'members'"
        @select="showMemberProfile"
      />

      <!-- Profile view -->
      <ProfileView
        v-else-if="currentView === 'profile'"
        :name="selectedMember"
        @back="goBack"
      />
    </main>

    <footer class="footer">
      <button class="action-btn" @click="currentView = 'main'">
        ✏️ 录入
      </button>
      <button class="action-btn" @click="showMembers">
        👥 成员
      </button>
      <button class="action-btn" @click="handleSearch('')">
        🔍 搜索
      </button>
    </footer>
  </div>
</template>

<style scoped>
.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.header {
  text-align: center;
  padding: 30px 20px;
  color: white;
}

.header h1 {
  font-size: 28px;
  margin-bottom: 8px;
}

.subtitle {
  font-size: 14px;
  opacity: 0.9;
}

.main {
  flex: 1;
  padding: 0 20px 20px;
}

.input-panel {
  margin-bottom: 20px;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  color: #666;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #ddd;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.footer {
  padding: 16px 20px;
  background: rgba(255, 255, 255, 0.1);
  display: flex;
  gap: 12px;
}

.action-btn {
  flex: 1;
  background: white;
  color: #667eea;
  font-weight: 600;
  padding: 14px;
}

@media (max-width: 768px) {
  .header h1 {
    font-size: 24px;
  }
}
</style>
