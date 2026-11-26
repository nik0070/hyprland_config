import pandas as pd
from pathlib import Path
from graph import app

def main():
    print("Hello from trading-agent!")

    result = app.invoke({})
    print("\n✅ Graph executed successfully!")
    print("-" * 60)
    print(f'result keys : {result.keys()}')
    for name, summary in result.get("summaries", {}).items():
        print(f"📄 {name}: {summary['rows']} rows, columns={summary['columns']}")

    print("\nMarket Intel:")
    print(result.get("sector_analysis", {}))
    
    print("\nSector Picks:")
    print([p['company'] for p in result.get("sector_picks", [])])
    
    print("\nEarnings Picks:")
    print([p['company'] for p in result.get("earnings_picks", [])])

    print("\nFundamental Data Processed For:")
    print(list(result.get("financial_data", {}).keys()))

    final_report_text = result.get("final_report", "No report generated.")

    with open("reasoning.md", "w", encoding="utf-8") as f:
        f.write(final_report_text)

    print("\n📄 Final Report saved to reasoning.md")

if __name__ == "__main__":
    main()
