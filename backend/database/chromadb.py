import chromadb  # Import the chromadb library for database operations

def get_chromadb_collection():
    """
    Initialize and return the ChromaDB collection for recipes.

    Returns:
        Collection: The ChromaDB collection for storing recipe documents.
    """
    client = chromadb.PersistentClient(path="./chroma_db")  # Create a persistent client with the specified path
    collection = client.get_or_create_collection("recipes")  # Get or create the 'recipes' collection
    return collection  # Return the collection

def add_documents(collection, embeddings, docs, recipe_url):
    """
    Add documents to the ChromaDB collection with associated metadata.

    Args:
        collection (Collection): The ChromaDB collection to add documents to.
        embeddings (List): The list of embeddings corresponding to the documents.
        docs (List): The list of documents to be added.
        recipe_url (str): The URL of the recipe for metadata purposes.
    """
    # Iterate over the embeddings and add each document to the collection
    for i, embedded_chunk in enumerate(embeddings):
        collection.add(
            ids=[f"{recipe_url}_{i}"],  # Unique ID for each document based on recipe URL and index
            embeddings=[embeddings[i]],  # Embedding for the document
            documents=[docs[i]],  # The actual document content
            metadatas=[{"recipe_url": recipe_url, "chunk_index": i}]  # Metadata including recipe URL and chunk index
        )

def get_documents_by_url(collection, recipe_url: str):
    """
    Retrieve documents from the ChromaDB collection by recipe URL.

    Args:
        collection (Collection): The ChromaDB collection to query.
        recipe_url (str): The URL of the recipe to filter documents.

    Returns:
        List: A list of documents associated with the given recipe URL.
    """
    results = collection.get(
        where={"recipe_url": recipe_url}  # Query to filter documents by recipe URL
    )

    return results.get("documents", []) if results else []  # Return documents or an empty list if none found

def delete_chromadb_collection():
    """
    Delete the ChromaDB collection for recipes.
    """
    client = chromadb.PersistentClient(path="./chroma_db")  # Create a persistent client with the specified path
    client.delete_collection("recipes")  # Delete the 'recipes' collection
