// components/chatbot/chat-dialog.tsx
"use client"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Send, Loader2 } from "lucide-react"
import { ChatMessage } from "./chat-message"
import { Message } from "@/lib/interface"

// Props for the ChatDialog component
interface ChatDialogProps {
  url: string
  onClose: () => void
}

export function ChatDialog({ url, onClose }: ChatDialogProps) {
  // State to manage chat messages
  const [messages, setMessages] = useState<Message[]>([
    {
      id: (Date.now()).toString(), // Added id for the initial message
      content: "Hi there! How can I help you today?",
      role: "assistant" // Added role for the initial message
    }
  ])
  
  // State to manage user input and loading status
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null) // Added inputRef for the input field

  useEffect(() => {
    // Focus on the input field when the component mounts
    inputRef.current?.focus()
  }, [])

  useEffect(() => {
    // Scroll to bottom when messages change
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" })
    }
  }, [messages])

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Prevent submission if input is empty or loading
    if (isLoading || !input.trim()) return;

    // Create user message object
    const userMessage: Message = {
      id: (Date.now() + 1).toString(), // Unique id for the user message
      content: input,
      role: "user"
    }

    // Update messages state with user message
    setMessages(prev => [...prev, userMessage])
    setInput("") // Clear input field
    setIsLoading(true) // Set loading state

    try {
      // Send user message to the chat API
      const response = await fetch("/api/chat", { // Updated API endpoint
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ url: url, query: input }) // Send the user input
      })
      
      if (!response.ok) {
        throw new Error("Failed to get response")
      }
      
      const data = await response.json()
      
      // Create assistant message object
      const assistantMessage: Message = {
        id: (Date.now() + 2).toString(), // Unique id for the assistant message
        content: data.data.response,
        role: "assistant"
      }
      
      // Update messages state with assistant message
      setMessages(prev => [...prev, assistantMessage])
    } catch (error) {
      console.error("Error sending message:", error)
      
      // Create error message object
      const errorMessage: Message = {
        id: (Date.now() + 3).toString(), // Unique id for the error message
        content: "Sorry, I encountered an error. Please try again.",
        role: "assistant"
      }
      
      // Update messages state with error message
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false) // Reset loading state
    }
  }

  return (
    <Card className="w-full shadow-xl border-2">
      <CardHeader className="px-4 py-2 border-b h-10 flex items-center">
        <CardTitle className="text-lg">Recipe Assistant</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <ScrollArea className="h-[350px] px-4 py-4">
          <div className="space-y-4">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="flex items-center justify-center py-2">
                <Loader2 className="h-5 w-5 animate-spin text-muted-foreground" />
              </div>
            )}
            <div ref={messagesEndRef} /> {/* Reference for scrolling to the bottom */}
          </div>
        </ScrollArea>
      </CardContent>
      <CardFooter className="p-3 border-t">
        <form onSubmit={handleSubmit} className="flex w-full gap-2">
          <Input
            ref={inputRef} // Reference for the input field
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={isLoading}
            className="flex-1"
          />
          <Button 
            type="submit" 
            size="icon" 
            disabled={isLoading || !input.trim()} // Disable button if loading or input is empty
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardFooter>
    </Card>
  )
}
