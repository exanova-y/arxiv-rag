import { ChatCanvas, useChatCanvas } from '@llamaindex/chat-ui'

function CustomCanvas({ className }: { className?: string }) {
  const { currentArtifact, isVisible, hideCanvas } = useChatCanvas()
  
  if (!isVisible || !currentArtifact) return null
  
  return (
    <div className={`w-full max-w-4xl mx-auto bg-gray-50 border rounded-lg flex flex-col ${className || ''}`}>
      {/* Custom header */}
      <div className="flex items-center justify-between p-4 border-b bg-white">
        <div>
          <h2 className="font-semibold text-gray-900">
            {currentArtifact.title}
          </h2>
          <p className="text-sm text-gray-500">
            {currentArtifact.type === 'code' ? 'Code Editor' : 'Document'}
          </p>
        </div>
        
        <div className="flex items-center gap-2">
          <CustomCanvasActions />
          <button
            onClick={hideCanvas}
            className="p-1 hover:bg-gray-100 rounded"
          >
            <XIcon className="h-5 w-5" />
          </button>
        </div>
      </div>
      
      {/* Custom content area */}
      <div className="flex-1 overflow-hidden p-4">
        <div className="w-full max-w-6xl mx-auto h-full">
          <ChatCanvas className="h-full w-full">
            {/* Canvas content renders here */}
          </ChatCanvas>
        </div>
      </div>
      
      {/* Custom footer */}
      <div className="border-t bg-white p-3">
        <div className="flex items-center justify-between text-sm text-gray-500">
          <span>
            {currentArtifact.type === 'code' 
              ? `${currentArtifact.language} • ${currentArtifact.file_name}`
              : 'Markdown Document'
            }
          </span>
          <span>
            Last modified: {new Date().toLocaleTimeString()}
          </span>
        </div>
      </div>
    </div>
  )
}

export default CustomCanvas