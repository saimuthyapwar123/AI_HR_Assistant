# app/graph/policy_agent.py

def policy_agent(retriever, llm):
    def run(state):
        query = state["user_query"]

        if retriever is None:
            state["final_answer"] = "No HR policy documents are available."
            return state

        docs = retriever.invoke(query)

        if not docs:
            state["final_answer"] = "The policy does not specify this."
            return state

        context = "\n\n".join(d.page_content for d in docs)

        prompt = f"""
You are an HR Policy Rule Engine.

Rules:
1. You may apply rules ONLY if explicitly written.
2. You may NOT invent exceptions.
3. If the question involves something NOT mentioned in policy (like maternity, disability, special cases),
   you MUST say: "The policy does not specify this."
4. Never answer Yes/No unless policy explicitly allows or denies it.

Policy:
{context}

Question:
{query}

Format:
- Relevant policy rule:
- Condition check:
- Final answer:
"""

        answer = llm.invoke(prompt)
        state["final_answer"] = answer.content
        return state

    return run


