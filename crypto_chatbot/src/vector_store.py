from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from config import RAG_MODEL_NAME, DEVICE, VECTOR_STORE_PATH, logger

class VectorStoreManager:
    def __init__(self):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=RAG_MODEL_NAME,
            model_kwargs={'device': DEVICE},
            encode_kwargs={'normalize_embeddings': True}
        )
        self.vector_store = self._load_vector_store()
    
    def _load_vector_store(self):
        """Load the vector store from disk"""
        try:
            vector_store = FAISS.load_local(
                VECTOR_STORE_PATH, 
                self.embedding_model, 
                allow_dangerous_deserialization=True
            )
            logger.info(f"Loaded vector store from {VECTOR_STORE_PATH}")
            return vector_store
        except Exception as e:
            raise Exception(f"Failed to load vector store from {VECTOR_STORE_PATH}: {e}")
    
    def get_relevant_documents(self, query, k=3):
        """Retrieve relevant documents for a query"""
        retriever = self.vector_store.as_retriever(search_kwargs={"k": k})
        documents = retriever.get_relevant_documents(query)
        logger.info(f"Retrieved {len(documents)} documents for query: {query}")
        return documents