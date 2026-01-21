# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from pydantic import BaseModel, Field

# # -----------------------------------
# # Structured output schema
# # -----------------------------------

# class RouteDecision(BaseModel):
#     agent: str = Field(
#         description="Which agent should handle the request",
#         enum=["policy", "employee", "resume", "interview", "decision"]
#     )
#     confidence: float = Field(
#         description="How confident you are (0 to 1)"
#     )

# # -----------------------------------
# # Ambiguous / meaningless queries
# # -----------------------------------

# AMBIGUOUS_QUERIES = {
#     "analyze this",
#     "tell me something",
#     "help",
#     "hi",
#     "hello",
#     "what",
#     "why",
#     "ok",
#     "okay",
#     "explain",
#     "hmm",
# }


# ROUTER_PROMPT = """ 
# You are an HR intent classifier.

# Your task is to determine the user's INTENT — not to match keywords.

# This system has TWO strictly separate data sources:
# 1) Company employees (people currently working in the company)
# 2) Job candidates (people whose resumes are stored)

# A person mentioned in a resume is NOT an employee unless the user explicitly states they are employed.

# --------------------------------------------------
# AVAILABLE AGENTS
# --------------------------------------------------

# policy  
# → Questions about company rules, limits, rights, benefits, leave, payroll, probation, holidays, or HR procedures.
# → Questions asking WHAT the policy allows, says, defines, or restricts.

# employee  
# → Looking up, listing, filtering, counting, or checking people who currently work in the company.
# → Includes role, department, experience, skills, activity status, or tenure of employees.

# resume  
# → Looking up, comparing, or analyzing job candidates.
# → Includes resumes, candidate skills, experience, projects, tools, or comparisons between candidates.

# interview  
# → Asking for interview questions, hiring preparation, interview evaluation, or assessment guidance.

# decision  
# → Applying rules or judgment to a SPECIFIC employee.
# → Includes promotions, eligibility, approvals, or compliance decisions for a named employee.

# --------------------------------------------------
# CRITICAL ROUTING RULES (READ CAREFULLY)
# --------------------------------------------------

# • Do NOT route by keywords alone — reason about the user's intent.

# • A candidate (resume) and an employee are NEVER the same unless explicitly stated.

# • If the user asks to list, find, filter, or count employees → ALWAYS use employee.

# • If the user asks WHAT a company rule or policy says or allows → policy.

# • If the user asks to APPLY policy or rules to a specific employee → decision.

# • Promotion policy questions (general) → policy  
# • Promotion eligibility of a named employee → decision

# • Hiring, shortlisting, or choosing candidates → resume.

# • Comparing or analyzing candidates WITHOUT choosing → resume.

# • Interview preparation or evaluation → interview.

# • If the request is vague, ambiguous, or cannot be answered directly → decision.

# --------------------------------------------------
# User query:
# {query}
# """


# # -----------------------------------

# def supervisor_agent(llm):
#     parser = JsonOutputParser(pydantic_object=RouteDecision)

#     prompt = ChatPromptTemplate.from_template(
#         ROUTER_PROMPT + "\n{format_instructions}"
#     ).partial(format_instructions=parser.get_format_instructions())

#     chain = prompt | llm | parser

#     def run(state):
#         query = state["user_query"].strip().lower()

#         # -------------------------------
#         # 1️⃣ Absolute ambiguity guardrail
#         # -------------------------------
#         if query in AMBIGUOUS_QUERIES or len(query.split()) <= 2:
#             state["agent_type"] = "decision"
#             state["route_confidence"] = 0.50
#             print("🧭 Routed → decision (forced: ambiguous)")
#             return state

#         # -------------------------------
#         # 2️⃣ Ask the LLM
#         # -------------------------------
#         result = chain.invoke({"query": query})

#         agent = result["agent"]
#         confidence = float(result["confidence"])

#         # -------------------------------
#         # 3️⃣ ACC safety gate
#         # -------------------------------
#         if confidence < 0.65:
#             agent = "decision"

#         # -------------------------------
#         # Save state
#         # -------------------------------
#         state["agent_type"] = agent
#         state["route_confidence"] = confidence

#         print(f"🧭 Routed → {agent} (confidence={confidence:.2f})")
#         return state

#     return run



from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

# -----------------------------------
# Structured output schema
# -----------------------------------

class RouteDecision(BaseModel):
    agent: str = Field(
        description="Which agent should handle the request",
        enum=["policy", "employee", "resume", "interview", "decision"]
    )
    confidence: float = Field(
        description="How confident you are (0 to 1)"
    )

# -----------------------------------
# Ambiguous / meaningless queries
# -----------------------------------

AMBIGUOUS_QUERIES = {
    "analyze this",
    "tell me something",
    "help",
    "hi",
    "hello",
    "what",
    "why",
    "ok",
    "okay",
    "explain",
    "hmm",
}


