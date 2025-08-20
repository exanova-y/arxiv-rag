import { useState } from 'react'
import { ChatSection } from '@llamaindex/chat-ui'
import { useChat } from '@ai-sdk/react'
import './App.css'

function App() {
  const ChatExample = () => {
    const handler = useChat()
    return <ChatSection handler={handler} />
  }
  return (
    <>
      <div>
        <ChatExample />
      </div> 
    </>
  )
}

export default App
