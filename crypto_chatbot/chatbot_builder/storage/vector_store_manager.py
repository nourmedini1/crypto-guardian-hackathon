import logging
from typing import List
from langchain.docstore.document import Document
from langchain_community.vectorstores import FAISS

logger = logging.getLogger(__name__)

class VectorStoreManager:
    """Manages vector store operations"""
    
    def __init__(self, embedding_model):
        self.embedding_model = embedding_model
    
    def build_vector_store(self, documents: List[Document]) -> FAISS:
        """Build a vector store from documents"""
        return FAISS.from_documents(documents, self.embedding_model)
    
    def save_vector_store(self, vector_store: FAISS, path: str) -> None:
        """Save vector store to disk"""
        vector_store.save_local(path)
        logger.info(f"Vector store saved to {path}")
    
    def load_vector_store(self, path: str) -> FAISS:
        """Load vector store from disk"""
        return FAISS.load_local(path, self.embedding_model, allow_dangerous_deserialization=True)