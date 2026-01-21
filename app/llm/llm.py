import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

# --------------------------------------------------
# Common settings
# --------------------------------------------------
TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", 0.2))
# MAX_TOKENS = 2048


# --------------------------------------------------
# Gemini (Google)
# --------------------------------------------------
GOOGLE_MODEL = os.getenv(
    "GOOGLE_MODEL",
    "models/gemini-2.5-flash"
)


def get_gemini_llm():
    """
    Returns Google Gemini LLM
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError("❌ GOOGLE_API_KEY not set")

    print(f"🔵 Using Gemini model: {GOOGLE_MODEL}")

    return ChatGoogleGenerativeAI(
        model=GOOGLE_MODEL,
        temperature=TEMPERATURE
    )


# --------------------------------------------------
# Groq
# --------------------------------------------------
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"
)


def get_groq_llm():
    """
    Returns Groq LLM
    """
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("❌ GROQ_API_KEY not set")

    print(f"🟢 Using Groq model: {GROQ_MODEL}")

    return ChatGroq(
        model=GROQ_MODEL,
        temperature=TEMPERATURE
    )




# from langchain_anthropic import ChatAnthropic

# # --------------------------------------------------
# # Claude (Anthropic)
# # --------------------------------------------------
# CLAUDE_MODEL = os.getenv(
#     "CLAUDE_MODEL",
#     "claude-3-haiku-20240307"
# )

# def get_claude_llm():
#     """
#     Returns Anthropic Claude LLM
#     """
#     if not os.getenv("ANTHROPIC_API_KEY"):
#         raise RuntimeError("❌ ANTHROPIC_API_KEY not set")

#     print(f"🟣 Using Claude model: {CLAUDE_MODEL}")

#     return ChatAnthropic(
#         model=CLAUDE_MODEL,
#         temperature=TEMPERATURE
#     )

