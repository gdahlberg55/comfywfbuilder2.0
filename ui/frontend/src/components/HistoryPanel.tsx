import { useQuery } from '@tanstack/react-query'
import { Clock, Download, Trash2 } from 'lucide-react'
import { workflowsApi } from '../services/api'
import { useWorkflowStore } from '../store/workflowStore'
import toast from 'react-hot-toast'

export default function HistoryPanel() {
  const { setCurrentWorkflow } = useWorkflowStore()

  const { data: history, isLoading, refetch } = useQuery({
    queryKey: ['workflow-history'],
    queryFn: () => workflowsApi.getHistory(20, 0),
  })

  const handleView = async (workflowId: string) => {
    try {
      const workflow = await workflowsApi.getWorkflow(workflowId)
      setCurrentWorkflow(workflow)
      toast.success('Workflow loaded')
    } catch (error) {
      toast.error('Failed to load workflow')
    }
  }

  const handleDownload = async (workflowId: string) => {
    try {
      await workflowsApi.download(workflowId)
      toast.success('Workflow downloaded')
    } catch (error) {
      toast.error('Failed to download workflow')
    }
  }

  const handleDelete = async (workflowId: string) => {
    if (!confirm('Are you sure you want to delete this workflow?')) {
      return
    }

    try {
      await workflowsApi.delete(workflowId)
      toast.success('Workflow deleted')
      refetch()
    } catch (error) {
      toast.error('Failed to delete workflow')
    }
  }

  if (isLoading) {
    return (
      <div className="card text-center py-12">
        <div className="text-gray-400">Loading history...</div>
      </div>
    )
  }

  if (!history || history.length === 0) {
    return (
      <div className="card text-center py-12">
        <div className="text-gray-400">
          <Clock className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>No workflow history yet</p>
          <p className="text-sm mt-2">
            Generated workflows will appear here
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <h3 className="text-lg font-semibold text-white mb-4">
        Workflow History
      </h3>

      <div className="space-y-3">
        {history.map((item) => (
          <div
            key={item.id}
            className="p-4 bg-gray-700/50 rounded-lg hover:bg-gray-700 transition-colors"
          >
            <div className="flex items-start justify-between gap-4">
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span
                    className={`px-2 py-0.5 text-xs rounded ${
                      item.status === 'completed'
                        ? 'bg-green-500/20 text-green-400'
                        : item.status === 'failed'
                        ? 'bg-red-500/20 text-red-400'
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}
                  >
                    {item.status}
                  </span>
                  <span className="text-xs text-gray-500">
                    {item.model_type}
                  </span>
                </div>

                <p className="text-sm text-white truncate">
                  {item.description}
                </p>

                <p className="text-xs text-gray-400 mt-1">
                  {new Date(item.created_at).toLocaleString()}
                </p>
              </div>

              <div className="flex gap-2">
                <button
                  onClick={() => handleView(item.id)}
                  className="p-2 text-gray-400 hover:text-primary-400 transition-colors"
                  title="View workflow"
                >
                  <Clock className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDownload(item.id)}
                  className="p-2 text-gray-400 hover:text-primary-400 transition-colors"
                  title="Download workflow"
                >
                  <Download className="w-4 h-4" />
                </button>
                <button
                  onClick={() => handleDelete(item.id)}
                  className="p-2 text-gray-400 hover:text-red-400 transition-colors"
                  title="Delete workflow"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
