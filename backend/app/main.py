from fastapi import FastAPI

app = FastAPI(title="PC Hub")

@app.get("/ok")
def root():
    return{"message": "All is ok"}