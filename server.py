import pandas as pd

from fastapi import FastAPI, UploadFile, HTTPException,File
from fastapi.responses import FileResponse

from main import classify_csv_logs

app= FastAPI(title= "Log Classification API", description= "Classify logs using LLM, Embedding and Regex")

@app.post("/classify")
async def classify_logs(file: UploadFile= File(...)):
    try:
        if not file.filename.endswith(".csv"):
            raise HTTPException(status_code=400, detail= "Invalid file type. Please upload a CSV file.")
        
        df= pd.read_csv(file.file)
        if "source" not in df.columns or "log_message" not in df.columns:
            raise HTTPException(status_code=400, detail= "Invalid CSV file. Please upload a CSV file with 'source' and 'log_message' columns.")
        
        classified_df= classify_csv_logs(df)

        classified_df.to_csv("classified_logs.csv", index=False)

        return FileResponse("classified_logs.csv", media_type="text/csv", filename="classified_logs.csv")
    except Exception as e:
        raise HTTPException(status_code=500, detail= str(e))

    finally:
        file.close()

if __name__== "__main__":
    import uvicorn
    uvicorn.run(app, host= "localhost", port= 8000)



        


