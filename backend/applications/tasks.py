import smtplib,csv,os
from applications.workers import celery
from applications.models import User, HouseholdServiceRequest
from celery.schedules import crontab
from applications.models import *
from flask import current_app as app
from jinja2 import Template
from applications.mailer import send_email
from datetime import datetime, timedelta
from weasyprint import HTML
from io import StringIO
import calendar
# Define email server and credentials


# def get_html_report(username,data):
#     with open('/report.html', 'r') as file:
#         jinja_template=Template(file.read())
#         html_report=jinja_template.render(username,data)
#         return html_report

def generate_html_report(customer, requested_services, closed_services):
    with open('applications/report.html', 'r') as file:
        template = Template(file.read())
        return template.render(
            customer=customer,
            requested_services=requested_services,
            closed_services=closed_services,
            month_year=datetime.today().replace(day=1).strftime('%B %Y')
        )

@celery.task
def send_daily_reminder():
    with app.app_context():
        professionals = User.query.filter_by(role="service_professional").all()
        for professional in professionals:
            pending_requests = HouseholdServiceRequest.query.filter_by(
                service_professional_id=professional.id, status="pending"
            ).count()

            if pending_requests:
                # Send Email Reminder
                send_email(
                   professional.email,
                   "Daily Reminder",
                   f"Hello {professional.username},\n\nYou have {pending_requests} pending service requests. Please check and take necessary action."
                )
    
def send_email_with_pdf(to, subject, html_content, pdf_data, pdf_filename):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    sender = "noreply@example.com"
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject

    # Attach the HTML content
    msg.attach(MIMEText(html_content, "html"))

    # Attach the PDF
    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(pdf_data)
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition", f"attachment; filename={pdf_filename}"
    )
    msg.attach(attachment)

    # Send the email via MailHog
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)
@celery.task
def send_monthly_activity_report():
    with app.app_context():
        today = datetime.today()
        # First day of the current month
        first_day = today.replace(day=1)

        # Last day of the current month
        last_day = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        customers = User.query.filter_by(role="customer").all()
        
        for customer in customers:
            requested_services = HouseholdServiceRequest.query.filter(
                HouseholdServiceRequest.customer_id == customer.id,
                HouseholdServiceRequest.date_created.between(first_day, last_day)
            ).all()

            closed_services = HouseholdServiceRequest.query.filter(
                HouseholdServiceRequest.customer_id == customer.id,
                HouseholdServiceRequest.status == "closed",
                HouseholdServiceRequest.date_closed.between(first_day, last_day)
            ).all()

            report_html = generate_html_report(customer, requested_services, closed_services)
            pdf=HTML(string=report_html).write_pdf()
            send_email_with_pdf(
                to=customer.email,
                subject="Monthly Activity Report",
                html_content=report_html,
                pdf_data=pdf,
                pdf_filename="monthly_activity_report.pdf"
            )
          


@celery.task
def export_service_requests(sp_id):
    sp=User.query.get(sp_id)
    requests=HouseholdServiceRequest.query.filter_by(service_professional_id=sp_id,status='closed',closed_by='service_professional').all()
      # Prepare CSV data
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["service_id", "customer_id", "professional_id", "date_of_request", "description"])
    for request in requests:
        writer.writerow([request.service_id, request.customer_id, request.service_professional_id, request.date_created, request.description])
    output.seek(0)
    # Save CSV to a file (in a temporary directory)
    filename = f"service_request_export_{sp_id}.csv"
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, "w") as f:
        f.write(output.getvalue())

    # Send email with file link or attachment
    send_email_with_csv(
        sp.email,
        subject="Service request Export Completed",
        message=f"Your service request export is ready. You can download it from {file_path}.",
        csv_data=output.getvalue().encode("utf-8"),
        csv_filename=filename
    )

def send_email_with_csv(to, subject, message, csv_data, csv_filename):
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.mime.base import MIMEBase
    from email import encoders

    sender = "noreply@example.com"
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "text/plain"))

    attachment = MIMEBase("application", "octet-stream")
    attachment.set_payload(csv_data)
    encoders.encode_base64(attachment)
    attachment.add_header(
        "Content-Disposition", f"attachment; filename={csv_filename}"
    )
    msg.attach(attachment)

    # Send the email via MailHog
    with smtplib.SMTP("localhost", 1025) as server:
        server.send_message(msg)


#to test only
@celery.on_after_finalize.connect 
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(60, send_daily_reminder.s(), name='Daily_Reminder') 
    sender.add_periodic_task(60, send_monthly_activity_report.s(), name='Monthly_Report')


from celery.schedules import crontab


celery.conf.timezone = "Asia/Kolkata"
celery.conf.beat_schedule = {
    "daily-reminder-task": {
        "task": "tasks.send_daily_reminder",
        "schedule": crontab(hour='20', minute='0'),  # 8 PM IST
    },
    "monthly-report-task": {
        "task": "tasks.send_monthly_activity_report",
        "schedule": crontab(day_of_month='1', hour='0', minute='0'),  # 1st of every month
    },
}

