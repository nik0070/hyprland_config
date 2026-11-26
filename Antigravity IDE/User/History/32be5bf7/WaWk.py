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
        {sector_picks}

        STOCKS WITH EARNINGS TODAY:
        {earnings_picks}

        FUNDAMENTAL DATA FROM ALL PICKS: 
        {financials}
        
        Task: Write a thesis for today's market, Highlight the specific stocks picked, evaluate their PE, PB and other KPIs from their fundamental data, and give a final verdict (Bullish/Bearish/Hold) for each.

        """
        )
        
    formatted_prompt = prompt.format(
            sectors=state.get("sector_analysis", {}),
            sector_picks=state.get("sector_picks", {}),
            earnings_picks=state.get("earnings_picks", {}),
            financials=state.get("financial_data", {})
        )

    response = llm.invoke(formatted_prompt)
    return {"final_report": response.content}
