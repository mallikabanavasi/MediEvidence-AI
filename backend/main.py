from fastapi import FastAPI

app = FastAPI(title="MediEvidence AI")


@app.get("/")
def home():
    return {
        "message": "MediEvidence AI Backend is running successfully!"
    }