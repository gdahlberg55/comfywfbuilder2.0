import type { WebSocketMessage } from '@/types'

class WebSocketService {
  private ws: WebSocket | null = null
  private listeners: Set<(message: WebSocketMessage) => void> = new Set()
  private reconnectTimeout: number | null = null
  private reconnectDelay = 1000

  connect() {
    const wsUrl = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/progress'

    this.ws = new WebSocket(wsUrl)

    this.ws.onopen = () => {
      console.log('WebSocket connected')
      this.reconnectDelay = 1000
    }

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data) as WebSocketMessage
        this.listeners.forEach((listener) => listener(message))
      } catch (error) {
        console.error('Failed to parse WebSocket message:', error)
      }
    }

    this.ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }

    this.ws.onclose = () => {
      console.log('WebSocket disconnected')
      this.reconnect()
    }
  }

  private reconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout)
    }

    this.reconnectTimeout = window.setTimeout(() => {
      console.log('Attempting to reconnect WebSocket...')
      this.connect()
      this.reconnectDelay = Math.min(this.reconnectDelay * 2, 30000)
    }, this.reconnectDelay)
  }

  disconnect() {
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout)
    }

    if (this.ws) {
      this.ws.close()
      this.ws = null
    }
  }

  subscribe(callback: (message: WebSocketMessage) => void) {
    this.listeners.add(callback)

    // Return unsubscribe function
    return () => {
      this.listeners.delete(callback)
    }
  }

  send(message: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(message))
    }
  }
}

export const websocketService = new WebSocketService()
