import { useState } from 'react'
import WorkflowForm from '../components/WorkflowForm'
import ProgressPanel from '../components/ProgressPanel'
import WorkflowViewer from '../components/WorkflowViewer'
import HistoryPanel from '../components/HistoryPanel'
import { useWorkflowStore } from '../store/workflowStore'

export default function WorkflowBuilder() {
  const [activeTab, setActiveTab] = useState<'viewer' | 'history'>('viewer')
  const { currentWorkflow } = useWorkflowStore()

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Left Column - Input Form */}
      <div className="lg:col-span-1">
        <WorkflowForm />
      </div>

      {/* Right Column - Output */}
      <div className="lg:col-span-2 space-y-6">
        {/* Progress Panel */}
        <ProgressPanel />

        {/* Tab Navigation */}
        <div className="flex gap-2 border-b border-gray-700">
          <button
            onClick={() => setActiveTab('viewer')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'viewer'
                ? 'text-primary-500 border-b-2 border-primary-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            Workflow Viewer
          </button>
          <button
            onClick={() => setActiveTab('history')}
            className={`px-4 py-2 font-medium transition-colors ${
              activeTab === 'history'
                ? 'text-primary-500 border-b-2 border-primary-500'
                : 'text-gray-400 hover:text-gray-300'
            }`}
          >
            History
          </button>
        </div>

        {/* Content */}
        {activeTab === 'viewer' ? (
          <WorkflowViewer workflow={currentWorkflow} />
        ) : (
          <HistoryPanel />
        )}
      </div>
    </div>
  )
}
