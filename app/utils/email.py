import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.core.settings import settings


def send_email(to_address: str, subject: str, body: str):
    """
    Envía un correo usando la configuración de variables de entorno.
    """
    # Crear el mensaje
    msg = MIMEMultipart()
    msg['From'] = settings.email_user
    msg['To'] = to_address
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Conexión al servidor SMTP
    try:
        server = smtplib.SMTP(settings.email_host, settings.email_port)
        server.starttls()
        server.login(settings.email_user, settings.email_pass)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error enviando correo: {e}")
        return False