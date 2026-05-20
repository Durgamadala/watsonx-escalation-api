from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Escalation API", version="1.0.0")


class EscalationRequest(BaseModel):
    employee_name: str
    department: str
    issue: str
    status: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/escalate")
def escalate(data: EscalationRequest):
    return {
        "status": "success",
        "ticket_id": "INC12345",
        "message": "Issue escalated successfully",
        "received_data": data.dict()
    }
