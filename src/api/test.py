from fastapi import FastAPI, Query


app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}