from src.state.agent_state import AgentState
import json
from src.llm.llm_client import get_llm
from langchain_core.prompts import PromptTemplate

def analyze_market_node(state: AgentState) -> dict:
    print("\n[Market Intel] Analyzing news for sector trends...")
    llm = get_llm()

    prompt = PromptTemplate.from_template(
        """You are a top-tier financial analyst. Read the following news summaries and identify 2-3 sectors that are currently 'Hot' (bullish).

        NEWS SUMMARIES:
        {news}

        OUTPUT FORMAT: You MUST return ONLY a raw JSON dictionary. No markdown formatting, no backticks.
        Example:
        {{
            "Technology": {{"reason": "New AI breakthroughs", "trend": "up"}},
            "Healthcare": {{"reason": "Favorable FDA regulations", "trend": "up"}}
        }}
        """
    )

    formatted_prompt = prompt.format(news=state.get("summaries", {}))
    response = llm.invoke(formatted_prompt)

    # Parse the llm output to save it to the STATE
    try:
        clean_text = response.content.strip().strip("```json").strip("```")
        sector_analysis = json.loads(clean_text)
    except: 
        print("Warning : LLM failed to output valid JSON. Falling back to empty dict.")
        sector_analysis = {}


    return {"sector_analysis": sector_analysis}


    