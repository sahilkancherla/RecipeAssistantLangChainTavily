import os
import json
from langchain_core.output_parsers import PydanticOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_openai import ChatOpenAI

from models.model import RecipeResponse, RecipeEquipmentResponse, PrepResponse, NutritionResponse
from models.prompts import get_recipe_prompt, get_equipment_prompt, get_prep_prompt, get_nutrition_prompt

def get_sequential_chain(llm: ChatOpenAI, verbose: bool = False):
    """
    Create a sequential chain of LLM chains for processing recipe-related queries.

    Args:
        llm (ChatOpenAI): The language model to use for generating responses.
        verbose (bool): Flag to enable verbose output for debugging.

    Returns:
        SequentialChain: A chain that processes recipe, equipment, prep, and nutrition information.
    """
    # Initialize output parsers for each type of response
    parser_recipe = PydanticOutputParser(pydantic_object=RecipeResponse)
    parser_equipment = PydanticOutputParser(pydantic_object=RecipeEquipmentResponse)
    parser_prep = PydanticOutputParser(pydantic_object=PrepResponse)
    parser_nutrition = PydanticOutputParser(pydantic_object=NutritionResponse)
    
    # Get prompts for each type of information
    recipe_prompt = get_recipe_prompt(parser_recipe)
    equipment_prompt = get_equipment_prompt(parser_equipment)
    prep_prompt = get_prep_prompt(parser_prep)
    nutrition_prompt = get_nutrition_prompt(parser_nutrition)
    
    # Create individual LLM chains for each prompt
    recipe_chain = LLMChain(llm=llm, prompt=recipe_prompt, output_key="recipe")
    equipment_chain = LLMChain(llm=llm, prompt=equipment_prompt, output_key="equipment")
    prep_chain = LLMChain(llm=llm, prompt=prep_prompt, output_key="prep")
    nutrition_chain = LLMChain(llm=llm, prompt=nutrition_prompt, output_key="nutrition")
    
    # Combine all chains into a sequential chain
    sequential_chain = SequentialChain(
        chains=[recipe_chain, equipment_chain, prep_chain, nutrition_chain],
        input_variables=["query"],
        output_variables=["recipe", "equipment", "prep", "nutrition"],  # Keep both outputs
        verbose=verbose,
    )
    
    return sequential_chain

def call_sequential_chain(sequential_chain, query):
    """
    Call the sequential chain with a user query and return structured outputs.

    Args:
        sequential_chain (SequentialChain): The chain to process the query.
        query (str): The user query to process.

    Returns:
        dict: A dictionary containing structured outputs for recipe, prep, equipment, and nutrition.
    """
    # Execute the sequential chain with the provided query
    final_output = sequential_chain({"query": query})
    
    # Clean and extract JSON responses from the final output
    recipe_json = clean_json_and_return(final_output['recipe'])
    prep_json = clean_json_and_return(final_output['prep'])
    equipment_json = clean_json_and_return(final_output['equipment'])
    nutrition_json = clean_json_and_return(final_output['nutrition'])
    
    # Compile results into a dictionary
    res = {
        'recipe': recipe_json,
        'prep_json': prep_json,
        'equipment_json': equipment_json,
        'nutrition_json': nutrition_json
    }
    return res

def clean_json_and_return(string_json):
    """
    Clean a JSON string by removing markdown formatting and parsing it into a Python object.

    Args:
        string_json (str): The JSON string to clean and parse.

    Returns:
        dict: The parsed JSON object.
    """
    # Remove markdown formatting and parse the cleaned string into a JSON object
    cleaned_json_str = string_json.strip("```json").strip("```").strip()
    cleaned_json = json.loads(cleaned_json_str)
    return cleaned_json