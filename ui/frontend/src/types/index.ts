export type ModelType = 'flux' | 'sdxl' | 'pony' | 'sd1.5'

export type WorkflowStatus = 'pending' | 'processing' | 'completed' | 'failed'

export type AgentStatus = 'pending' | 'running' | 'completed' | 'failed'

export interface WorkflowRequest {
  description: string
  model_type?: ModelType
  width?: number
  height?: number
  steps?: number
  include_upscale?: boolean
  include_adetailer?: boolean
  lora_models?: string[]
  custom_options?: Record<string, any>
}

export interface AgentProgress {
  name: string
  status: AgentStatus
  message?: string
  started_at?: string
  completed_at?: string
  error?: string
}

export interface WorkflowResponse {
  id: string
  status: WorkflowStatus
  workflow_json?: any
  agent_progress: AgentProgress[]
  created_at: string
  completed_at?: string
  error?: string
  metadata: Record<string, any>
}

export interface WorkflowHistory {
  id: string
  description: string
  model_type: ModelType
  status: WorkflowStatus
  created_at: string
  preview_url?: string
}

export interface Agent {
  name: string
  description: string
  category: string
}

export interface WebSocketMessage {
  type: string
  workflow_id?: string
  agent?: string
  status?: string
  message?: string
  timestamp?: string
  error?: string
}
