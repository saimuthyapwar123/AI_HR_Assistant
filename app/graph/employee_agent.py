
# from app.db.mongo import get_collection

# def employee_agent(llm):
#     employees_col = get_collection("employees")

#     def run(state):
#         employees = list(
#                         employees_col.find(
#                             {
#                                 "employee_id": {"$exists": True},
#                                 "is_active": True
#                             },
#                             {"_id": 0}
#                         )
#                     )


#         if not employees:
#             state["final_answer"] = "No employee data is available."
#             return state

#         prompt = f"""
#             You are an HR employee assistant.

#             You can ONLY use company employee data.
#             Employee skills come ONLY from the "skills" field in employee records.

#             STRICT RULES:
#             - Respond ONLY in plain English (no Python code).
#             - Do NOT explain how filtering works.
#             - Do NOT assume resume skills apply to employees.
#             - NEVER mention resumes unless the user explicitly asks about candidates or resumes.
#             - If a requested skill does not exist in employee data, clearly say so.
#             - If no employee matches, respond with a short explanation.

#             Employee Data:
#             {employees}

#             Question:
#             {state["user_query"]}
#        """



#         answer = llm.invoke(prompt)
#         state["final_answer"] = answer.content
#         return state

#     return run



from app.db.mongo import get_collection

def employee_agent(llm):
    employees_col = get_collection("employees")

    def run(state):
        query = state["user_query"].lower().strip()

        # ====================================================
        # 1️⃣ DIRECT COUNT FROM MONGODB (NO DATA LOAD)
        # ====================================================
        if "how many" in query and "employee" in query:
            count = employees_col.count_documents(
                {
                    "employee_id": {"$exists": True},
                    "is_active": True
                }
            )

            state["final_answer"] = (
                f"There are {count} active employees in the company."
            )
            return state

        # ====================================================
        # 2️⃣ LOAD EMPLOYEE DATA ONLY IF REQUIRED
        # ====================================================
        employees = list(
            employees_col.find(
                {
                    "employee_id": {"$exists": True},
                    "is_active": True
                },
                {"_id": 0}
            )
        )

        if not employees:
            state["final_answer"] = "No employee data is available."
            return state

        # ====================================================
        # 3️⃣ FALLBACK TO LLM (REASONING / EXPLANATION)
        # ====================================================
        prompt = f"""
                You are an HR employee assistant.

                You can ONLY use company employee data.
                Employee skills come ONLY from the "skills" field in employee records.

                STRICT RULES:
                - Respond ONLY in plain English (no Python code).
                - Do NOT explain how filtering works.
                - Do NOT assume resume skills apply to employees.
                - NEVER mention resumes unless the user explicitly asks about candidates or resumes.
                - If a requested skill does not exist in employee data, clearly say so.
                - If no employee matches, respond with a short explanation.

                Employee Data:
                {employees}

                Question:
                {state["user_query"]}
                """

        answer = llm.invoke(prompt)
        state["final_answer"] = answer.content
        return state

    return run
