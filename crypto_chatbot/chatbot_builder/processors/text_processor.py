from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from typing import List, Dict
from config import Config

class TextProcessor:
    """Handles text chunking operations"""
    
    def __init__(self, chunk_size: int = Config.CHUNK_SIZE, chunk_overlap: int = Config.CHUNK_OVERLAP):
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", " ", ""]
        )
    
    def chunk_text(self, text: str) -> List[str]:
        """Split text into manageable chunks"""
        return self.splitter.split_text(text)
    
    def create_documents(self, text: str, metadata: Dict) -> List[Document]:
        """Create Document objects from text with metadata"""
        chunks = self.chunk_text(text)
        return [Document(page_content=chunk, metadata=metadata) for chunk in chunks]