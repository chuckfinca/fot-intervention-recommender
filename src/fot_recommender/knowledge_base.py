import fitz  # PyMuPDF
import pdfplumber
import pandas as pd
from typing import List, Dict, Any
from pathlib import Path

# Import configurations and manual data
from .config import PDF_PATH, COMPLEXITY_MAP_PATH
from .manual_extractions import MANUAL_CONTENT

def extract_text_with_pymupdf(pdf_path: Path, page_number: int) -> str:
    """Extracts all text from a single page using PyMuPDF."""
    try:
        doc = fitz.open(pdf_path)
        page = doc.load_page(page_number - 1)
        text = page.get_text("text") # type: ignore
        doc.close()
        return text
    except Exception as e:
        return f"Error extracting page {page_number}: {e}"

def extract_tables_with_pdfplumber(pdf_path: Path, page_number: int) -> List[Dict[str, Any]]:
    """Extracts all tables from a single page into a list of JSON-serializable objects."""
    tables_content = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            page = pdf.pages[page_number - 1]
            extracted_tables = page.extract_tables()
            if not extracted_tables:
                return []
            for i, table in enumerate(extracted_tables):
                if not table or len(table) == 0: 
                    continue
                header = table[0]
                if not all(h is not None for h in header): 
                    continue
                table_data = [dict(zip(header, row)) for row in table[1:]]
                tables_content.append({"table_index": i, "data": table_data})
        return tables_content
    except Exception as e:
        return [{"error": f"Could not process tables on page {page_number}: {e}"}]

def get_manual_extraction(fot_page: int) -> Dict[str, Any]:
    """Retrieves a manually extracted content block by its FOT page number."""
    for key, value in MANUAL_CONTENT.items():
        if str(fot_page) in key:
            return value
    return {"error": f"No manual content found for FOT page {fot_page}"}


def build_knowledge_base() -> List[Dict[str, Any]]:
    """
    Main function to process all source documents according to the complexity map.
    It now correctly handles single pages and page ranges (e.g., '45-49').
    """
    print("--- Starting Knowledge Base Construction ---")
    
    if not COMPLEXITY_MAP_PATH.exists():
        print(f"ERROR: Complexity map not found at {COMPLEXITY_MAP_PATH}")
        return []

    try:
        columns_to_use = ["FOT Page", "Content Type", "Proposed Tool"]
        df = pd.read_csv(COMPLEXITY_MAP_PATH, usecols=columns_to_use) # type: ignore
        complexity_map = df.dropna(subset=["FOT Page"]).copy()
    except Exception as e:
        print(f"Error loading or parsing CSV: {e}")
        return []
    
    knowledge_base = []
    print(f"Loaded complexity map. Processing {len(complexity_map)} entries...")

    # Iterate through the map to drive the extraction process
    for index, row in complexity_map.iterrows():
        fot_page_str = str(row['FOT Page']).strip()
        tool = str(row['Proposed Tool']).strip()
        
        page_numbers_to_process = []
        
        if '-' in fot_page_str:
            try:
                start_str, end_str = fot_page_str.split('-')
                start = int(start_str.strip())
                end = int(end_str.strip())
                page_numbers_to_process.extend(range(start, end + 1))
            except ValueError:
                print(f"WARNING: Could not parse page range '{fot_page_str}'. Skipping row.")
                continue
        else:
            try:
                page_numbers_to_process.append(int(fot_page_str))
            except ValueError:
                print(f"WARNING: Could not parse page number '{fot_page_str}'. Skipping row.")
                continue

        # Process each page determined (either single or from a range)
        for page_num in page_numbers_to_process:
            print(f"Processing FOT Page {page_num} using tool: {tool}")

            content_block = {
                "source_document": PDF_PATH.name,
                "fot_page": page_num,
                "extraction_tool": tool,
                "content": None
            }
            
            tools_to_run = [t.strip() for t in tool.split(',')]
            extracted_content = {}

            if "Manual" in tools_to_run:
                extracted_content["manual"] = get_manual_extraction(page_num)
            if "PyMuPDF" in tools_to_run:
                extracted_content["text"] = extract_text_with_pymupdf(PDF_PATH, page_num)
            if "pdfplumber" in tools_to_run:
                tables = extract_tables_with_pdfplumber(PDF_PATH, page_num)
                if tables: # Only add tables if they are found
                    extracted_content["tables"] = tables
            
            # Simplify content structure if only one tool was used
            if len(extracted_content) == 1:
                content_block["content"] = list(extracted_content.values())[0]
            # Handle cases where no content was extracted
            elif not extracted_content:
                content_block["content"] = "No content extracted."
            else:
                content_block["content"] = extracted_content

            knowledge_base.append(content_block)

    print(f"--- Knowledge base construction complete. {len(knowledge_base)} total pages processed. ---")
    return knowledge_base
