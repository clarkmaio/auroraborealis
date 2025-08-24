


import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.resolve()))



from fastapi import FastAPI
from src.data.scraper import DataScraper
from datetime import datetime, timedelta
import pandas as pd
import json
from typing import Dict, List


app = FastAPI()

def from_df_to_json(df: pd.DataFrame) -> Dict:
    '''Convert DataFrame to JSON ready to be returned by API'''
    df['valuedate'] = df['valuedate'].astype(str) 
    json_data = df.to_json(orient='records')
    json_data = json.loads(json_data)
    return json_data

@app.get("/")
async def root():
    return {"message": "Welcome in Aurora Borealis API!"}

@app.get("/get_history")
async def get_history() -> Dict:
    #raw_data = DataScraper().load_data()
    #return from_df_to_json(df=raw_data)
    return {'message': 'history'}

@app.get("/get_interval", response_model=List[dict])
async def get_interval(start: str, end: str):
    start_date = pd.to_datetime(start, format='%Y%m%d')
    end_date = pd.to_datetime(end, format='%Y%m%d').replace(hour=23)
    interval = DataScraper().load_data(start_date=start_date, end_date=end_date)
    return from_df_to_json(df=interval)

@app.get("/get_lastdays", response_model=List[dict])
async def get_lastdays(days: int):
    end_date = datetime.now().replace(minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=days)
    interval = DataScraper().load_data(start_date=start_date, end_date=end_date)
    return from_df_to_json(df=interval)




