import os
import logging
from concurrent.futures import ProcessPoolExecutor
from typing import List, Dict, Any, Optional
from langchain.docstore.document import Document
from processors.pdf_processor import PDFProcessor
from processors.text_processor import TextProcessor

logger = logging.getLogger(__name__)

class DocumentCollector:
    """Collects and processes documents from folders"""
    
    def __init__(self, pdf_processor: PDFProcessor, text_processor: TextProcessor):
        self.pdf_processor = pdf_processor
        self.text_processor = text_processor
    
    def process_folder(self, folder_path: str, is_two_column: bool = True) -> List[Document]:
        """Process all PDFs in a folder"""
        docs = []
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith('.pdf'):
                continue
                
            pdf_path = os.path.join(folder_path, filename)
            try:
                # Process the PDF
                result = self.pdf_processor.process_pdf(pdf_path, is_two_column=is_two_column)
                if not result["text"]:
                    logger.warning(f"No text extracted from {pdf_path}")
                    continue
                
                # Create document chunks
                chunks = self.text_processor.create_documents(result["text"], result["metadata"])
                docs.extend(chunks)
                logger.info(f"Processed {pdf_path}: {len(chunks)} chunks created.")
            except Exception as e:
                logger.error(f"Error processing file {pdf_path}: {e}")
        
        return docs
    
    def process_multiple_folders(self, folders: List[str], is_two_column_flags: List[bool]) -> List[Document]:
        """Process multiple folders with different column settings"""
        all_docs = []
        with ProcessPoolExecutor() as executor:
            futures = []
            for folder, is_two_column in zip(folders, is_two_column_flags):
                futures.append(executor.submit(self.process_folder, folder, is_two_column))
            
            for future in futures:
                try:
                    docs = future.result()
                    all_docs.extend(docs)
                except Exception as e:
                    logger.error(f"Error in process pool: {e}")
        
        return all_docs