import { ChatSection } from '@llamaindex/chat-ui'
import { useChat } from '@ai-sdk/react'
import { DefaultChatTransport } from 'ai'

export default function MyChat() {
  const handler = useChat({
    transport: new DefaultChatTransport({ api: '/api/chat' }),
  })
  return <ChatSection handler={handler} />
}