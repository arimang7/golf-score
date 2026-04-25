import pandas as pd
import numpy as np

def analyze_trades(file_path):
    try:
        df = pd.read_csv(file_path)
        # basic metrics
        summary = {
            "count": len(df),
            "columns": list(df.columns),
            "is_empty": df.empty
        }
        return summary
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Create a dummy CSV for testing
    test_file = "/tmp/test_trades.csv"
    pd.DataFrame({
        "Date": ["2026-03-01", "2026-03-02"],
        "Symbol": ["AAPL", "TSLA"],
        "Type": ["Buy", "Sell"],
        "Price": [150.0, 200.0]
    }).to_csv(test_file, index=False)
    
    print(analyze_trades(test_file))
