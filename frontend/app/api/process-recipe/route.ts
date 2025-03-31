// app/api/process-recipe/route.ts
import { NextRequest, NextResponse } from "next/server"

// Get the backend URL from the environment variables
const backend_url = process.env.BACKEND_URL

// Handle POST requests to process a recipe
export async function POST(request: NextRequest) {
  try {
    // Parse the incoming JSON request to extract the recipe URL
    const { url } = await request.json()
    
    // Validate that the recipe URL is provided
    if (!url) {
      return NextResponse.json(
        { error: "Recipe URL is required" },
        { status: 400 } // Bad Request
      )
    }

    // Fetch the processed recipe data from the external service
    const response = await fetch(`${backend_url}/add_and_process_recipe?url=${url}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    
    // Parse the JSON response from the external service
    const data = await response.json();
    
    // Return the processed recipe data in the response
    return NextResponse.json(data)
  } catch (error) {
    // Log any errors that occur during processing
    console.error("Error processing recipe:", error)
    return NextResponse.json(
      { error: "Failed to process recipe" },
      { status: 500 } // Internal Server Error
    )
  }
}
