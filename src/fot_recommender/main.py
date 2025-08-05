import pprint
from fot_recommender.knowledge_base import build_knowledge_base

def main():
    """
    Main entry point for the FOT Intervention Recommender application.
    """
    print("--- FOT Intervention Recommender ---")
    
    knowledge_base = build_knowledge_base()
    
    if knowledge_base:
        print(f"\nSuccessfully built knowledge base with {len(knowledge_base)} items.")
        print("\n--- Sample of First Extracted Intervention ---")
        # Pretty-print the first item to verify its structure
        pprint.pprint(knowledge_base[0])
        print("--------------------------------------------")
    else:
        print("\nKnowledge base construction returned 0 items. Check implementation.")

    print("\nNext steps: Implement Phase 2 (RAG Pipeline)...")

if __name__ == "__main__":
    main()
