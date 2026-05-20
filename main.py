from fastapi import FastAPI
from pydantic import BaseModel
import random
import requests
import os

app = FastAPI(title="Watsonx Escalation API", version="1.0.0")


# =========================
# REQUEST MODEL
# =========================
class EscalationRequest(BaseModel):
    employee_name: str
    department: str
    issue: str
    status: str
    email: str


# =========================
# ENV VARIABLE (FROM RENDER)
# =========================
BREVO_API_KEY = os.getenv("BREVO_API_KEY")


# =========================
# HEALTH CHECK
# =========================
@app.get("/")
def home():
    return {"message": "Watsonx Escalation API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


# =========================
# ESCALATION ENDPOINT
# =========================
@app.post("/escalate")
def escalate(data: EscalationRequest):

    # Generate ticket ID
    ticket_id = f"INC{random.randint(10000, 99999)}"

    # Email subject
    subject = f"IT Support Ticket Created - {ticket_id}"

    # Email body
    html_content = f"""
    <html>
        <body>
            <h2>IT Support Escalation</h2>

            <p>Hello {data.employee_name},</p>

            <p>Your issue has been escalated successfully.</p>

            <h3>Ticket Details:</h3>

            <ul>
                <li><b>Ticket ID:</b> {ticket_id}</li>
                <li><b>Employee:</b> {data.employee_name}</li>
                <li><b>Department:</b> {data.department}</li>
                <li><b>Issue:</b> {data.issue}</li>
                <li><b>Status:</b> {data.status}</li>
            </ul>

            <p>Our IT support team will contact you shortly.</p>

            <br>
            <p>Regards,<br><b>IT Support Team</b></p>
        </body>
    </html>
    """

    # Brevo API endpoint
    url = "https://api.brevo.com/v3/smtp/email"

    # Headers
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    # Payload
    payload = {
        "sender": {
            "name": "IT Support",
            "email": "durga01.madala@gmail.com"
        },
        "to": [
            {
                "email": data.email,
                "name": data.employee_name
            }
        ],
        "subject": subject,
        "htmlContent": html_content
    }

    try:
        response = requests.post(url, json=payload, headers=headers)

        return {
            "status": "success",
            "ticket_id": ticket_id,
            "email_status": response.status_code,
            "message": "Issue escalated successfully and email sent"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "ticket_id": ticket_id
        }
