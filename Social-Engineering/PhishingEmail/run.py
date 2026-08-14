from config import *
import automail

if __name__ == "__main__":
    victim = automail.Victim(VICTIM_NAME, VICTIM_SURNAME, VICTIM_RESIDENCE)
    automail.send_email(victim, output=OUTPUT_PHISHING_EMAIL, fake_xml=INPUT_FAKE_XML, save_to_txt=SAVE_TO_TXT)