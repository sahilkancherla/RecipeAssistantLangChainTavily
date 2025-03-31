// components/recipe-display.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { RecipeData } from "@/lib/interface"

// RecipeDisplay component to display recipe details
export default function RecipeDisplay({ recipe }: { recipe: RecipeData }) {
  const { data } = recipe
  const { recipe: recipeDetails, equipment_json, prep_json, nutrition_json } = data

  return (
    <div className="mt-8 w-full max-w-3xl mx-auto">
      <Card>
        <CardHeader>
          <div className="flex justify-between items-start">
            <div>
              <CardTitle className="text-2xl">{recipeDetails.name}</CardTitle>
              <div className="flex flex-wrap gap-2 mt-2">
                {/* Displaying recipe badges for cuisine, category, difficulty, and diet labels */}
                <Badge variant="outline">{recipeDetails.cuisine}</Badge>
                <Badge variant="outline">{recipeDetails.category}</Badge>
                <Badge variant="outline">{recipeDetails.difficulty}</Badge>
                {recipeDetails.diet_labels && 
                  recipeDetails.diet_labels.map((label) => (
                    <Badge key={label} variant="outline">{label}</Badge>
                  ))
                }
              </div>
            </div>
            <div className="text-right">
              {/* Displaying preparation, cooking, total time, and servings */}
              <div className="text-sm text-muted-foreground">
                Prep: {recipeDetails.prep_time} min
              </div>
              <div className="text-sm text-muted-foreground">
                Cook: {recipeDetails.cook_time} min
              </div>
              <div className="text-sm font-medium">
                Total: {recipeDetails.total_time} min
              </div>
              <div className="text-sm mt-1">
                Servings: {recipeDetails.servings}
              </div>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <Tabs defaultValue="ingredients">
            <TabsList className="grid grid-cols-5 mb-4">
              {/* Tab triggers for different sections of the recipe */}
              <TabsTrigger value="ingredients">Ingredients</TabsTrigger>
              <TabsTrigger value="instructions">Instructions</TabsTrigger>
              <TabsTrigger value="equipment">Equipment</TabsTrigger>
              <TabsTrigger value="tips">Tips</TabsTrigger>
              <TabsTrigger value="nutrition">Nutrition</TabsTrigger> {/* New Tab for Nutrition */}
            </TabsList>
            
            {/* Ingredients section */}
            <TabsContent value="ingredients" className="space-y-4">
              <ul className="list-disc pl-5 space-y-2">
                {recipeDetails.ingredients.map((ingredient, index) => (
                  <li key={index}>{ingredient}</li>
                ))}
              </ul>
            </TabsContent>
            
            {/* Instructions section */}
            <TabsContent value="instructions">
              <div className="space-y-4">
                <h3 className="font-medium text-lg">Preparation</h3>
                <ol className="list-decimal pl-5 space-y-2">
                  {prep_json.prep_instructions.map((instruction, index) => (
                    <li key={index}>{instruction}</li>
                  ))}
                </ol>
                
                <h3 className="font-medium text-lg mt-6">Cooking Instructions</h3>
                <ol className="list-decimal pl-5 space-y-2">
                  {recipeDetails.instructions.map((instruction, index) => (
                    <li key={index}>{instruction}</li>
                  ))}
                </ol>
              </div>
            </TabsContent>
            
            {/* Equipment section */}
            <TabsContent value="equipment">
              <div className="space-y-4">
                <h3 className="font-medium text-lg">Required Equipment</h3>
                <ul className="list-disc pl-5 space-y-2">
                  {equipment_json.equipment.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
                
                {/* Optional equipment section */}
                {equipment_json.optional_equipment && (
                  <>
                    <h3 className="font-medium text-lg mt-6">Optional Equipment</h3>
                    <ul className="list-disc pl-5 space-y-2">
                      {equipment_json.optional_equipment.map((item, index) => (
                        <li key={index}>{item}</li>
                      ))}
                    </ul>
                  </>
                )}
              </div>
            </TabsContent>
            
            {/* Tips section */}
            <TabsContent value="tips">
              <ul className="list-disc pl-5 space-y-2">
                {recipeDetails.author_tips.map((tip, index) => (
                  <li key={index}>{tip}</li>
                ))}
              </ul>
            </TabsContent>

            {/* Nutrition section */}
            <TabsContent value="nutrition">
              <div className="space-y-4">
                <h3 className="font-medium text-lg">Nutrition Information</h3>
                <ul className="list-disc pl-5 space-y-2">
                  <li>Calories: {nutrition_json.calories}</li>
                  <li>Carbs: {nutrition_json.carbs} g</li>
                  <li>Fat: {nutrition_json.fat} g</li>
                  <li>Protein: {nutrition_json.protein} g</li>
                </ul>
              </div>
            </TabsContent>
          </Tabs>
        </CardContent>
      </Card>
    </div>
  )
}
