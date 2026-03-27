const BASE_URL = 'http://localhost:7777'
const DEFAULT_TENANT = 'demo'

export const API_BASE = BASE_URL

export interface ChatMessage {
  message: string
  stream?: boolean
}

export interface ChatResponse {
  content: string
  run_id?: string
}

export async function sendChatMessage(
  message: string,
  tenantId: string = DEFAULT_TENANT,
  onChunk?: (chunk: string) => void
): Promise<string> {
  const url = `${BASE_URL}/v1/teams/jarvis-${tenantId}/runs`

  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Accept: 'text/event-stream',
    },
    body: JSON.stringify({
      message,
      stream: true,
    }),
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status} ${response.statusText}`)
  }

  const contentType = response.headers.get('content-type') || ''

  if (contentType.includes('text/event-stream')) {
    const reader = response.body?.getReader()
    if (!reader) throw new Error('No response body')

    const decoder = new TextDecoder()
    let fullContent = ''
    let buffer = ''

    while (true) {
      const { done, value } = await reader.read()
      if (done) break

      buffer += decoder.decode(value, { stream: true })
      const lines = buffer.split('\n')
      buffer = lines.pop() || ''

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6).trim()
          if (data === '[DONE]') continue
          try {
            const parsed = JSON.parse(data)
            const chunk =
              parsed.content ||
              parsed.delta?.content ||
              parsed.choices?.[0]?.delta?.content ||
              ''
            if (chunk) {
              fullContent += chunk
              onChunk?.(chunk)
            }
          } catch {
            // Non-JSON data line, skip
          }
        }
      }
    }

    return fullContent || 'Resposta recebida com sucesso.'
  } else {
    const data = await response.json()
    const content =
      data.content ||
      data.message ||
      data.response ||
      JSON.stringify(data)
    onChunk?.(content)
    return content
  }
}

export async function getSchedules() {
  const response = await fetch(`${BASE_URL}/schedules`)
  if (!response.ok) {
    throw new Error(`Failed to fetch schedules: ${response.status}`)
  }
  return response.json()
}

export async function createSchedule(schedule: Record<string, unknown>) {
  const response = await fetch(`${BASE_URL}/schedules`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(schedule),
  })
  if (!response.ok) {
    throw new Error(`Failed to create schedule: ${response.status}`)
  }
  return response.json()
}
