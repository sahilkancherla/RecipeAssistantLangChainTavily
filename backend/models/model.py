from pydantic import BaseModel
from typing import List, Optional

class RecipeResponse(BaseModel):
    """Model representing the response for a recipe."""
    name: str  # Name of the recipe
    cuisine: str  # Type of cuisine (e.g., Italian, Indian)
    category: str  # Category of the recipe (e.g., "Dessert", "Main Course")
    servings: int  # Number of servings the recipe yields
    prep_time: int  # Preparation time in minutes
    cook_time: int  # Cooking time in minutes
    total_time: int  # Total time in minutes (prep + cook)
    difficulty: str  # Difficulty level (e.g., "Easy", "Medium", "Hard")
    ingredients: List[str]  # List of ingredient names
    instructions: List[str]  # Step-by-step cooking instructions
    diet_labels: Optional[List[str]]  # Optional dietary labels (e.g., Vegan, Gluten-Free)
    author_tips: Optional[List[str]]  # Optional tips provided by the author

class RecipeEquipmentResponse(BaseModel):
    """Model representing the required kitchen equipment for a recipe."""
    equipment: List[str]  # Essential kitchen tools/equipment
    optional_equipment: Optional[List[str]] = None  # Optional tools that may be useful

class PrepResponse(BaseModel):
    """Model representing the preparation instructions for a recipe."""
    prep_instructions: List[str]  # List of preparation steps

class NutritionResponse(BaseModel):
    """Model representing the nutritional information of a recipe."""
    calories: int  # Total calories per serving
    protein: int  # Protein content per serving
    carbs: int  # Carbohydrate content per serving
    fat: int  # Fat content per serving