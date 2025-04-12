import logging
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings

from config import Config
from processors.pdf_processor import PDFProcessor
from processors.text_processor import TextProcessor
from storage.document_collector import DocumentCollector
from storage.vector_store_manager import VectorStoreManager

logger = logging.getLogger(__name__)

class RAGPipeline:
    """Main pipeline orchestrator"""
    
    def __init__(self):
        print(f"Using device: {Config.DEVICE}")
        
        # Initialize embedding model
        self.embedding_model = HuggingFaceEmbeddings(
            model_name=Config.MODEL_NAME,
            model_kwargs={'device': Config.DEVICE},
            encode_kwargs={'normalize_embeddings': True}
        )
        
        # Initialize components
        self.pdf_processor = PDFProcessor()
        self.text_processor = TextProcessor()
        self.document_collector = DocumentCollector(self.pdf_processor, self.text_processor)
        self.vector_store_manager = VectorStoreManager(self.embedding_model)
    
    def build_knowledge_base(self, folders: List[str], is_two_column_flags: List[bool]) -> None:
        """Build complete knowledge base from document folders"""
        try:
            # Collect and process documents
            all_docs = self.document_collector.process_multiple_folders(folders, is_two_column_flags)
            logger.info(f"Collected {len(all_docs)} documents")
            
            # Build and save vector store
            vector_store = self.vector_store_manager.build_vector_store(all_docs)
            self.vector_store_manager.save_vector_store(vector_store, Config.VECTOR_STORE_PATH)
            
            logger.info(f"Vector store built successfully with {len(vector_store.index_to_docstore_id)} documents")
        except Exception as e:
            logger.error(f"Failed to build knowledge base: {e}")
            raise