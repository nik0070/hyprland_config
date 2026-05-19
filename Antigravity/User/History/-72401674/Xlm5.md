# TODO: Trading Agent Core Logic

- [x] Refactor `AgentState` in `src/state/agent_state.py` for automated workflow
- [x] Create `src/langgraph_nodes/market_intel_node.py` (News + Bills analyzer)
- [x] Create `src/langgraph_nodes/sector_catalyst_node.py` (Filters universe of stocks → `sector_picks`)
- [x] Create `src/langgraph_nodes/earnings_catalyst_node.py` (Track 2: Identifies upcoming earnings → `earnings_picks`)
- [ ] Create `src/langgraph_nodes/fundamental_check_node.py` (Merger + Financials reader + API fetch)
- [ ] Create `src/langgraph_nodes/report_gen_node.py` (Markdown formatter)
- [ ] Update `main.py` to wire the full dual-track DAG
- [ ] Add file writing logic to `main.py` to save `reasoning.md`
- [ ] Test with a sample news file and financial CSV
