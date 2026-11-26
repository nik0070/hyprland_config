from src.state.agent_state import AgentState
from src.llm.llm_client import get_llm
from langchain_core.prompts import PromptTemplate

def report_gen_node(state:AgentState) -> dict:
    print("\n[Reporter] Generating final trading thesis...")
    llm = get_llm()

    prompt = PromptTemplate.from_template(
        """You are an algorithmic trading analyst. Write a concise daily trading report in Markdown.

        MACRO SECTOR ANALYSIS:
        {sectors}

        STOCKS PICKED FROM SECTORS:

        STOCKS WITH EARNINGS TODAY:

        FUNDAMENTAL DATA FROM ALL PICKS: """)
