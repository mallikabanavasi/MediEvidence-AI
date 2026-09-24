from fastapi import FastAPI

from backend.api.reports import router as reports_router
from backend.api.clinical import router as clinical_router


app = FastAPI(
    title="MediEvidence AI"
)


app.include_router(
    reports_router,
    prefix="/reports"
)

app.include_router(
    clinical_router,
    prefix="/clinical"
)


@app.get("/")
def home():

    return {
        "message": "MediEvidence AI Backend is running successfully!"
    }