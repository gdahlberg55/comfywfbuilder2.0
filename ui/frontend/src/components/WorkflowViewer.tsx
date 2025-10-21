import { useState } from 'react'
import { Download, Code2, Eye } from 'lucide-react'
import Editor from '@monaco-editor/react'
import toast from 'react-hot-toast'
import { workflowsApi } from '../services/api'
import type { WorkflowResponse } from '../types'

interface Props {
  workflow: WorkflowResponse | null
}

export default function WorkflowViewer({ workflow }: Props) {
  const [viewMode, setViewMode] = useState<'json' | 'visual'>('json')

  const handleDownload = async () => {
    if (!workflow?.id) return

    try {
      await workflowsApi.download(workflow.id)
      toast.success('Workflow downloaded!')
    } catch (error) {
      toast.error('Failed to download workflow')
    }
  }

  if (!workflow) {
    return (
      <div className="card text-center py-12">
        <div className="text-gray-400">
          <Eye className="w-12 h-12 mx-auto mb-3 opacity-50" />
          <p>No workflow generated yet</p>
          <p className="text-sm mt-2">
            Enter a description and click "Generate Workflow" to get started
          </p>
        </div>
      </div>
    )
  }

  if (workflow.status === 'processing') {
    return (
      <div className="card text-center py-12">
        <div className="text-gray-400">
          <div className="animate-pulse">
            <Code2 className="w-12 h-12 mx-auto mb-3" />
            <p>Generating workflow...</p>
            <p className="text-sm mt-2">Please wait while the agents work their magic</p>
          </div>
        </div>
      </div>
    )
  }

  if (workflow.status === 'failed') {
    return (
      <div className="card">
        <div className="text-red-400">
          <h3 className="text-lg font-semibold mb-2">Generation Failed</h3>
          <p className="text-sm">{workflow.error || 'Unknown error occurred'}</p>
        </div>
      </div>
    )
  }

  if (!workflow.workflow_json) {
    return (
      <div className="card text-center py-12">
        <div className="text-gray-400">
          <p>Workflow data not available</p>
        </div>
      </div>
    )
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-white">Workflow Output</h3>

        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('json')}
            className={`px-3 py-1 rounded text-sm ${
              viewMode === 'json'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-700 text-gray-300'
            }`}
          >
            JSON
          </button>
          <button
            onClick={() => setViewMode('visual')}
            className={`px-3 py-1 rounded text-sm ${
              viewMode === 'visual'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-700 text-gray-300'
            }`}
          >
            Visual
          </button>
          <button onClick={handleDownload} className="btn-primary flex items-center gap-2">
            <Download className="w-4 h-4" />
            Download
          </button>
        </div>
      </div>

      {viewMode === 'json' ? (
        <div className="h-[600px] border border-gray-700 rounded-lg overflow-hidden">
          <Editor
            height="100%"
            defaultLanguage="json"
            value={JSON.stringify(workflow.workflow_json, null, 2)}
            theme="vs-dark"
            options={{
              readOnly: true,
              minimap: { enabled: false },
              fontSize: 13,
            }}
          />
        </div>
      ) : (
        <div className="h-[600px] border border-gray-700 rounded-lg flex items-center justify-center">
          <div className="text-gray-400 text-center">
            <Eye className="w-12 h-12 mx-auto mb-3 opacity-50" />
            <p>Visual workflow preview coming soon</p>
            <p className="text-sm mt-2">
              For now, use the JSON view or download the workflow
            </p>
          </div>
        </div>
      )}

      {/* Metadata */}
      <div className="mt-4 pt-4 border-t border-gray-700 text-sm text-gray-400">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <strong>Workflow ID:</strong> {workflow.id}
          </div>
          <div>
            <strong>Created:</strong>{' '}
            {new Date(workflow.created_at).toLocaleString()}
          </div>
          <div>
            <strong>Model Type:</strong> {workflow.metadata.model_type}
          </div>
          <div>
            <strong>Dimensions:</strong> {workflow.metadata.dimensions}
          </div>
        </div>
      </div>
    </div>
  )
}
