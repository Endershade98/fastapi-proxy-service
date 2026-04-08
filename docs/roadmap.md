## Epic 1: Core Proxy Engine (Domain & Application Layer)

Obiettivo: Costruire il motore core del proxy secondo principi DDD e Clean Architecture, separando logica di dominio, orchestrazione e interfacce concrete.

- Task 1.1: Implementare gestione cache (hit/miss, TTL, serializzazione sicura) nel layer Adapter
- Task 1.2: Gestire forward request con retry/backoff nel layer Application
- Task 1.3: Implementare parsing sicuro JSON/text con gestione fallback
- Task 1.4: Gestione eccezioni centralizzata (UpstreamTimeoutError, UpstreamServiceError) come entità di dominio
- Task 1.5: Introduzione delle entity e value objects per Request/Response, TTL e stato richiesta
- Task 1.6: Isolamento logica di dominio dal framework (FastAPI) per testabilità

## Epic 2: Rate Limiting e Security (Interface Layer)

Obiettivo: Gestire sicurezza e limitazioni request senza mescolare logica core.

- Task 2.1: Middleware per rate limiting per IP con Redis
- Task 2.2: Logging strutturato delle richieste superate (monitoring)
- Task 2.3: Implementazione opzionale API Key / JWT con gestione separata
- Task 2.4: Introduzione di Value Object per ClientIP e RequestQuota

## Epic 3: Asynchronous Processing & Celery Integration (Infrastructure & Application Layer)

Obiettivo: Scalare operazioni lente o retry senza bloccare il ciclo HTTP principale.

- Task 3.1: Creare worker Celery per gestione asincrona di caching e logging
- Task 3.2: Spostare salvataggio cache post-forwarding in Celery task async
- Task 3.3: Gestire retry HTTP asincrono con backoff tramite Celery
- Task 3.4: Notifiche/alerting async su errori critici
- Task 3.5: Tracciamento stato task Celery (Pending → Started → Success/Failure)

## Epic 4: Monitoring & Logging (Cross-Cutting)

Obiettivo: Avere osservabilità completa su cache, retry e performance.

- Task 4.1: Logging strutturato con livelli INFO/WARN/ERROR
- Task 4.2: Tracciamento cache HIT/MISS e performance dei task Celery
- Task 4.3: Integrazione con Prometheus/Grafana per metriche runtime
- Task 4.4: Alerting su errori critici o timeout
- Task 4.5: Log centralizzato delle transizioni di stato delle richieste

## Epic 5: Testing & CI/CD (Application & Infrastructure Layer)

Obiettivo: Garantire qualità del codice e sicurezza su ogni rilascio.

- Task 5.1: Unit test per ProxyService e CacheService (mocking fetch e Redis)
- Task 5.2: Integration test endpoint /proxy completo di retry e cache
- Task 5.3: End-to-end test flow completo: cache + retry + rate limiting + Celery
- Task 5.4: Lint, safety checks e pipeline CI/CD con test coverage reporting
- Task 5.5: Test di resilienza per Celery worker (task fail/retry)

## Epic 6: Performance & Scalability (Infrastructure Layer)

Obiettivo: Ottimizzare throughput, latenza e resilienza.

- Task 6.1: Gestione connessioni HTTP async ottimizzate con httpx
- Task 6.2: Configurazione Redis cluster per cache distribuita e resiliente
- Task 6.3: Analisi e ottimizzazione dei timeout e backoff strategy
- Task 6.4: Benchmarking e stress test della pipeline async Celery
- Task 6.5: Introduzione di circuit breaker o bulkhead pattern per resilienza upstream