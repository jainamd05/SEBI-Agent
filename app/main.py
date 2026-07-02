from fastapi import FastAPI

app = FastAPI(
    title="SEBI AI Agent",
    description="Backend API for SEBI TechSprint",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "SEBI AI Agent Backend is Running",
        "status": "success",
        "version": "1.0.0",
    }