import { useState, useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import WorkflowBuilder from './pages/WorkflowBuilder'
import { websocketService } from './services/websocket'
import Header from './components/Header'

function App() {
  useEffect(() => {
    // Connect WebSocket on mount
    websocketService.connect()

    // Cleanup on unmount
    return () => {
      websocketService.disconnect()
    }
  }, [])

  return (
    <div className="min-h-screen bg-gray-900">
      <Header />
      <main className="container mx-auto px-4 py-8">
        <WorkflowBuilder />
      </main>
      <Toaster position="bottom-right" />
    </div>
  )
}

export default App
