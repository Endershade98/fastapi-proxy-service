# Proxy Server - Stati delle richieste

Questo documento elenca i principali stati delle richieste gestite dal ProxyServer FastAPI, con codici, descrizione e note operative.

## Tabella 1: Stati principali delle richieste

| Codice Stato | Nome Stato       | Descrizione                                                                 | Azione successiva / Note                        |
|--------------|-----------------|-----------------------------------------------------------------------------|------------------------------------------------|
| 100          | PENDING         | Richiesta ricevuta dall'endpoint ma non ancora elaborata                    | Controllo cache → Cache HIT o Cache MISS      |
| 110          | CACHE_HIT       | Risposta trovata in cache                                                   | Restituisce subito al client                  |
| 120          | CACHE_MISS      | Nessuna risposta trovata in cache                                           | Forwarding al server esterno                  |
| 200          | FORWARDING      | Richiesta inoltrata al server esterno                                       | Monitoraggio stato → Completed / Retrying / Failed |
| 210          | RETRYING        | Tentativo di re-invio dopo fallimento con backoff                           | Retry limit controllato → Retry o Failed      |
| 300          | COMPLETED       | Risposta ricevuta correttamente dal server esterno e cache aggiornata       | Return response al client                      |
| 400          | FAILED          | Errore critico o timeout dopo max retries                                    | Log errore, return error al client            |

---

## Tabella 2: Stati della connessione / client IP

| Codice Stato | Nome Stato     | Descrizione                                         | Note                                           |
|--------------|---------------|---------------------------------------------------|-----------------------------------------------|
| 500          | ACTIVE        | Connessione attiva con client/server             | Durante il forwarding o elaborazione richiesta |
| 510          | RATE_LIMITED  | Superato limite richieste per IP                 | Ritorna 429 al client                          |
| 520          | IDLE          | Connessione aperta ma inattiva                   | Attesa di nuova richiesta                      |
| 530          | CLOSED        | Connessione terminata                            | Pulizia risorse                                |
| 540          | ERROR         | Errore nella connessione                         | Log dell’errore                                |

---

## Tabella 3: Stati della connessione / client IP

| Codice | Stato         | Descrizione                                         |
|--------|---------------|---------------------------------------------------|
| 500    | ACTIVE        | Connessione attiva con client/server             |
| 510    | RATE_LIMITED  | Superato limite richieste per IP                 |
| 520    | IDLE          | Connessione aperta ma inattiva                   |
| 530    | CLOSED        | Connessione terminata                            |
| 540    | ERROR         | Errore nella connessione                         |

---

## Note operative

- I codici sono arbitrari e possono essere modificati per allinearsi con la tua implementazione.
- Gli stati **RETRYING** e **FAILED** richiedono logging dettagliato per monitorare eventuali problemi upstream.
- È consigliabile tracciare ogni transizione di stato nel log o in un sistema di monitoring (es. Prometheus/Grafana) per performance e debugging.
- La tabella degli stati può essere integrata con **metriche di cache HIT/MISS** e **tempo di risposta per ogni stato**.