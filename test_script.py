import pandas as pd
df = pd.DataFrame({"source": [1], "log_message": [2]})
try:
    pd.read_csv(df)
except Exception as e:
    import traceback
    traceback.print_exc()

