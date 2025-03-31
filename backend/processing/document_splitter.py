from langchain_core.documents import Document  
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text_into_documents(text: str, chunk_size: int = 1000, chunk_overlap: int = 200, add_start_index: bool = True):
    """
    Splits the input text into smaller document chunks.

    Args:
        text (str): The text to be split into chunks.
        chunk_size (int): The maximum size of each chunk in characters. Default is 1000.
        chunk_overlap (int): The number of overlapping characters between chunks. Default is 200.
        add_start_index (bool): If True, includes the starting index of each chunk in the original text. Default is True.

    Returns:
        List[str]: A list of text chunks.
    """
    # Initialize the text splitter with specified parameters
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,  # Maximum size of each chunk
        chunk_overlap=chunk_overlap,  # Overlap between chunks
        add_start_index=add_start_index,  # Whether to track the index in the original document
    )
    
    # Split the text into chunks
    chunks = text_splitter.split_text(text)
    
    return chunks

def get_embeddings_for_chunks(chunks, embedding_model):
    """
    Generates embeddings for a list of text chunks using the specified embedding model.

    Args:
        chunks (List[str]): The list of text chunks to embed.
        embedding_model: The model used to generate embeddings.

    Returns:
        List: A list of embedded chunks.
    """
    # Embed the document chunks using the provided embedding model
    embedded_chunks = embedding_model.embed_documents(chunks)
    
    return embedded_chunks