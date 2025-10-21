import axios from 'axios'
import type { WorkflowRequest, WorkflowResponse, WorkflowHistory, Agent } from '@/types'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const workflowsApi = {
  generate: async (request: WorkflowRequest): Promise<WorkflowResponse> => {
    const { data } = await api.post('/api/workflows/generate', request)
    return data
  },

  getWorkflow: async (workflowId: string): Promise<WorkflowResponse> => {
    const { data } = await api.get(`/api/workflows/${workflowId}`)
    return data
  },

  getHistory: async (limit = 20, offset = 0): Promise<WorkflowHistory[]> => {
    const { data } = await api.get('/api/workflows/', {
      params: { limit, offset },
    })
    return data
  },

  download: async (workflowId: string) => {
    const response = await api.get(`/api/workflows/${workflowId}/download`, {
      responseType: 'blob',
    })
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `${workflowId}.json`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  },

  delete: async (workflowId: string) => {
    await api.delete(`/api/workflows/${workflowId}`)
  },
}

export const agentsApi = {
  list: async (): Promise<{ agents: Agent[]; total: number }> => {
    const { data } = await api.get('/api/agents/list')
    return data
  },

  getPipeline: async () => {
    const { data } = await api.get('/api/agents/pipeline')
    return data
  },
}

export const modelsApi = {
  getTypes: async () => {
    const { data } = await api.get('/api/models/types')
    return data
  },

  getLoras: async () => {
    const { data } = await api.get('/api/models/loras')
    return data
  },

  getResolutions: async () => {
    const { data } = await api.get('/api/models/resolutions')
    return data
  },
}

export default api
