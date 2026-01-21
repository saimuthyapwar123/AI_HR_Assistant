# app/graph/graph_builder.py
from langgraph.graph import StateGraph, END
from app.graph.state import HRGraphState


def build_hr_graph(
    supervisor,
    policy,
    employee,
    resume,
    interview,
    decision,
    checkpointer=None,
):
    graph = StateGraph(HRGraphState)

    # -----------------
    # Register nodes
    # -----------------
    graph.add_node("supervisor", supervisor)
    graph.add_node("policy", policy)
    graph.add_node("employee", employee)
    graph.add_node("resume", resume)
    graph.add_node("interview", interview)
    graph.add_node("decision", decision)

    # -----------------
    # Entry point
    # -----------------
    graph.set_entry_point("supervisor")

    # -----------------
    # Conditional routing (SAFE)
    # -----------------
    def route(state: HRGraphState) -> str:
        """
        Decide next node safely.
        Default fallback → decision agent
        """
        agent = state.get("agent_type")

        if agent in {"policy", "employee", "resume", "interview", "decision"}:
            return agent

        # Fallback if supervisor output is invalid
        return "decision"

    graph.add_conditional_edges(
        "supervisor",
        route,
        {
            "policy": "policy",
            "employee": "employee",
            "resume": "resume",
            "interview": "interview",
            "decision": "decision",
        },
    )

    # -----------------
    # Terminate all agent nodes
    # -----------------
    for node in ("policy", "employee", "resume", "interview", "decision"):
        graph.add_edge(node, END)

    # -----------------
    # Compile with checkpointing
    # -----------------
    return graph.compile(checkpointer=checkpointer)
