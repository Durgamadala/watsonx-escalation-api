from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

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


# 🔥 ADD THIS NEW ENDPOINT (IMPORTANT)
@app.get("/watsonx-openapi")
def watsonx_openapi():
    return {
        "openapi": "3.0.0",
        "info": {
            "title": "Escalation API",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "https://watsonx-escalation-api.onrender.com"
            }
        ],
        "paths": {
            "/escalate": {
                "post": {
                    "operationId": "escalate",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "employee_name": {"type": "string"},
                                        "department": {"type": "string"},
                                        "issue": {"type": "string"},
                                        "status": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "OK"
                        }
                    }
                }
            }
        }
    }
