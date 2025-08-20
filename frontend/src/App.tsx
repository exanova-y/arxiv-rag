'use client'

import {
  ChatCanvas,
  ChatInput,
  ChatMessage,
  ChatMessages,
  ChatSection,
  useChatUI,
} from '@llamaindex/chat-ui'
import { UIMessage, useChat } from '@ai-sdk/react' // useChat is a hook that manages the chat state (variable)
import { DefaultChatTransport } from 'ai'

const initialMessages: UIMessage[] = [
  {
    id: '1',
    role: 'assistant',
    parts: [
      {
        type: 'text',
        text: 'Good morning! How can I help you today?',
      },
    ],
  },
  {
    id: '2',
    role: 'user',
    parts: [
      {
        type: 'text',
        text: 'gm',
      },
    ],
  },
  {
    id: '3',
    role: 'assistant',
    parts: [
      {
        type: 'text',
        text: 'How are you doing?',
      },
    ],
  },
  {
    id: '4',
    role: 'user',
    parts: [
      {
        type: 'text',
        text: 'good, thanks! what can you help me with?',
      },
    ],
  },
  {
    id: '5',
    role: 'assistant',
    parts: [
      {
        type: 'text',
        text: 'I can help you search and analyze academic papers from arXiv! Try asking me about any research topic.',
      },
    ],
  },
  {
    id: '6',
    role: 'user',
    parts: [
      {
        type: 'text',
        text: 'cool, let me test the streaming',
      },
    ],
  },
]

export default function App(): JSX.Element {
  return (
    <div className="flex h-screen flex-col">
      <header className="w-full border-b p-4 text-center">
        <h1 className="text-2xl font-bold">
          ArXiv literature search
        </h1>
        <p className="text-gray-600">
          A simple chat interface using @llamaindex/chat-ui
        </p>
      </header>
      <div className="min-h-0 flex-1">
        <ChatExample />
      </div>
    </div>
  )
}

function ChatExample() {
  const handler = useChat({
    transport: new DefaultChatTransport({
      api: 'http://localhost:8000/api/chat',
    }),
    messages: initialMessages,
    onFinish: (message) => { //This is a callback function from the useChat hook, that runs when after the AI assistant's response has been completely received from the backend stream.

      console.log('Received message:', message)
      // Auto-reply after receiving a message

      setTimeout(() => { // wait 1 sec
        handler.append({ // add user msg to chat ui. since a new user message was just added, the message is automatically sent to the backend.
          id: Date.now().toString(),
          role: 'user',
          parts: [{ type: 'text', text: 'this is an automated message' }]
        })
      }, 1000)
    }
  })

  return (
    //ChatSection wires the handler into the UI. backend -> frontend
    // ChatMessages is the scrolling list of conversation history.
    // specifically, ChatInput does frontend -> backend
    <ChatSection 
      handler={handler}
      className="block h-full flex-row gap-4 p-0 md:flex md:p-5"
    >
      <div className="md:max-w-1/2 mx-auto flex h-full min-w-0 max-w-full flex-1 flex-col gap-4">
        <ChatMessages>
          <ChatMessages.List className="px-4 py-6">
            <CustomChatMessages />
          </ChatMessages.List>
        </ChatMessages>
        <div className="border-t p-4">
          <ChatInput> 
            <ChatInput.Form>
              <ChatInput.Field placeholder="Type your message..." />
              <ChatInput.Submit />
            </ChatInput.Form>
          </ChatInput>
        </div>
      </div>
      <ChatCanvas className="w-full md:w-2/3" />
    </ChatSection>
  )
}

function CustomChatMessages() {
  const { messages } = useChatUI()

  return (
    <>
      {messages.map((message, index) => (
        <ChatMessage
          key={index}
          message={message}
          isLast={index === messages.length - 1}
          className="mb-4"
        >
          <ChatMessage.Avatar>
            <div className="flex h-8 w-8 items-center justify-center rounded-full bg-blue-500 text-sm font-semibold text-white">
              {message.role === 'user' ? 'U' : 'AI'}
            </div>
          </ChatMessage.Avatar>
          <ChatMessage.Content>
            <ChatMessage.Part.File />
            <ChatMessage.Part.Event />
            <ChatMessage.Part.Markdown />
            <ChatMessage.Part.Artifact />
            <ChatMessage.Part.Source />
            <ChatMessage.Part.Suggestion />
          </ChatMessage.Content>
          <ChatMessage.Actions />
        </ChatMessage>
      ))}
    </>
  )
}