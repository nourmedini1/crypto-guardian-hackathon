import pdfplumber
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class PDFProcessor:
    """Handles PDF extraction and processing"""
    
    @staticmethod
    def extract_columns_sequentially(pdf_path: str) -> str:
        """Extract text from a two-column PDF by processing columns separately"""
        all_text = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    width = page.width
                    left_bbox = (0, 0, width / 2, page.height)
                    right_bbox = (width / 2, 0, width, page.height)
                    left_text = page.within_bbox(left_bbox).extract_text() or ""
                    right_text = page.within_bbox(right_bbox).extract_text() or ""
                    all_text.append(left_text)
                    all_text.append(right_text)
        except Exception as e:
            logger.error(f"Error extracting columns from {pdf_path}: {e}")
        return "\n".join(all_text)
    
    @staticmethod
    def extract_single_column(pdf_path: str) -> str:
        """Extract text from a single-column PDF"""
        text = ""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text() or ""
                    text += page_text + "\n"
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
        return text
    
    @staticmethod
    def get_metadata(pdf_path: str) -> Dict[str, Any]:
        """Extract metadata from PDF file"""
        try:
            with pdfplumber.open(pdf_path) as pdf:
                return pdf.metadata or {}
        except Exception as e:
            logger.error(f"Error reading metadata from {pdf_path}: {e}")
            return {}
    
    def process_pdf(self, pdf_path: str, is_two_column: bool = True, num_title_lines: int = 5) -> Dict[str, Any]:
        """Process a PDF file and extract its content and metadata"""
        try:
            # Extract text based on layout
            if is_two_column:
                text = self.extract_columns_sequentially(pdf_path)
            else:
                text = self.extract_single_column(pdf_path)
            
            # Get metadata
            metadata = self.get_metadata(pdf_path)
            author = metadata.get("Author", "Unknown")
            
            # Extract title from first few lines
            lines = text.splitlines()
            title = " ".join(lines[:num_title_lines]) if lines else "Untitled"
            
            meta = {"author": author, "title": title, "source": pdf_path}
            return {"text": text, "metadata": meta}
            
        except Exception as e:
            logger.error(f"Error processing PDF {pdf_path}: {e}")
            return {"text": "", "metadata": {"source": pdf_path}}