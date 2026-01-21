

# def resume_agent(retriever, llm):
#     def run(state):
#         query = state["user_query"]

#         if retriever is None:
#             state["final_answer"] = "No resume documents are available."
#             return state

#         docs = retriever.invoke(query)

#         if not docs:
#             state["final_answer"] = "No resumes match this query."
#             return state

#         context = "\n\n".join(d.page_content for d in docs)

#         prompt = f"""
# You are a Resume Analysis Engine.

# CRITICAL RULES:
# - Each resume belongs to one person only.
# - NEVER move skills between people.
# - NEVER assume two resumes share a skill unless both explicitly list it.
# - NEVER invent skills, projects, or experience.
# - If something is not written, say it is not mentioned.

# Resume Data:
# {context}

# Question:
# {query}

# Answer ONLY using the text above.
# """


#         answer = llm.invoke(prompt)
#         state["final_answer"] = answer.content
#         return state

#     return run



def resume_agent(retriever, llm):
    def run(state):
        query = state.get("user_query")

        if not retriever:
            state["final_answer"] = "No resume documents are available."
            return state

        docs = retriever.invoke(query)

        if not docs:
            state["final_answer"] = "No resumes match this query."
            return state

        # Preserve resume boundaries to avoid mixing
        context = ""
        for idx, doc in enumerate(docs, start=1):
            context += f"\n\n--- Resume {idx} ---\n{doc.page_content}"

        prompt = f"""
You are a STRICT Resume Analysis Engine.

ABSOLUTE RULES (DO NOT VIOLATE):
1. Each resume represents ONE unique individual.
2. NEVER mix, merge, or transfer information between resumes.
3. NEVER assume shared skills, projects, experience, or achievements.
4. Common information is valid ONLY if it appears explicitly in ALL relevant resumes.
5. NEVER invent, infer, or guess missing details.
6. If information is not written, respond exactly with: "Not mentioned".
7. Lifetime projects or total career experience must be derived ONLY from what is explicitly stated.

QUERY HANDLING:
- Respond ONLY to what the question asks.
- If the question refers to:
  • A single resume → Answer using ONLY that resume.
  • Multiple resumes → Answer SEPARATELY for each resume.
  • Common/shared data → Extract ONLY overlapping information explicitly present in ALL resumes.
- If no shared data exists, say: "No common information found".

RESPONSE FORMAT RULES:
- Clearly label responses (e.g., Resume 1, Resume 2).
- Do NOT summarize unless asked.
- Do NOT add explanations, opinions, or assumptions.
- Keep answers concise, factual, and text-extracted.

Resume Data:
{context}

Question:
{query}

FINAL INSTRUCTION:
Answer STRICTLY using the resume data above and follow ALL rules.
"""

        answer = llm.invoke(prompt)
        state["final_answer"] = answer.content.strip()
        return state

    return run
