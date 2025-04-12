import os
import logging
from pipeline.RAG_pipeline import RAGPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    folders = [os.path.join("pdfs", "half_page"), "pdfs"]
    is_two_column_flags = [True, False]
    
    try:
        pipeline = RAGPipeline()
        pipeline.build_knowledge_base(folders, is_two_column_flags)
    except Exception as e:
        logger.error(f"Failed to build vector store: {e}")