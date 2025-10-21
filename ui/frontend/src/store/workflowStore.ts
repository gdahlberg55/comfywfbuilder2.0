import { create } from 'zustand'
import type { WorkflowResponse, AgentProgress } from '@/types'

interface WorkflowStore {
  currentWorkflow: WorkflowResponse | null
  agentProgress: Map<string, AgentProgress>
  setCurrentWorkflow: (workflow: WorkflowResponse | null) => void
  updateAgentProgress: (agent: AgentProgress) => void
  clearProgress: () => void
}

export const useWorkflowStore = create<WorkflowStore>((set) => ({
  currentWorkflow: null,
  agentProgress: new Map(),

  setCurrentWorkflow: (workflow) => {
    set({ currentWorkflow: workflow })
  },

  updateAgentProgress: (agent) => {
    set((state) => {
      const newProgress = new Map(state.agentProgress)
      newProgress.set(agent.name, agent)
      return { agentProgress: newProgress }
    })
  },

  clearProgress: () => {
    set({ agentProgress: new Map() })
  },
}))
