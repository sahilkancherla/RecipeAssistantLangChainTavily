import os
import requests
from langchain_core.messages import SystemMessage
from langgraph.prebuilt import ToolNode
from langgraph.graph import MessagesState, StateGraph
from langchain_core.messages import HumanMessage
from langgraph.graph import END
from langgraph.prebuilt import tools_condition
from langchain_core.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from database.chromadb import get_chromadb_collection
from models.prompts import get_chat_prompt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set environment variables for API keys and user agent
os.environ['USER_AGENT'] = 'myagent'
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = os.getenv('LANGSMITH_API_KEY')
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')

# Initialize embedding function and language model
embedding_function = OpenAIEmbeddings(model="text-embedding-3-large")
llm = init_chat_model("gpt-4o-mini", model_provider="openai")

def refine_query(state: MessagesState):
    """Improve the user's query before retrieval while ensuring it relates to the available recipe data."""
    user_query = state["messages"][-1].content  # Get the last user query

    # Generate embedding for the user query
    query_embedding = embedding_function.embed_query(user_query)
    collection = get_chromadb_collection()
    
    # Query the database for similar documents
    retrieved_docs = collection.query(
        query_embeddings=[query_embedding],  # Querying with the embedding
        n_results=5,  # Retrieve top 5 most similar documents
    )

    # Extract recipe context from retrieved documents
    if retrieved_docs:
        recipe_context = "\n\n".join(doc for doc in retrieved_docs['documents'][0])
    else:
        recipe_context = "No relevant recipe context found."

    # Use LLM to refine the query with recipe context
    refined_query = llm.invoke(
        f"Given the following recipe content:\n\n"
        f"{recipe_context}\n\n"
        f"Rewrite the following user query to be clearer and more specific for information retrieval, "
        f"while ensuring it stays relevant to the given recipe details:\n\n"
        f"User Query: {user_query}\n\n"
    ).content
    
    return {"messages": [HumanMessage(content=refined_query)]}  # Return refined message

@tool(response_format="content_and_artifact")
def retrieve(query):
    """Retrieve information related to a query."""
    
    # Generate embedding for the user query
    query_embedding = embedding_function.embed_query(query)
    collection = get_chromadb_collection()
    
    # Query the database for similar documents
    retrieved_docs = collection.query(
        query_embeddings=[query_embedding],  # Querying with the embedding
        n_results=5,  # Retrieve top 5 most similar documents
    )
    
    # Check if any documents were retrieved
    if not retrieved_docs:
        print("retrieved no docs")  # Log if no documents were found
        return "No relevant recipe found. Please provide ingredients or steps.", []
    
    # Serialize the retrieved documents and their metadata
    serialized = "\n\n".join(
        f"Source: {metadata}\nContent: {doc}"
        for doc, metadata in zip(retrieved_docs["documents"][0], retrieved_docs["metadatas"][0])
    )
    
    return serialized, retrieved_docs  # Return serialized content and retrieved documents

def query_or_respond(state: MessagesState):
    """Generate tool call for recipe retrieval or respond."""
    llm_with_tools = llm.bind_tools([retrieve])  # Bind the retrieval tool
    response = llm_with_tools.invoke(state["messages"])  # Invoke the LLM with the current messages
    return {"messages": [response]}  # Append message to state

def get_tools():
    """Return the tools available for use."""
    tools = ToolNode([retrieve])  # Create a ToolNode with the retrieve function
    return tools

def generate(state: MessagesState):
    """Generate answer using retrieved recipe details."""
    # Extract recent tool messages (retrieved recipe details)
    recent_tool_messages = []
    for message in reversed(state["messages"]):
        if message.type == "tool":
            recent_tool_messages.append(message)
        else:
            break
    tool_messages = recent_tool_messages[::-1]  # Reverse to maintain original order

    # Format retrieved recipe content
    if tool_messages:
        recipe_content = "\n\n".join(doc.content for doc in tool_messages)
    else:
        recipe_content = "No relevant recipe found. Please try another query."

    # Define system prompt for structured recipe guidance
    system_message_content = get_chat_prompt(recipe_content)

    # Filter relevant conversation messages (ignore tool calls)
    conversation_messages = [
        message
        for message in state["messages"]
        if message.type in ("human", "system") or (message.type == "ai" and not message.tool_calls)
    ]
    prompt = [SystemMessage(system_message_content)] + conversation_messages  # Create the prompt for LLM

    # Generate response from the LLM
    response = llm.invoke(prompt)
    return {"messages": [response]}  # Return the generated response

def build_graph(tools):
    """Build the state graph for the query processing flow."""
    graph_builder = StateGraph(MessagesState)
    graph_builder.add_node(refine_query)  # Add query refinement step
    graph_builder.add_node(query_or_respond)  # Add query or respond step
    graph_builder.add_node(tools)  # Add tools to the graph
    graph_builder.add_node(generate)  # Add generate step

    graph_builder.set_entry_point("refine_query")  # Start with query improvement

    # Define the flow of the graph
    graph_builder.add_edge("refine_query", "query_or_respond")  # Send improved query forward
    graph_builder.add_conditional_edges(
        "query_or_respond",
        tools_condition,
        {END: END, "tools": "tools"},
    )
    graph_builder.add_edge("tools", "generate")  # Connect tools to generate step
    graph_builder.add_edge("generate", END)  # End the graph

    graph = graph_builder.compile()  # Compile the graph
    return graph  # Return the compiled graph
