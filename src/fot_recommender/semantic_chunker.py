import collections
from typing import List, Dict, Any

def _serialize_table_to_markdown(table_data: List[Dict[str, Any]]) -> str:
    """
    Converts a list of dictionaries (representing a table) into a Markdown string.
    Assumes the first dictionary in the list contains the headers.
    """
    if not table_data:
        return ""

    # Extract headers from the first row
    headers = table_data[0].keys()
    
    # Create Markdown header row and separator row
    md_header = "| " + " | ".join(headers) + " |"
    md_separator = "|-" + "-|-".join(['-' * len(h) for h in headers]) + "-|" # Basic separator

    # Create Markdown data rows
    md_rows = [md_header, md_separator]
    for row_dict in table_data:
        # Ensure all keys from headers are present, even if with None values
        row_values = [str(row_dict.get(header, '')) for header in headers]
        md_rows.append("| " + " | ".join(row_values) + " |")
    
    return "\n".join(md_rows)

def chunk_by_concept(raw_knowledge_base: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Groups items from the raw knowledge base by a composite key of 
    (source_document, concept) to create high-quality, coherent semantic chunks.
    Includes table data serialization for embedding.

    Args:
        raw_knowledge_base: A list of dictionaries, where each dict represents a page 
                            or a piece of content from the source documents.

    Returns:
        A list of consolidated dictionaries, where each represents a semantic chunk.
    """
    grouped_by_source_and_concept = collections.defaultdict(list)
    for item in raw_knowledge_base:
        composite_key = (item['source_document'], item['concept'])
        grouped_by_source_and_concept[composite_key].append(item)

    final_chunks = []
    for (source_doc, concept), items in grouped_by_source_and_concept.items():
        items.sort(key=lambda x: x.get('absolute_page', 0))

        # Collect all content and any table data
        all_content_parts = []
        for item in items:
            if item.get('content'):
                all_content_parts.append(item['content'])
            if item.get('table_data'):
                # Serialize table data to Markdown and add it as a content part
                table_md = _serialize_table_to_markdown(item['table_data'])
                if table_md: # Only add if serialization produced something
                    all_content_parts.append(f"\nExample Table:\n{table_md}")
        
        combined_content = "\n\n".join(all_content_parts).strip()
        
        pages = sorted(list(set(item['absolute_page'] for item in items if 'absolute_page' in item)))
        page_str = f"Pages: {', '.join(map(str, pages))}" if pages else "N/A"
        
        # Prepend title to content for embedding
        content_for_embedding = f"Title: {concept}. Content: {combined_content}"
        
        final_chunk = {
            "title": concept,
            "source_document": source_doc,
            "fot_pages": page_str,
            "content_for_embedding": content_for_embedding,
            "original_content": combined_content # Keep original for potential display
        }
        final_chunks.append(final_chunk)
        
    return final_chunks