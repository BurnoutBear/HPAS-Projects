# Phishing Email

Questa app permette di generare mail di phishing personalizzate con i dati delle vittime, salvando la mail come file eml.


## Installazione

Prima di avviare l'applicazione è necessario creare l'ambiente virtuale Python (`.venv`) nella directory principale del progetto.

```bash
python -m venv .venv
```

Dopo aver attivato l'ambiente virtuale, installare le dipendenze del progetto tramite il file `requirements.txt`:

```bash
pip install -r requirements.txt
```

## Utilizzo

Modificare il file config.py per personalizzare la mail generata con le informazioni sulla vittima. 
Sono necessari: nome, cognome, cittá di residenza

Assegnare alla variabile SCAM_LINK nel file di config una stringa con il link al sito di login fittizzio.

Assicurarsi di avere un file nominato daticert.xml e modificare la variabile INPUT_FAKE_XML con i path corretto nel file di config.
I contenuti del file non sono importanti ma utilizzare una firma autentica delle poste italiane per un altra email é raccomandato. 

Specificare il path all'interno della cartella dove verrano salvati i file in output nella variabile OUTPUT_PATH

infine basta semplicemente eseguire il file run.py
''''bash
python3 run.py
''''

I file di output generati sono i seguenti.

### emailbody.txt

In caso serva comporre manualmente l'email.

Se SAVE_TO_TXT é imposto a True nel file di config il soggetto e il corpo della mail verrano salvati in questo file invece di generare un file eml.

Il file postacert.eml verrá comunque generato e va inserito come allegato.

### postacert.eml

Il file .eml che verrá allegato alla mail di phishing vera e propria.
Contiene il link indicato dalla variabile SCAM_LINK nel file di config.

### phishingMail.eml

Un mock-up della mail da inviare alla vittima, salvato come file .eml invece di essere inviata.

Verrá generato solo in caso SAVE_TO_TXT sia False 