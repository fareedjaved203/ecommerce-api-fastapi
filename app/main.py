from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "E commerce backend is running!"}