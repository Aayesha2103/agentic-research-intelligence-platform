from langchain_ollama import OllamaEmbeddings


def get_embedding_model():
    """
    Creates the local embedding model used by the RAG system.
    """

    return OllamaEmbeddings(
        model="bge-m3"
    )


def create_embedding(text: str) -> list[float]:
    """
    Converts text into a numerical embedding vector.
    """

    embedding_model = get_embedding_model()

    return embedding_model.embed_query(text)