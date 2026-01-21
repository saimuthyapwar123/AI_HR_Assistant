# # app/graph/decision_agent.py

# from app.graph.state import HRGraphState
# from app.db.mongo import get_collection


# def decision_agent(llm):
#     employees_col = get_collection("employees")

#     def _run(state: HRGraphState) -> HRGraphState:
#         query = state["user_query"].strip().lower()
#         employees = list(
#                         employees_col.find(
#                             {
#                                 "employee_id": {"$exists": True},
#                                 "is_active": True
#                             },
#                             {"_id": 0}
#                         )
#                     )

#         # 🛑 Guard: ambiguous or generic queries
#         AMBIGUOUS = {
#             "help me",
#             "help me with hr",
#             "analyze this",
#             "explain this",
#             "tell me something",
#         }

#         if query in AMBIGUOUS or len(query.split()) < 3:
#             state["final_answer"] = (
#                 "Please clarify your request.\n\n"
#                 "I can help with:\n"
#                 "• HR policy questions\n"
#                 "• Promotion or eligibility decisions\n"
#                 "• Resume screening\n"
#                 "• Interview preparation\n"
#                 "• Employee-related decisions"
#             )
#             return state

#         # 🛑 Guard: no employee data
#         if not employees:
#             state["final_answer"] = (
#                 "No employee data is available in the system. "
#                 "Please add employee records before making HR decisions."
#             )
#             return state

#         # ✅ Valid decision-making scenario
#         prompt = f"""
#                 You are an HR decision-making assistant.

#                 AVAILABLE DATA SOURCES:
#                 - Employee data (primary source)
#                 - HR policy rules (if explicitly provided)
#                 - Resume data (ONLY if explicitly provided)

#                 STRICT RULES:
#                 - Use employee data as the PRIMARY source.
#                 - Use policy data ONLY if a relevant policy is explicitly available.
#                 - Use resume data ONLY if the question explicitly involves candidates or resumes.
#                 - NEVER assume policy rules.
#                 - NEVER infer skills or experience not written.
#                 - If required policy or resume data is missing, clearly say so.
#                 - If data is insufficient, do NOT provide a recommendation.

#                 Question:
#                 {state["user_query"]}

#                 Employee Data:
#                 {employees}

#                 (Policy or resume data may be empty or unavailable.)
#         """

#         answer = llm.invoke(prompt)

#         state["db_results"] = employees
#         state["final_answer"] = answer.content
#         return state

#     return _run





# app/graph/decision_agent.py

from app.graph.state import HRGraphState
from app.db.mongo import get_collection


def decision_agent(llm, policy_retriever, resume_retriever):
    employees_col = get_collection("employees")

    PROMOTION_KEYWORDS = {"promote", "promotion", "eligible"}
    POLICY_KEYWORDS = {"policy", "leave", "probation", "promotion"}
    RESUME_KEYWORDS = {"candidate", "resume", "shortlist", "hire", "compare"}

    def _run(state: HRGraphState) -> HRGraphState:
        query = state["user_query"].strip().lower()

        # ------------------------------------------------
        # 🛑 Guard: ambiguous queries
        # ------------------------------------------------
        if len(query.split()) < 3:
            state["final_answer"] = (
                "Please clarify your request.\n\n"
                "I can help with:\n"
                "• HR policy questions\n"
                "• Promotion or eligibility decisions\n"
                "• Resume screening\n"
                "• Interview preparation\n"
                "• Employee-related decisions"
            )
            return state

        # ------------------------------------------------
        # 1️⃣ Load employee data (PRIMARY SOURCE)
        # ------------------------------------------------
        employees = list(
            employees_col.find(
                {"employee_id": {"$exists": True}, "is_active": True},
                {"_id": 0}
            )
        )

        if not employees:
            state["final_answer"] = (
                "No employee data is available in the system."
            )
            return state

        # ------------------------------------------------
        # 2️⃣ Decide which sources are REQUIRED
        # ------------------------------------------------
        needs_policy = any(k in query for k in POLICY_KEYWORDS)
        needs_resume = any(k in query for k in RESUME_KEYWORDS)

        # Promotion ALWAYS requires policy
        if any(k in query for k in PROMOTION_KEYWORDS):
            needs_policy = True

        # ------------------------------------------------
        # 3️⃣ Fetch POLICY data if required
        # ------------------------------------------------
        policy_context = None
        if needs_policy:
            policy_docs = policy_retriever.invoke(query)

            if not policy_docs:
                state["final_answer"] = (
                    "The company policy required to make this decision is not specified."
                )
                return state

            policy_context = "\n\n".join(d.page_content for d in policy_docs)

        # ------------------------------------------------
        # 4️⃣ Fetch RESUME data if required
        # ------------------------------------------------
        resume_context = None
        if needs_resume:
            resume_docs = resume_retriever.invoke(query)

            if not resume_docs:
                state["final_answer"] = (
                    "Resume data is required for this decision but is not available."
                )
                return state

            resume_context = "\n\n".join(d.page_content for d in resume_docs)

        # ------------------------------------------------
        # 5️⃣ FINAL DECISION PROMPT (STRICT & SAFE)
        # ------------------------------------------------
        prompt = f"""
You are an enterprise HR decision explanation assistant.

CONTEXT:
A decision has already been evaluated using validated employee, policy, and resume data.
Your task is to clearly explain the outcome of that decision.

STRICT OUTPUT RULES:
- Do NOT display or repeat employee records.
- Do NOT display or quote policy rules or documents.
- Do NOT mention resumes unless explicitly asked.
- Do NOT describe internal data sources or retrieval.
- Do NOT assume missing information.
- Do NOT apply general HR best practices.
- Do NOT ask the user for more information.
- If the decision is a refusal, explain why at a high level.

RESPONSE STYLE:
- Professional HR tone.
- Clear and concise explanation.
- No bullet points or numbered lists.

Question:
{state["user_query"]}
"""

        

        # prompt = f"""
        #         You are an HR decision-making assistant.

        #         STRICT RULES:
        #         - Use employee data as the PRIMARY source.
        #         - Use policy data ONLY if provided below.
        #         - Use resume data ONLY if provided below.
        #         - NEVER assume missing rules or policies.
        #         - NEVER apply general HR practices.
        #         - If required data is missing, clearly refuse.

        #         Question:
        #         {state["user_query"]}

        #         Employee Data:
        #         {employees}

        #         Policy Data:
        #         {policy_context or "Not provided"}

        #         Resume Data:
        #         {resume_context or "Not provided"}
        #         """

        answer = llm.invoke(prompt)
        state["final_answer"] = answer.content
        return state

    return _run
