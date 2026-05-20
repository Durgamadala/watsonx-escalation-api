from fastapi import FastAPI
from pydantic import BaseModel
import random
import smtplib
from email.mime.text import MIMEText

app = FastAPI(title="Escalation API", version="1.0.0")


class EscalationRequest(BaseModel):
    employee_name: str
    department: str
    issue: str
    status: str
    email: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/escalate")
def escalate(data: EscalationRequest):

    # Dynamic Ticket ID
    ticket_id = f"INC{random.randint(10000,99999)}"

    # Email configuration
    sender_email = "durga01.madala@gmail.com"
    sender_password = "iyhx lspm bhxo dlka"

    subject = f"IT Support Ticket Created - {ticket_id}"

    body = f"""
Hello {data.employee_name},

Your IT issue has been successfully escalated.

Ticket Details:
-------------------------
Ticket ID: {ticket_id}
Department: {data.department}
Issue: {data.issue}
Status: {data.status}

Our support team will contact you shortly.

Regards,
IT Support Team
"""

    # Send email
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = data.email

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, data.email, msg.as_string())
        server.quit()

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "message": "Issue escalated successfully and email sent",
        "received_data": data.dict()
    }
