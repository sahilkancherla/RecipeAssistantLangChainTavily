// components/chatbot/chat-button.tsx
"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { MessageCircle, X } from "lucide-react"
import { ChatDialog } from "./chat-dialog"
import { AnimatePresence, motion } from "framer-motion"

// ChatButton component to toggle the chat dialog
export function ChatButton({ url }: { url: string }) {
  // State to manage the visibility of the chat dialog
  const [isOpen, setIsOpen] = useState(false)

  return (
    <>
      {/* Button to open/close the chat dialog */}
      <div className="fixed bottom-4 right-4 z-50">
        <Button
          onClick={() => setIsOpen(!isOpen)} // Toggle chat dialog visibility
          size="icon"
          className="h-14 w-14 rounded-full shadow-lg"
        >
          {isOpen ? (
            <X className="h-6 w-6" /> // Close icon when dialog is open
          ) : (
            <MessageCircle className="h-6 w-6" /> // Open icon when dialog is closed
          )}
        </Button>
      </div>

      {/* Animate presence for chat dialog */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 50, scale: 0.9 }} // Initial animation state
            animate={{ opacity: 1, y: 0, scale: 1 }} // Animation when dialog is open
            exit={{ opacity: 0, y: 20, scale: 0.9 }} // Animation when dialog is closed
            transition={{ type: "spring", stiffness: 300, damping: 30 }} // Animation transition settings
            className="fixed bottom-20 right-4 z-40 w-[350px] md:w-[400px]"
          >
            <ChatDialog url={url} onClose={() => setIsOpen(false)} /> {/* Chat dialog component */}
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
