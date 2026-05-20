from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/escalate")
def escalate(data: dict):
    return {
        "status": "success",
        "ticket_id": "INC12345",
        "message": "Issue escalated successfully",
        "received_data": data
    }
