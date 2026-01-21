# app/graph/interview_agent.py

from app.graph.state import HRGraphState


def interview_agent(llm):
    def _run(state: HRGraphState) -> HRGraphState:
        query = state["user_query"]

        prompt = f"""
        Generate interview questions based on this requirement:
        {query}

        Include:
        - Technical questions
        - Scenario-based questions
        - Experience-based questions
        """

        answer = llm.invoke(prompt)

        state["final_answer"] = answer.content
        return state

    return _run
