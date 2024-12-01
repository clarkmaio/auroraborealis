from fastapi import FastAPI
from src.data.scraper import DataScraper
from datetime import datetime
import pandas as pd
import json
from typing import Dict, List

ds = DataScraper()
app = FastAPI()


def from_df_to_json(df: pd.DataFrame) -> Dict:
    df['valuedate'] = df['valuedate'].astype(str) 
    json_data = df.to_json(orient='records')
    json_data = json.loads(json_data)
    return json_data

@app.get("/")
async def root():
    return {"message": "Welcome in Aurora Borealis API!"}

@app.get("/get_history", response_model=List[dict])
def get_history() -> Dict:
    raw_data = ds.load_data()
    return from_df_to_json(df=raw_data)
    #return {'Output': 'this'}

@app.get("/get_interval", response_model=List[dict])
def get_interval(start: str, end: str):
    start_date = pd.to_datetime(start, format='%Y%m%d')
    end_date = pd.to_datetime(end, format='%Y%m%d').replace(hour=23)
    interval = ds.load_data(start_date=start_date, end_date=end_date)
    return from_df_to_json(df=interval)



if __name__ == '__main__':
    raw_data = ds.load_data().head(10)
    d = from_df_to_json(df=raw_data)