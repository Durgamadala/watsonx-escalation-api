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

    # Generate Dynamic Ticket ID
    ticket_id = f"INC{random.randint(10000,99999)}"

    # Email Body
    body = f"""
Hello {data.employee_name},

Your issue has been escalated successfully.

Ticket ID: {ticket_id}
Department: {data.department}
Issue: {data.issue}

Our support team will reach out to you shortly.

Regards,
IT Support Team
"""

    # Your Gmail Credentials
    sender_email = "durga01.madala@gmail.com"
    sender_password = "iyhx lspm bhxo dlka"

    # Create Email
    msg = MIMEText(body)
    msg["Subject"] = "Issue Escalation Confirmation"
    msg["From"] = sender_email
    msg["To"] = data.email

    # Send Email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, data.email, msg.as_string())
    server.quit()

    return {
        "status": "success",
        "ticket_id": ticket_id,
        "message": "Issue escalated successfully and email sent",
        "received_data": data.dict()
    }
