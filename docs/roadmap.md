# Project Roadmap – FastAPI Proxy (DDD + Clean Architecture)

---

## Epic 1: Core Proxy Engine (Domain & Application Layer) ✅ COMPLETATA

Obiettivo: Costruire il motore core del proxy secondo principi DDD e Clean Architecture, separando logica di dominio, orchestrazione e interfacce concrete.

- Task 1.1: Implementare gestione cache (hit/miss, TTL, serializzazione sicura) nel layer Adapter
- Task 1.2: Gestire forward request con retry/backoff nel layer Application
- Task 1.3: Implementare parsing sicuro JSON/text con gestione fallback
- Task 1.4: Gestione eccezioni centralizzata (UpstreamTimeoutError, UpstreamServiceError) come entità di dominio
- Task 1.5: Introduzione delle entity e value objects per Request/Response, TTL e stato richiesta
- Task 1.6: Isolamento logica di dominio dal framework (FastAPI) per testabilità

---

## Epic 2: Rate Limiting e Security (Interface + Domain Layer)

Obiettivo: Gestire sicurezza e limitazioni request separando enforcement, policy e observability.

- Task 2.1: Middleware per rate limiting per IP con Redis (enforcement veloce e stateless)
- Task 2.2: Logging strutturato delle richieste rilevanti su MongoDB (solo eventi: rate limit, errori, anomalie)
- Task 2.3: Implementazione opzionale API Key / JWT con persistenza su PostgreSQL
- Task 2.4: Introduzione di Value Object nel domain:
  - ClientIP (validazione e normalizzazione IP)
  - RequestQuota (limite + finestra temporale)
- Task 2.5: Introduzione Domain Service RateLimitPolicy per separare logica di decisione dal middleware

---

## Epic 3: Asynchronous Processing & Celery Integration (Infrastructure & Application Layer)

Obiettivo: Scalare operazioni lente o non critiche senza bloccare il ciclo HTTP principale.

- Task 3.1: Creare worker Celery per gestione asincrona
- Task 3.2: Spostare il salvataggio cache post-forwarding in task async
- Task 3.3: Gestire retry HTTP asincrono con backoff tramite Celery
- Task 3.4: Notifiche/alerting asincrone su errori critici
- Task 3.5: Tracciamento stato task Celery (Pending → Started → Success/Failure)
- Task 3.6: Logging asincrono su MongoDB tramite Celery (decoupling completo dal request cycle)

---

## Epic 4: Monitoring & Logging (Cross-Cutting)

Obiettivo: Avere osservabilità completa su comportamento del sistema.

- Task 4.1: Logging strutturato con livelli INFO/WARN/ERROR/DEBUG
- Task 4.2: Tracciamento cache HIT/MISS e performance richieste
- Task 4.3: Integrazione con Prometheus/Grafana per metriche runtime
- Task 4.4: Alerting su errori critici, timeout e spike di traffico
- Task 4.5: Centralizzazione log su MongoDB (collections: request_logs, rate_limits, errors)
- Task 4.6: Query analytics su MongoDB:
  - top IP
  - endpoint più utilizzati
  - percentuale cache hit/miss
  - frequenza rate limiting

---

## Epic 5: Testing & CI/CD (Application & Infrastructure Layer)

Obiettivo: Garantire qualità, stabilità e sicurezza del codice.

- Task 5.1: Unit test per ProxyService e CacheService (mocking HTTP e Redis)
- Task 5.2: Integration test endpoint /proxy con cache e retry
- Task 5.3: End-to-end test completo (cache + retry + rate limiting + Celery)
- Task 5.4: Pipeline CI/CD con lint, security checks e coverage
- Task 5.5: Test resilienza Celery worker (retry, failure handling)
- Task 5.6: Test logging MongoDB (mock repository, no DB reale)

---

## Epic 6: Performance & Scalability (Infrastructure Layer)

Obiettivo: Ottimizzare throughput, latenza e resilienza del sistema.

- Task 6.1: Ottimizzazione client HTTP async (httpx pooling, timeout)
- Task 6.2: Configurazione Redis cluster per cache distribuita
- Task 6.3: Ottimizzazione timeout e strategie di backoff
- Task 6.4: Benchmark e stress test pipeline async (Celery)
- Task 6.5: Introduzione circuit breaker / bulkhead pattern per resilienza upstream
- Task 6.6: Ottimizzazione scrittura MongoDB (batch insert, async logging)

---

## Architettura Tecnologica (Sintesi)

- FastAPI → API Layer
- Redis → Cache + Rate Limiting (volatile, high performance)
- PostgreSQL → Dati core (API keys, utenti, configurazioni)
- MongoDB → Logging, audit, analytics (non strutturato, append-only)

---

## Principio Architetturale Chiave

- Redis → decide **SE bloccare**
- Domain → decide **PERCHÉ**
- MongoDB → registra **COSA è successo**
- PostgreSQL → definisce **CHI e QUANTO può usare il sistema**