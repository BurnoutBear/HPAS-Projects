from dataclasses import dataclass, field
from datetime import datetime
import secrets
import uuid
from email.generator import BytesGenerator
from email.message import EmailMessage
from email.policy import SMTP
import pytz

TIMEZONE = "Europe/Rome"
TZ = pytz.timezone(TIMEZONE)
HTML_BODY = """\
<html>
<body>
<p>Gentile Contribuente,</p>

<p>
Le ricordiamo dell’abilitazione del domicilio digitale, entrato in vigore con il provvedimento del 7 ottobre 2024 
(<a href="https://www.agenziaentrate.gov.it/portale/documents/20143/6458356/ProvvComunicazioneDomiciliodigitaleSpeciale+del+7+ottobre+2024.pdf/f1ad2896-77fc-4a22-0e61-6acadce56a5d?t=1728376480652">provvedimento-pdf</a>),
che permette di comunicare un indirizzo PEC presso il quale eleggere il proprio domicilio digitale speciale al fine di ricevere atti e comunicazioni dell’Agenzia delle entrate e dell’Agenzia delle entrate-Riscossione.
</p>

<p>
Ai sensi dell'art. 3-bis, comma 1-bis, del d.lgs 7 marzo 2005, n. 82
(Codice dell'Amministrazione Digitale - CAD), qualunque persona fisica ha facoltà di eleggere e modificare il proprio domicilio digitale, da iscrivere nell'Indice nazionale dei domicili digitali (INAD).
</p>

<p>
Per professionisti iscritti in albi o elenchi (come definiti ai sensi degli art. 6-bis e 6-quinques del d.lgs n.82/2005 CAD) l'elezione del domicilio digitale è un obbligo e La esortiamo ad eleggere al piú presto il proprio domicilio digitale.
</p>

<p>
Le ricordiamo che la comunicazione per il domicilio digitale speciale può avvenire esclusivamente online, utilizzando lo specifico servizio web disponibile in area riservata.
</p>

<p>
La presente comunicazione ha finalità esclusivamente informative e non costituisce un avviso di accertamento né una richiesta di pagamento.
</p>

<p>
Ulteriori indicazioni sono disponibili sul sito dell’Agenzia delle Entrate al seguente avviso:
<a href="https://www.agenziaentrate.gov.it/portale/comunicazione-del-domicilio-digitale-speciale/che-cos-cittadini">
Comunicazione del domicilio digitale speciale
</a>
</p>

<p>
Cordiali saluti,<br>
Il Direttore della Direzione Centrale Servizi ai Contribuenti
</p>

</body>
</html>
"""
OUTPUT_FILE = "postacert.eml"

@dataclass
class Victim:
    name: str
    surname: str
    city: str
    mail: str = field(init=False)

    def __post_init__(self):
        self.mail = f"{self.name}.{self.surname}@gmail.it"

def write_email(victim: Victim) -> None:
    msg = EmailMessage(policy=SMTP)
    date_extended = datetime.now(TZ)
    date_small = date_extended.strftime("%d-%m-%Y")
    smtp_id = secrets.token_hex(8).upper()

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
        f"<{uuid.uuid4().hex}@legalmail.it>"
    )

    msg["Subject"] = (
        "NOTIFICA NOTIFICA ELEZIONE DOMICILIO DIGITALE "
        "TI8 Q01358/2026 "
        f"[ENTRATE|AGEDP|REGISTRO UFFICIALE|236913|{date_small}]"
        "[358965823|349749437]"
    )
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
    with open(OUTPUT_FILE, "wb") as f:
        BytesGenerator(f, policy=SMTP).flatten(msg)

    print(f"EML file written to {OUTPUT_FILE}")

if __name__ == "__main__":
    victim = Victim("Marco", "Rossi", "Roma")
    write_email(victim)
