import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from typing import Optional

# Charger les variables d'environnement
load_dotenv(override=True)

class EmailError(Exception):
    """Exception levée en cas d'erreur lors de l'envoi d'email"""
    pass

def send_email(
    subject: str,
    sender: str,
    recipient: str,
    html_content: str
) -> bool:
    """
    Envoie un email HTML via SMTP.
    
    :param subject: Objet de l'email
    :param sender: Adresse email de l'expéditeur
    :param recipient: Adresse email du destinataire
    :param html_content: Contenu HTML du message
    :return: True si l'email a été envoyé
    :raises EmailError: Si une erreur survient
    """
    try:
        # Récupération des paramètres SMTP depuis .env
        smtp_server = os.getenv("MAIL_HOST")
        smtp_port = int(os.getenv("MAIL_PORT", "587"))  # Port par défaut : 587
        smtp_user = os.getenv("MAIL_USERNAME")
        smtp_password = os.getenv("MAIL_PASSWORD")

        if not all([smtp_server, smtp_user, smtp_password]):
            raise EmailError("Paramètres SMTP incomplets dans le fichier .env")

        # Création du message
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient

        html_part = MIMEText(html_content, "html")
        msg.attach(html_part)

        # Connexion au serveur SMTP
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Sécurisation de la connexion
            server.login(smtp_user, smtp_password)
            server.sendmail(sender, recipient, msg.as_string())

        return True

    except smtplib.SMTPException as e:
        raise EmailError(f"Erreur SMTP lors de l'envoi de l'email : {str(e)}") from e

    except Exception as e:
        raise EmailError(f"Erreur inattendue lors de l'envoi de l'email : {str(e)}") from e