# FastAPI app instance & route includes
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return{"Message: Hello, World!"}