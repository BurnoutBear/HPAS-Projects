# Agenzia delle Entrate

Questa applicazione replica il flusso di autenticazione della piattaforma di login dell'Agenzia delle Entrate (ADE).

## Funzionalità implementate

Attualmente è supportato il flusso di autenticazione tramite **CIE (Carta d'Identità Elettronica)**.

Il flusso completo di autenticazione viene gestito tramite l'oggetto `LoginFlow`, che mantiene tutte le informazioni necessarie durante il processo di login, tra cui:

- sessione utente;
- credenziali di accesso;
- QR Code generato;
- tempo di validità (TTL);
- altre informazioni necessarie alla gestione del flusso di autenticazione.

## Installazione

Prima di avviare l'applicazione è necessario creare l'ambiente virtuale Python (`.venv`) nella directory principale del progetto.

```bash
python -m venv .venv
```

Dopo aver attivato l'ambiente virtuale, installare le dipendenze del progetto tramite il file `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Flusso di autenticazione

### Accesso iniziale

Il primo step consiste nell'accesso alla pagina di login ADE tramite una sessione valida.  
Dopo la selezione del metodo di autenticazione CIE, la stessa sessione viene mantenuta durante il redirect verso la pagina di autenticazione.

### Login tramite credenziali

Il login tramite username e password segue questo flusso:  
1. Invio delle credenziali tramite richiesta HTTP POST.
2. Avvio di un processo di polling per verificare lo stato dell'autenticazione.
3. Attesa del completamento della verifica a due fattori (2FA).
4. Prosecuzione dell'accesso una volta completata correttamente la verifica.

### Login tramite QR Code

Il login tramite QR Code segue invece questo processo:  
1. Generazione del QR Code associato alla sessione.
2. Avvio del polling per verificare l'avvenuta scansione del QR Code.
3. Attesa della conferma dell'autenticazione.
4. Completamento del flusso di login dopo la validazione.
