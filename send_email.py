import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Gmail:

 def enviar_correo(destinatario, asunto, mensaje):
    # Datos de tu cuenta (Gmail ejemplo)
    remitente = "jhossanderhiciano@gmail.com"
    password = "jhux issv shcl ivcz"  # NO tu contraseña normal, usar contraseña de aplicación

    # Crear mensaje
    msg = MIMEMultipart()
    msg['From'] = remitente
    msg['To'] = destinatario
    msg['Subject'] = asunto
    msg.attach(MIMEText(mensaje, 'plain'))

    # Conexión al servidor Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, password)
    server.send_message(msg)
    server.quit()

