from typing import TypedDict, List, Optional, Dict, Any


class HRGraphState(TypedDict):
    # user input
    user_query: str

    # routing
    agent_type: Optional[str]

    # RAG / DB outputs
    retrieved_docs: Optional[List[Dict[str, Any]]]
    db_results: Optional[List[Dict[str, Any]]]

    # final response
    final_answer: Optional[str]
