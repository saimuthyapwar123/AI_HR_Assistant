# app/run_graph.py


from app.llm.llm import get_gemini_llm,get_groq_llm
from app.graph.graph_builder import build_hr_graph
from app.graph.supervisor import supervisor_agent
from app.graph.policy_agent import policy_agent
from app.graph.employee_agent import employee_agent
from app.graph.resume_agent import resume_agent
from app.graph.interview_agent import interview_agent
from app.graph.decision_agent import decision_agent
# from app.vector_store.chroma_store import get_retriever
from app.vector_store.policy_store import get_policy_retriever
from app.vector_store.resume_store import get_resume_retriever

from app.checkpoint.mongo_checkpointer import get_mongo_checkpointer


policy_retriever = get_policy_retriever()
resume_retriever = get_resume_retriever()


gemini_llm = get_gemini_llm()
groq_llm = get_groq_llm()

# try:
#     claude_llm = get_claude_llm()
# except Exception as e:
#     print("⚠️ Claude disabled:", e)
#     claude_llm = None


def main():
    # llm = get_gemini_llm()
    # retriever = get_retriever()
    checkpointer = get_mongo_checkpointer()

    # supervisor_llm = claude_llm or gemini_llm

    graph = build_hr_graph(
        supervisor=supervisor_agent(groq_llm),
        policy=policy_agent(policy_retriever, groq_llm),
        resume=resume_agent(resume_retriever, groq_llm),
        employee=employee_agent(groq_llm),
        interview=interview_agent(groq_llm),
        decision=decision_agent(
                    groq_llm,
                    policy_retriever=policy_retriever,
                    resume_retriever=resume_retriever
                ),
        checkpointer=checkpointer,
    )



    thread_id = "user_123"

    print("🤖 HR Assistant Ready (type exit to quit)")

    while True:
        query = input("Query : ").strip()
        if query.lower() in {"exit", "quit"}:
            break

        result = graph.invoke(
            {"user_query": query},
            config={"configurable": {"thread_id": thread_id}}
        )

        print("\n🧠 Response:\n", result["final_answer"])
        print("-" * 50)


if __name__ == "__main__":
    main()
