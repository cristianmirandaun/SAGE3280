# SAGE3280 - Base (Fase 1) — Esqueleto

Resumen
-------
Base mínima para SAGE3280: modelo de datos en PostgreSQL, API REST (FastAPI) con endpoints para:
- Gestión de pacientes
- Gestión de convocatorias/contactos automáticos (registro y estado)
- Registro de intentos de contacto (logs)
- Gestión básica de citas/agenda (registro y estado)

Objetivo
--------
Proveer la infraestructura y el contrato API necesarios para:
- Ejecutar procesos por lotes que identifiquen pacientes con controles pendientes.
- Registrar contactos planeados y resultados (confirmado, reprogramado, rechazado).
- Mantener trazabilidad y métricas de adherencia.

Levantar localmente (ejemplo)
-----------------------------
1. Copiar .env.example -> .env y ajustar VARIABLES (POSTGRES_PASSWORD, etc.)
2. docker-compose up --build
3. La API estará en http://localhost:8000
4. Docs OpenAPI: http://localhost:8000/docs
