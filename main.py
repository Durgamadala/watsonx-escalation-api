from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -------------------
# Request schema
# -------------------
class EscalationRequest(BaseModel):
    employee_name: str
    department: str
    issue: str
    status: str

# -------------------
# Health check
# -------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -------------------
# Escalation API
# -------------------
@app.post("/escalate")
def escalate(data: EscalationRequest):
    return {
        "status": "success",
        "ticket_id": "INC12345",
        "message": "Issue escalated successfully",
        "received_data": data.dict()
    }