ROUTER_PROMPT = """
You are an HR INTENT CLASSIFIER.

Your task is to identify the USER'S INTENT — not to match keywords.

This system has TWO completely separate data domains:
1) Employees → people currently working in the company
2) Candidates → people whose resumes are stored for hiring

A person mentioned in a resume is NOT an employee unless explicitly stated.

--------------------------------------------------
AVAILABLE AGENTS
--------------------------------------------------

policy
→ Questions about company rules, policies, eligibility criteria, limits, benefits, leave, payroll,
  probation, holidays, compliance, or HR procedures.
→ Questions asking WHAT the policy says, allows, defines, or restricts.

employee
→ Looking up, listing, filtering, counting, or checking employees currently working in the company.
→ Includes role, department, skills, experience, tenure, status, or employee records.
→ Employee IDs (e.g., ACM123) ALWAYS indicate employees.

resume
→ Looking up, comparing, analyzing, or shortlisting job candidates.
→ Includes resumes, candidate skills, experience, projects, tools, or comparisons between candidates.
→ Candidates are NEVER employees unless clearly stated.

interview
→ Interview preparation, interview questions, evaluation rubrics, assessment guidance,
  or hiring interview feedback.

decision
→ Applying policies, rules, or judgment to a SPECIFIC employee.
→ Includes promotion eligibility, approvals, compliance decisions, warnings,
  or HR actions for a named employee.

--------------------------------------------------
CRITICAL ROUTING RULES (MUST FOLLOW)
--------------------------------------------------

• Reason about INTENT — do NOT rely on keywords alone.

• Employees and candidates are NEVER the same entity.

• If the user asks to LIST, FIND, FILTER, or COUNT employees → employee

• If the user asks WHAT a policy or rule says or allows → policy

• If the user asks to APPLY a policy to a specific employee → decision

• Promotion rules in general → policy
• Promotion eligibility of a named employee → decision

• Hiring, shortlisting, or choosing candidates → resume

• Comparing or analyzing candidates WITHOUT making a decision → resume

• Interview preparation or evaluation → interview

• If the query is vague, ambiguous, or requires judgment → decision

--------------------------------------------------
User Query:
{query}
"""


# -----------------------------------

def supervisor_agent(llm):
    parser = JsonOutputParser(pydantic_object=RouteDecision)

    prompt = ChatPromptTemplate.from_template(
        ROUTER_PROMPT + "\n{format_instructions}"
    ).partial(format_instructions=parser.get_format_instructions())

    chain = prompt | llm | parser

    def run(state):
        query = state["user_query"].strip().lower()

        # -------------------------------
        # 1️⃣ Absolute ambiguity guardrail
        # -------------------------------
        if query in AMBIGUOUS_QUERIES or len(query.split()) <= 2:
            state["agent_type"] = "decision"
            state["route_confidence"] = 0.50
            print("🧭 Routed → decision (forced: ambiguous)")
            return state

        # -------------------------------
        # 2️⃣ Ask the LLM
        # -------------------------------
        result = chain.invoke({"query": query})

        agent = result["agent"]
        confidence = float(result["confidence"])

        # -------------------------------
        # 3️⃣ ACC safety gate
        # -------------------------------
        if confidence < 0.65:
            agent = "decision"

        # -------------------------------
        # Save state
        # -------------------------------
        state["agent_type"] = agent
        state["route_confidence"] = confidence

        print(f"🧭 Routed → {agent} (confidence={confidence:.2f})")
        return state

    return run




# from langchain_core.prompts import ChatPromptTemplate
# from langchain_core.output_parsers import JsonOutputParser
# from pydantic import BaseModel, Field

# AMBIGUOUS_QUERIES = {
#     "analyze this", "tell me something", "help", "hi", "hello",
#     "what", "why", "ok", "okay", "explain", "hmm"
# }

# class RouteDecision(BaseModel):
#     agent: str = Field(enum=["policy", "employee", "resume", "interview", "decision"])
#     confidence: float

# ROUTER_PROMPT = """
# You are an HR intent classifier.

# Choose ONE agent strictly.

# policy → company rules, leave, probation, promotion policy
# employee → current employees only
# resume → candidates / resumes
# interview → interview questions
# decision → apply policy to a specific employee

# If vague or unclear → decision

# User query:
# {query}
# """

# def supervisor_agent(llm):
#     parser = JsonOutputParser(pydantic_object=RouteDecision)
#     prompt = ChatPromptTemplate.from_template(
#         ROUTER_PROMPT + "\n{format_instructions}"
#     ).partial(format_instructions=parser.get_format_instructions())

#     chain = prompt | llm | parser

#     def run(state):
#         query = state["user_query"].strip().lower()

#         if query in AMBIGUOUS_QUERIES or len(query.split()) <= 2:
#             state["agent_type"] = "decision"
#             return state

#         result = chain.invoke({"query": query})
#         agent = result["agent"]
#         confidence = float(result["confidence"])

#         if confidence < 0.65:
#             agent = "decision"

#         state["agent_type"] = agent
#         return state

#     return run
