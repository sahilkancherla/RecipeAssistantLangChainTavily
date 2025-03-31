"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Loader2, Check } from "lucide-react"
import RecipeDisplay from "@/components/recipe-display"
import { ChatButton } from "@/components/chatbot/chat-button"
import { Progress } from "@/components/ui/progress"
import { RecipeData, Task } from "@/lib/interface"

export default function Home() {
  const [url, setUrl] = useState("") // State for the recipe URL
  const [recipeData, setRecipeData] = useState<RecipeData | null>(null) // State for the recipe data
  const [loading, setLoading] = useState(false) // State for loading status
  const [error, setError] = useState<string | null>(null) // State for error messages
  const [tasks, setTasks] = useState<Task[]>([
    { id: 1, name: "Loading recipe URL", completed: false },
    { id: 2, name: "Extracting raw recipe information", completed: false },
    { id: 3, name: "Identifying recipe components", completed: false },
    { id: 4, name: "Cleaning recipe information", completed: false },
    { id: 5, name: "Finalizing recipe data", completed: false }
  ])
  const [progress, setProgress] = useState(0) // State for progress percentage

  useEffect(() => {
    if (!loading) {
      // Reset tasks and progress when not loading
      setTasks(tasks.map(task => ({ ...task, completed: false })))
      setProgress(0)
      return
    }

    let currentTaskIndex = -1
    const totalTasks = tasks.length
    
    // Interval to update task completion and progress
    const interval = setInterval(() => {
      if (currentTaskIndex < totalTasks) {
        setTasks(prevTasks => 
          prevTasks.map((task, index) => 
            index === currentTaskIndex ? { ...task, completed: true } : task
          )
        )
        
        // Update progress bar
        const newProgress = Math.round(((currentTaskIndex + 1) / totalTasks) * 100)
        setProgress(newProgress)
        
        currentTaskIndex++
      } else {
        clearInterval(interval) // Clear interval when all tasks are completed
      }
    }, 2500)

    return () => clearInterval(interval) // Cleanup interval on component unmount
  }, [loading])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault() // Prevent default form submission
    setLoading(true) // Set loading state
    setError(null) // Reset error state
    // Reset tasks and progress
    setTasks(tasks.map(task => ({ ...task, completed: false })))
    setProgress(0)

    try {
      const response = await fetch("/api/process-recipe", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }), // Send the URL to the API
      })

      if (!response.ok) {
        throw new Error("Failed to process recipe") // Handle API errors
      }

      const data = await response.json() // Parse the response data
      setRecipeData(data) // Set the recipe data
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred") // Handle errors
    } finally {
      // Complete all tasks when done
      setTasks(tasks.map(task => ({ ...task, completed: true })))
      setProgress(100)
      
      // Small delay before hiding loading UI to show completed state
      setTimeout(() => {
        setLoading(false)
      }, 1000)
    }
  }

  return (
    <main className="container mx-auto py-10 px-4">
      <Card className="w-full max-w-3xl mx-auto">
        <CardHeader>
          <CardTitle>Recipe Extractor</CardTitle>
          <CardDescription>Enter a recipe URL to extract the details</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              type="url"
              placeholder="https://example.com/recipe"
              value={url}
              onChange={(e) => setUrl(e.target.value)} // Update URL state on input change
              required
              className="flex-1"
            />
            <Button type="submit" disabled={loading}>
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Processing
                </>
              ) : (
                "Process"
              )}
            </Button>
          </form>
          
          {loading && (
            <div className="mt-6 space-y-4">
              <Progress value={progress} className="h-2 w-full" />
              
              <div className="space-y-3">
                {tasks.map((task) => (
                  <div key={task.id} className="flex items-center gap-3">
                    <div className={`flex h-6 w-6 items-center justify-center rounded-full ${
                      task.completed 
                        ? "bg-green-100 text-green-600" 
                        : "bg-slate-100 text-slate-400"
                    }`}>
                      {task.completed ? (
                        <Check className="h-4 w-4" />
                      ) : (
                        <div className="h-4 w-4" />
                      )}
                    </div>
                    <span className={`text-sm ${
                      task.completed ? "text-slate-900" : "text-slate-500"
                    }`}>
                      {task.name}
                    </span>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {error && (
            <div className="mt-4 p-4 bg-red-50 text-red-600 rounded-md">
              {error} {/* Display error message if exists */}
            </div>
          )}
        </CardContent>
      </Card>

      {recipeData && !loading && <RecipeDisplay recipe={recipeData} />} {/* Display recipe data if available */}
      <ChatButton url={url} /> {/* Pass the URL to the ChatButton */}
    </main>
  )
}
