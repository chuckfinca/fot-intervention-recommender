import json
import pprint
from .config import RAW_KB_PATH

def main():
    """
    Main entry point for the FOT Intervention Recommender application.
    This version loads a pre-processed knowledge base directly from a JSON file.
    """
    print("--- FOT Intervention Recommender ---")
    
    # --- PHASE 1: LOAD PRE-PROCESSED KNOWLEDGE BASE ---
    print(f"Loading knowledge base from: {RAW_KB_PATH}")
    try:
        with open(RAW_KB_PATH, 'r', encoding='utf-8') as f:
            knowledge_base = json.load(f)
    except FileNotFoundError:
        print(f"FATAL ERROR: The knowledge base file was not found at {RAW_KB_PATH}")
        return
    except json.JSONDecodeError:
        print(f"FATAL ERROR: The file at {RAW_KB_PATH} is not a valid JSON file.")
        return
        
    print(f"Successfully loaded {len(knowledge_base)} items.")
    
    print("\n--- Sample of First Knowledge Base Item ---")
    if knowledge_base:
        pprint.pprint(knowledge_base[0])
    print("------------------------------------------")

    print("\nData loading is complete. Next step: Semantic Chunking.")


if __name__ == "__main__":
    main()