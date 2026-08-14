from config import *
from dataclasses import dataclass, field
from datetime import datetime
import secrets
import uuid
import smtplib
from email.generator import BytesGenerator
from email.message import EmailMessage
from email.policy import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

@dataclass
class Victim:
    name: str
    surname: str
    city: str
    mail: str = field(init=False)

    def __post_init__(self):
        # surname = self.surname.lower().replace(" ", "") # option 1
        surname = self.surname.lower().split()[0] # option 2
        name = self.name.lower().split()[0]
        self.mail = f"{name}.{surname}@legalmail.it"
        self.city = self.city.lower()

def write_email(victim:Victim, eml_output: str = OUTPUT_FILE_EML) -> str:
    msg = EmailMessage(policy=SMTP)
    date_extended = datetime.now(TIMEZONE)
    date_small = date_extended.strftime("%d-%m-%Y")
    date_hour = date_extended.strftime("%X (%z)")
    msg_id = uuid.uuid4().hex
    smtp_id = secrets.token_hex(8).upper()

    email_body = f"""\
    Il giorno {date_small} alle ore {date_hour} il messaggio"NOTIFICA ELEZIONE DOMICILIO DIGITALE TI8 Q01358/2026 ENTRATE|AGEDP-UD|REGISTRO UFFICIALE|236913|" è stato inviato da "dp.{victim.city}@pce.agenziaentrate.it" indirizzato a:
    {victim.mail}
    Il messaggio originale è incluso in allegato.

    Identificativo messaggio: {msg_id}.posta-certificata@legalmail.it


    """

    email_subject = (
            "NOTIFICA ELEZIONE DOMICILIO DIGITALE "
            "TI8 Q01358/2026 "
            f"[ENTRATE|AGEDP|REGISTRO UFFICIALE|236913|{date_small}]"
            "[358965823|349749437]"
        )

    msg["Received"] = (
        "from SpeedBack03 (217.175.54.43) "
        "by sendm.cert.legalmail.it (5.8.812.01) "
        f"(authenticated as dp.{victim.city}@pce.agenziaentrate.it) "
        f"id {smtp_id} "
        f"for {victim.mail}; "
        f"{date_extended.strftime('%A, %d %b %Y %X %z')}"
    )

    msg["Date"] = (
        date_extended.strftime("%A, %d %b %Y %X %z (%Z)")
    )
    msg["From"] = (
        f"dp.{victim.city}@pce.agenziaentrate.it"
    )
    msg["To"] = (
        victim.mail
    )
    msg["Message-ID"] = (
        f"<{msg_id}.posta-certificata@legalmail.it>"
    )

    msg["Subject"] = email_subject

    msg["MIME-Version"] = (
        "1.0"
    )

    # Custom header
    msg["X-Riferimento-Message-ID"] = (
        "<201232344.1979638.1695024791178@SpeedBack03>"
    )

    # Multipart message
    msg.set_content(
        HTML_BODY,
        subtype="html",
        charset="utf-8",
    )

    # Save as .eml
    with open(eml_output, "wb") as f:
        BytesGenerator(f, policy=SMTP).flatten(msg)
    print(f"EML file written to {eml_output}") 

    return email_subject, email_body

def send_email(victim: Victim, output: str = OUTPUT_PHISHING_EMAIL, fake_xml: str = INPUT_FAKE_XML, save_to_txt: bool = False) -> None:

    date = datetime.now(TIMEZONE).strftime("%d-%m-%Y")

    # Create the email
    subject, body = write_email(victim, OUTPUT_FILE_EML)
   
    if(save_to_txt):
        with open(OUTPUT_FILE_BODY, "w") as f2:
            f2.write(f"SUBJECT:\n{subject}\n")
            f2.write("\n")
            f2.write(f"BODY:\n{body}")
        print(f"Email contents written to {OUTPUT_FILE_BODY}") 
    else: 
        msg = MIMEMultipart()
        msg["From"] = f"dp.{victim.city}@pce.agenziaentrate.it"
        msg["To"] = f"{victim.mail}"
        msg["Subject"] = subject   
        msg.attach(MIMEText(body, "plain"))

        # Attach the .eml file
        with open(OUTPUT_FILE_EML, "rb") as attachment:
            eml_part = MIMEBase("application", "octet-stream")
            eml_part.set_payload(attachment.read())

        encoders.encode_base64(eml_part)

        eml_part.add_header(
            "Content-Disposition",
            f'attachment; filename="{OUTPUT_FILE_EML[len(OUPUT_PATH):]}"'
        )
        msg.attach(eml_part)

        # Attach the fake certificate
        try: 
            with open(fake_xml, "rb") as attachment:
                    xml_part = MIMEBase("application", "octet-stream")
                    xml_part.set_payload(attachment.read())

            encoders.encode_base64(xml_part)

            xml_part.add_header(
                "Content-Disposition",
                f'attachment; filename="{fake_xml[len(OUPUT_PATH):]}"'
            )
            msg.attach(xml_part)
        except OSError as e:
            print(f"No .xml file found, please provide a '{OUTPUT_FAKE_XML}' file")
            print("to specify name of xml file, usage: sendMail(victim, output, fake_xml)")
            exit
        else: 
            # Save email
            with open(output, "w", encoding="utf-8", newline="\n") as f:
                f.write(msg.as_string())
