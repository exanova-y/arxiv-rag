import { useState } from 'react'
import { ChatSection } from '@llamaindex/chat-ui'
import { useChat } from '@ai-sdk/react' // useChat hook from vercel/ai
import MyChat from './myChat'
import './App.css'


function App() {
  return (
    <div>
      <MyChat />
    </div>
  )
}

export default App;