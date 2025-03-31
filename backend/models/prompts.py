from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate

def get_chat_prompt(recipe_content: str):
    """
    Generates a system message for a culinary assistant based on the provided recipe content.
    
    Args:
        recipe_content (str): The content of the recipe to be used for context.
    
    Returns:
        str: A formatted system message for the chat assistant.
    """
    system_message_content = (
        "You are a knowledgeable culinary assistant with access to the following recipe context. "
        "Answer user questions accurately based on the retrieved recipe details. "
        "You can provide information on ingredients, instructions, cooking techniques, substitutions, "
        "nutritional details, storage tips, and variations. "
        "If the user asks for modifications (e.g., making it vegan, gluten-free, or low-calorie), provide relevant suggestions. "
        "If you don't have an exact match, suggest a similar alternative or say that you don't know. "
        "Be concise if possible, no more than 100 words."
        "\n\n"
        f"{recipe_content}"
    )
    return system_message_content

def get_recipe_prompt(parser: PydanticOutputParser):
    """
    Creates a prompt template for extracting key details from a recipe.
    
    Args:
        parser (PydanticOutputParser): The output parser to format the response.
    
    Returns:
        ChatPromptTemplate: A template for the recipe extraction prompt.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an intelligent recipe parser designed to extract key details from raw recipe text.
                Your task is to analyze the given recipe and identify the following information:
                1. Recipe name.
                2. Cuisine type (e.g., Italian, Indian, American).
                3. Category (e.g., Dessert, Main Course, Appetizer).
                4. Servings.
                5. Preparation time (in minutes).
                6. Cooking time (in minutes).
                7. Total time (in minutes).
                8. Difficulty level (Easy, Medium, Hard).
                9. Ingredients (list). Extract a list of all ingredients, ensuring that duplicate ingredients
                are combined by summing their respective quantities and standardizing units where applicable.
                10. Step-by-step cooking instructions.
                11. Diet labels (e.g. Vegan, Gluten-Free, Keto, Dairy-Free).
                12. Any suggestions/tips provided by the author in the recipe.
                
                Wrap the output in this format and provide no other text:
                {format_instructions}
                """
            ),
            ("human", "{query}")
        ]
    ).partial(format_instructions=parser.get_format_instructions())

def get_equipment_prompt(parser: PydanticOutputParser):
    """
    Creates a prompt template for extracting required kitchen equipment from recipe instructions.
    
    Args:
        parser (PydanticOutputParser): The output parser to format the response.
    
    Returns:
        ChatPromptTemplate: A template for the equipment extraction prompt.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an intelligent kitchen assistant designed to extract required equipment from a given list of recipe instructions.
                Your task is to analyze the provided steps and identify the following:
                1. A list of essential kitchen equipment (e.g., mixing bowl, whisk, oven, saucepan, measuring cups).
                2. A list of optional equipment that may be useful but are not strictly necessary.
                
                Wrap the output in this format and provide no other text:
                {format_instructions}
                """
            ),
            ("human", "{query}")
        ]
    ).partial(format_instructions=parser.get_format_instructions())

def get_prep_prompt(parser: PydanticOutputParser):
    """
    Creates a prompt template for extracting preparation steps from a recipe.
    
    Args:
        parser (PydanticOutputParser): The output parser to format the response.
    
    Returns:
        ChatPromptTemplate: A template for the preparation steps extraction prompt.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an intelligent kitchen assistant designed to extract and organize all preparation steps for a given recipe. 
                Your task is to analyze the recipe instructions and identify any **preparation steps** that must be completed before cooking begins. 
                These steps typically include actions like chopping, marinating, measuring, preheating, and similar tasks.

                **Your output should include:**
                1. A **step-by-step list** of all necessary prep actions.
                
                Wrap the output in this format and provide no other text:
                {format_instructions}
                """
            ),
            ("human", "{query}")
        ]
    ).partial(format_instructions=parser.get_format_instructions())

def get_nutrition_prompt(parser: PydanticOutputParser):
    """
    Creates a prompt template for extracting nutritional information from a recipe.
    
    Args:
        parser (PydanticOutputParser): The output parser to format the response.
    
    Returns:
        ChatPromptTemplate: A template for the nutrition extraction prompt.
    """
    return ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
                You are an intelligent nutrition assistant designed to extract nutritional information from a given recipe.
                Your task is to analyze the recipe instructions and identify the following:
                1. Calories.
                2. Protein.
                3. Carbs.
                4. Fat.
                Wrap the output in this format and provide no other text:
                {format_instructions}
                """
            ),
            ("human", "{query}")
        ]
    ).partial(format_instructions=parser.get_format_instructions())