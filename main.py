# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# # MongoDB init
# from app.db.mongo import get_mongo_client

# # Routers
# from app.router.employee_router import router as employee_router

# # LangGraph AI
# from app.llm.llm import get_groq_llm
# from app.graph.graph_builder import build_hr_graph
# from app.graph.supervisor import supervisor_agent
# from app.graph.policy_agent import policy_agent
# from app.graph.employee_agent import employee_agent
# from app.graph.resume_agent import resume_agent
# from app.graph.interview_agent import interview_agent
# from app.graph.decision_agent import decision_agent

# from app.vector_store.policy_store import get_policy_retriever
# from app.vector_store.resume_store import get_resume_retriever

# # ----------------------------------------------------
# # App
# # ----------------------------------------------------
# app = FastAPI(
#     title="Acme Technologies – AI HR Assistant",
#     version="1.0",
#     description="Enterprise AI HR system for Acme Technologies Pvt Ltd"
# )

# # CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ----------------------------------------------------
# # DB Init
# # ----------------------------------------------------
# get_mongo_client()

# # ----------------------------------------------------
# # Routers
# # ----------------------------------------------------
# app.include_router(employee_router, prefix="/api", tags=["Employees"])

# # ----------------------------------------------------
# # Load AI components
# # ----------------------------------------------------
# policy_retriever = get_policy_retriever()
# resume_retriever = get_resume_retriever()
# llm = get_groq_llm()

# graph = build_hr_graph(
#     supervisor=supervisor_agent(),
#     policy=policy_agent(policy_retriever, llm),
#     employee=employee_agent(llm),
#     resume=resume_agent(resume_retriever, llm),
#     interview=interview_agent(llm),
#     decision=decision_agent(llm)
# )

# # ----------------------------------------------------
# # AI Query Endpoint
# # ----------------------------------------------------
# @app.post("/api/hr/query")
# def ask_hr(query: str):
#     result = graph.invoke({"user_query": query})
#     return {
#         "company": "Acme Technologies Pvt Ltd",
#         "answer": result["final_answer"],
#         "agent": result["agent_type"]
#     }

# # ----------------------------------------------------
# # Health Check
# # ----------------------------------------------------
# @app.get("/")
# def root():
#     return {
#         "status": "running",
#         "company": "Acme Technologies Pvt Ltd",
#         "service": "AI HR Assistant"
#     }


from fastapi import FastAPI
from app.router.employee_router import router as employee_router

app = FastAPI(title="AI HR Assistant – Acme Technologies")

app.include_router(employee_router)
