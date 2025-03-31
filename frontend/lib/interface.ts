// Define the structure of the recipe data
export interface RecipeData {
    data: {
      equipment_json: {
        equipment: string[]
        optional_equipment: string[]
      }
      prep_json: {
        prep_instructions: string[]
      }
      recipe: {
        author_tips: string[]
        category: string
        cook_time: number
        cuisine: string
        diet_labels: string[] | null
        difficulty: string
        ingredients: string[]
        instructions: string[]
        name: string
        prep_time: number
        servings: number
        total_time: number
      }
      nutrition_json: {
        calories: number
        carbs: number
        fat: number
        protein: number
      }
    }
    url: string
}

// Define the structure of a chat message
export interface Message {
    id: string
    content: string
    role: "user" | "assistant"
}

// Define the structure of a task
export interface Task {
    id: number
    name: string
    completed: boolean
}