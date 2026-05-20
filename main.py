from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
