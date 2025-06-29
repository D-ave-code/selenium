import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os
import datetime
def enviar_correo(asunto, mensaje, destinatario, ruta_imagen=None):
    remitente = "espinozadavid34@yahoo.es"
    password = "yircgspbidyeospb"

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain"))

    # Adjuntar archivos si se proporciona ruta(s)
    if ruta_imagen:
        # Si es una lista de archivos
        if isinstance(ruta_imagen, list):
            for archivo_path in ruta_imagen:
                if os.path.exists(archivo_path):
                    with open(archivo_path, "rb") as archivo:
                        parte = MIMEBase("application", "octet-stream")
                        parte.set_payload(archivo.read())
                        encoders.encode_base64(parte)
                        parte.add_header(
                            "Content-Disposition",
                            f"attachment; filename={os.path.basename(archivo_path)}"
                        )
                        msg.attach(parte)
                else:
                    print(f"[WARNING] Archivo no encontrado: {archivo_path}")
        # Si es un solo archivo
        else:
            if os.path.exists(ruta_imagen):
                with open(ruta_imagen, "rb") as archivo:
                    parte = MIMEBase("application", "octet-stream")
                    parte.set_payload(archivo.read())
                    encoders.encode_base64(parte)
                    parte.add_header(
                        "Content-Disposition",
                        f"attachment; filename={os.path.basename(ruta_imagen)}"
                    )
                    msg.attach(parte)
            else:
                print(f"[WARNING] Archivo no encontrado: {ruta_imagen}")

    try:
        servidor = smtplib.SMTP("smtp.mail.yahoo.com", 587)
        servidor.starttls()
        servidor.login(remitente, password)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
        print("[OK] Correo enviado correctamente con archivos adjuntos.")
    except Exception as e:
        print(f"[ERROR] Error al enviar el correo: {e}")
