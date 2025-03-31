// app/api/chat/route.ts
import { NextRequest, NextResponse } from "next/server"

// Get the backend URL from the environment variables
const backend_url = process.env.BACKEND_URL

// Handle POST requests to the chat API
export async function POST(request: NextRequest) {
  try {
    // Parse the incoming JSON request
    const { url, query } = await request.json()
    
    // Validate that the query is provided
    if (!query) {
      return NextResponse.json(
        { error: "Message is required" },
        { status: 400 } // Bad Request
      )
    }

    // Fetch response from the external chat service
    const response = await fetch(`${backend_url}/chat?url=${url}&query=${query}`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    
    // Parse the JSON response from the external service
    const data = await response.json();
    
    // Return the data in the response
    return NextResponse.json({ data })
  } catch (error) {
    // Log any errors that occur during processing
    console.error("Error in chat API:", error)
    return NextResponse.json(
      { error: "Failed to process message" },
      { status: 500 } // Internal Server Error
    )
  }
}
