import { ref } from 'vue'

export interface AddRequest {
  input_type: 'text' | 'file' | 'image' | 'voice'
  content: string
}

export interface AddResponse {
  success: boolean
  message: string
  added_count: number
  updated_count: number
  details: Array<{ name: string; action: string }>
}

export interface SearchRequest {
  query: string
  member_name?: string
}

export interface SearchResult {
  content: string
  member_name: string
  attribute_type: string
  timestamp: string
}

export interface SearchResponse {
  success: boolean
  results: SearchResult[]
  count: number
}

export interface MemberInfo {
  name: string
  count: number
}

export interface MembersResponse {
  members: string[]
  total: number
}

export interface ProfileResponse {
  name: string
  info: Array<{
    content: string
    attribute_type: string
    timestamp: string
  }>
}

const API_BASE = '/api'

export function useApi() {
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function request<T>(url: string, options?: RequestInit): Promise<T> {
    loading.value = true
    error.value = null

    try {
      const response = await fetch(`${API_BASE}${url}`, {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...options?.headers
        }
      })

      if (!response.ok) {
        throw new Error(`API 请求失败: ${response.status}`)
      }

      return await response.json()
    } catch (e) {
      error.value = e instanceof Error ? e.message : '未知错误'
      throw e
    } finally {
      loading.value = false
    }
  }

  async function addMember(data: AddRequest): Promise<AddResponse> {
    return request<AddResponse>('/add', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async function searchMember(data: SearchRequest): Promise<SearchResponse> {
    return request<SearchResponse>('/search', {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async function getMembers(): Promise<MembersResponse> {
    return request<MembersResponse>('/members')
  }

  async function getProfile(name: string): Promise<ProfileResponse> {
    return request<ProfileResponse>(`/profile/${encodeURIComponent(name)}`)
  }

  async function checkHealth(): Promise<{ status: string; version: string }> {
    return request<{ status: string; version: string }>('/health')
  }

  return {
    loading,
    error,
    addMember,
    searchMember,
    getMembers,
    getProfile,
    checkHealth
  }
}
