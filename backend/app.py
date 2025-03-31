from flask import Flask, request, jsonify
import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

# Importing functions for web scraping and processing
from scraping.tavily import extract_raw_html_from_url
from processing.extract import get_sequential_chain, call_sequential_chain
from processing.document_splitter import split_text_into_documents, get_embeddings_for_chunks
from database.chromadb import get_chromadb_collection, add_documents, get_documents_by_url, delete_chromadb_collection
from rag.rag import build_graph, get_tools

# Initialize Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API key from environment variables
openai_key = os.getenv("OPENAI_API_KEY")

# Initialize language model and embedding model
llm = ChatOpenAI(model_name="gpt-4o-mini")
embedding_model = OpenAIEmbeddings(model="text-embedding-3-large")
sequential_chain = get_sequential_chain(llm=llm, verbose=False)

# Initialize chatbot model and tools
chat_llm = init_chat_model("gpt-4o-mini", model_provider="openai")
tools = get_tools()
graph = build_graph(tools=tools)

@app.route('/add_and_process_recipe', methods=['POST'])
def fetch_recipe():
    # Get the recipe URL from the request
    recipe_url = request.args.get('url')
    
    # Step 1: Get the raw HTML from the recipe URL
    raw_html = extract_raw_html_from_url(recipe_url)
    
    # Step 2: Get the structured data from the raw HTML
    final_output = call_sequential_chain(sequential_chain, raw_html)
    
    # Step 3: Split the raw HTML into documents
    docs = split_text_into_documents(raw_html)
        
    # Step 4: Add documents and blurb to the vector database
    chromadb_collection = get_chromadb_collection()
    embedded_docs = get_embeddings_for_chunks(docs, embedding_model)
    
    # Add the embedded documents to the database
    add_documents(chromadb_collection, embedded_docs, docs, recipe_url)
    
    # Check if recipe URL is provided
    if not recipe_url:
        return jsonify({"error": "No recipe URL provided"}), 400
    
    # Return the final output and recipe URL as JSON response
    return jsonify({"data": final_output, "url": recipe_url})

@app.route('/get_documents_for_recipe', methods=['GET'])
def get_documents():
    try:
        # Get the recipe URL parameter
        recipe_url = request.args.get('url')
        if not recipe_url:
            return jsonify({"error": "Missing 'url' parameter"}), 400

        # Retrieve ChromaDB collection
        chromadb_collection = get_chromadb_collection()

        # Fetch documents associated with the recipe URL
        docs = get_documents_by_url(collection=chromadb_collection, recipe_url=recipe_url)

        # Return the documents and recipe URL as JSON response
        return jsonify({"data": docs, "url": recipe_url})
    
    except Exception as e:
        # Return error message in case of an exception
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['GET'])
def chat_bot_func():
    # Retrieve query parameters for chat
    recipe_url = request.args.get('url')
    input_message = request.args.get('query')

    # Check for required parameters
    if not recipe_url or not input_message:
        return jsonify({"error": "Missing required parameters: 'url' and 'query'"}), 400

    # Initialize response storage for chat messages
    response_messages = []

    # Stream responses from the chat model
    for step in graph.stream(
        {"messages": [{"role": "user", "content": input_message}]},
        stream_mode="values",
    ):
        message = step["messages"][-1].content
        response_messages.append(message)

    # Return the final message in JSON format
    return jsonify({"response": response_messages[-1] if response_messages else "No response generated."})

@app.route('/delete_collection', methods=['POST'])
def delete_recipes():
    # Delete the ChromaDB collection
    delete_chromadb_collection()
    return jsonify({"response": "deleted collection"})
    
if __name__ == '__main__':
    # Run the Flask application in debug mode
    app.run(debug=True)
