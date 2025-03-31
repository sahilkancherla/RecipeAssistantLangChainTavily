// components/chatbot/chat-message.tsx
import { cn } from "@/lib/utils"
import { Avatar, AvatarFallback } from "@/components/ui/avatar"

// Define the props for the ChatMessage component
interface ChatMessageProps {
  message: {
    content: string // The content of the chat message
    role: "user" | "assistant" // The role of the message sender
  }
}

// ChatMessage component to display individual chat messages
export function ChatMessage({ message }: ChatMessageProps) {
  // Determine if the message is from the user
  const isUser = message.role === "user"
  
  return (
    <div
      className={cn(
        "flex items-start gap-3 text-sm", // Flex container for message layout
        isUser ? "flex-row-reverse" : "" // Reverse layout for user messages
      )}
    >
      <Avatar className={cn("h-8 w-8", isUser ? "bg-primary" : "bg-zinc-700")}>
        <AvatarFallback className={isUser ? "" : "text-white"}>
          {isUser ? "U" : "A"}
        </AvatarFallback>
      </Avatar>
      <div
        className={cn(
          "rounded-lg px-3 py-2 max-w-[85%]", // Styling for message bubble
          isUser
            ? "bg-primary text-primary-foreground" // User message styles
            : "bg-muted" // Assistant message styles
        )}
      >
        {message.content}
      </div>
    </div>
  )
}
