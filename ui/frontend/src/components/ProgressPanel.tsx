import { useEffect } from 'react'
import { CheckCircle2, Circle, Loader2, XCircle } from 'lucide-react'
import { websocketService } from '../services/websocket'
import { useWorkflowStore } from '../store/workflowStore'
import type { AgentStatus } from '../types'

const AGENT_PIPELINE = [
  { name: 'parameter-extractor', label: 'Parameter Extraction' },
  { name: 'asset-finder', label: 'Asset Discovery' },
  { name: 'prompt-crafter', label: 'Prompt Optimization' },
  { name: 'workflow-architect', label: 'Workflow Design' },
  { name: 'node-curator', label: 'Node Selection' },
  { name: 'graph-engineer', label: 'Connection Wiring' },
  { name: 'graph-analyzer', label: 'Graph Analysis' },
  { name: 'layout-strategist', label: 'Layout Planning' },
  { name: 'reroute-engineer', label: 'Route Optimization' },
  { name: 'layout-refiner', label: 'Layout Refinement' },
  { name: 'group-coordinator', label: 'Group Organization' },
  { name: 'nomenclature-specialist', label: 'Naming Convention' },
  { name: 'workflow-validator', label: 'Validation' },
  { name: 'workflow-serializer', label: 'Serialization' },
]

const StatusIcon = ({ status }: { status?: AgentStatus }) => {
  switch (status) {
    case 'running':
      return <Loader2 className="w-4 h-4 text-primary-500 animate-spin" />
    case 'completed':
      return <CheckCircle2 className="w-4 h-4 text-green-500" />
    case 'failed':
      return <XCircle className="w-4 h-4 text-red-500" />
    default:
      return <Circle className="w-4 h-4 text-gray-600" />
  }
}

export default function ProgressPanel() {
  const { agentProgress, updateAgentProgress } = useWorkflowStore()

  useEffect(() => {
    const unsubscribe = websocketService.subscribe((message) => {
      if (message.type === 'agent_progress' && message.agent) {
        updateAgentProgress({
          name: message.agent,
          status: message.status as AgentStatus,
          message: message.message,
        })
      }
    })

    return unsubscribe
  }, [updateAgentProgress])

  const hasProgress = agentProgress.size > 0

  if (!hasProgress) {
    return null
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-white mb-4">
        Generation Progress
      </h3>

      <div className="space-y-2">
        {AGENT_PIPELINE.map((agent) => {
          const progress = agentProgress.get(agent.name)
          const status = progress?.status || 'pending'

          return (
            <div
              key={agent.name}
              className="flex items-center gap-3 p-2 rounded-lg bg-gray-700/50"
            >
              <StatusIcon status={status} />
              <div className="flex-1">
                <div className="text-sm font-medium text-white">
                  {agent.label}
                </div>
                {progress?.message && (
                  <div className="text-xs text-gray-400">{progress.message}</div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
