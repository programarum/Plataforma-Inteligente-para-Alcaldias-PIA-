# ADR-0002: Usar FastAPI para el backend

- Estado: Accepted
- Fecha: 2026-06-30

## Contexto

PIA necesita exponer contratos HTTP, validar datos y documentar integraciones. El ecosistema Python tambien facilita la integracion posterior con capacidades de datos e inteligencia artificial.

## Decision

Usar FastAPI como framework de la API backend dentro del monolito modular. Los contratos publicos se documentaran con OpenAPI y la implementacion respetara los limites definidos por los modulos de dominio y aplicacion.

Este ADR selecciona la tecnologia; no define endpoints ni autoriza logica de negocio en el Sprint 1.

## Consecuencias

- Validacion tipada y documentacion de API integradas.
- Alineacion con el ecosistema Python previsto para PIA.
- Necesidad de convenciones claras para evitar que el framework invada el dominio.
- Dependencia del ciclo de vida y compatibilidad del ecosistema FastAPI.

## Alternativas consideradas

- Django: no seleccionado por incluir un marco mas amplio que el requerido para la API prevista.
- Flask: no seleccionado porque requeriria definir o integrar mas piezas para validacion y contratos.
