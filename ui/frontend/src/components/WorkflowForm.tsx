import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Sparkles, Settings2 } from 'lucide-react'
import toast from 'react-hot-toast'
import { workflowsApi } from '../services/api'
import type { WorkflowRequest, ModelType } from '../types'
import { useWorkflowStore } from '../store/workflowStore'

export default function WorkflowForm() {
  const [description, setDescription] = useState('')
  const [modelType, setModelType] = useState<ModelType>('flux')
  const [width, setWidth] = useState(1024)
  const [height, setHeight] = useState(1024)
  const [steps, setSteps] = useState(30)
  const [includeUpscale, setIncludeUpscale] = useState(true)
  const [includeAdetailer, setIncludeAdetailer] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)

  const { setCurrentWorkflow, clearProgress } = useWorkflowStore()

  const generateMutation = useMutation({
    mutationFn: (request: WorkflowRequest) => workflowsApi.generate(request),
    onSuccess: (data) => {
      setCurrentWorkflow(data)
      toast.success('Workflow generation started!')
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to generate workflow')
    },
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!description.trim()) {
      toast.error('Please enter a workflow description')
      return
    }

    clearProgress()

    const request: WorkflowRequest = {
      description: description.trim(),
      model_type: modelType,
      width,
      height,
      steps,
      include_upscale: includeUpscale,
      include_adetailer: includeAdetailer,
    }

    generateMutation.mutate(request)
  }

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-white mb-4 flex items-center gap-2">
        <Sparkles className="w-5 h-5 text-primary-500" />
        Workflow Configuration
      </h2>

      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Description */}
        <div>
          <label className="label">Workflow Description</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="input min-h-[120px]"
            placeholder="Describe your desired workflow in natural language...&#10;&#10;Example: Create a Flux workflow with LoRA support, 2-pass upscaling, and ADetailer for face enhancement"
          />
        </div>

        {/* Model Type */}
        <div>
          <label className="label">Model Type</label>
          <select
            value={modelType}
            onChange={(e) => setModelType(e.target.value as ModelType)}
            className="input"
          >
            <option value="flux">Flux</option>
            <option value="sdxl">SDXL</option>
            <option value="pony">Pony</option>
            <option value="sd1.5">SD 1.5</option>
          </select>
        </div>

        {/* Resolution */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="label">Width</label>
            <input
              type="number"
              value={width}
              onChange={(e) => setWidth(Number(e.target.value))}
              className="input"
              step="64"
            />
          </div>
          <div>
            <label className="label">Height</label>
            <input
              type="number"
              value={height}
              onChange={(e) => setHeight(Number(e.target.value))}
              className="input"
              step="64"
            />
          </div>
        </div>

        {/* Advanced Options */}
        <button
          type="button"
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="flex items-center gap-2 text-sm text-gray-400 hover:text-gray-300"
        >
          <Settings2 className="w-4 h-4" />
          {showAdvanced ? 'Hide' : 'Show'} Advanced Options
        </button>

        {showAdvanced && (
          <div className="space-y-4 pt-4 border-t border-gray-700">
            <div>
              <label className="label">Sampling Steps</label>
              <input
                type="number"
                value={steps}
                onChange={(e) => setSteps(Number(e.target.value))}
                className="input"
              />
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="upscale"
                checked={includeUpscale}
                onChange={(e) => setIncludeUpscale(e.target.checked)}
                className="w-4 h-4"
              />
              <label htmlFor="upscale" className="text-sm text-gray-300">
                Include Upscaling Pass
              </label>
            </div>

            <div className="flex items-center gap-2">
              <input
                type="checkbox"
                id="adetailer"
                checked={includeAdetailer}
                onChange={(e) => setIncludeAdetailer(e.target.checked)}
                className="w-4 h-4"
              />
              <label htmlFor="adetailer" className="text-sm text-gray-300">
                Include ADetailer
              </label>
            </div>
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={generateMutation.isPending}
          className="btn-primary w-full"
        >
          {generateMutation.isPending ? 'Generating...' : 'Generate Workflow'}
        </button>
      </form>

      {/* Example Prompts */}
      <div className="mt-6 pt-6 border-t border-gray-700">
        <p className="text-sm text-gray-400 mb-2">Example prompts:</p>
        <div className="space-y-2">
          {[
            'Create a Flux workflow with LoRA support and 2-pass upscaling',
            'Build a SDXL workflow with ADetailer for face enhancement',
            'Generate a Pony workflow with wildcards and multi-pass rendering',
          ].map((example, i) => (
            <button
              key={i}
              type="button"
              onClick={() => setDescription(example)}
              className="text-xs text-primary-400 hover:text-primary-300 block"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
