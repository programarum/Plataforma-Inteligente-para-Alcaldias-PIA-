# ADR-0008: Knowledge-Centered Architecture

- Status: Accepted
- Date: 2026-07-01

## Context

PIA necesita administrar archivos institucionales y preparar futuras capacidades
de búsqueda e IA sin convertir el repositorio documental en una fuente directa y
no gobernada para modelos probabilísticos.

## Decision

Se separan los módulos Documents y Knowledge. Documents representa metadata de
archivos y fragmentos textuales explícitos. Knowledge representa información
estructurada y relaciones con trazabilidad hacia documentos, normas, metas,
indicadores u otras fuentes.

Las futuras capacidades de IA y RAG consumirán Knowledge, no Documents
directamente. La transformación entre ambas fronteras será un proceso explícito
y gobernable que se diseñará en sprints posteriores.

## Consequences

- La gestión documental evoluciona sin depender de proveedores o técnicas de IA.
- El conocimiento puede normalizarse, relacionarse y gobernarse antes de indexar.
- Documentos y conocimiento conservan pertenencia institucional y trazabilidad.
- Los chunks no implican OCR, parsing, embeddings ni recuperación automática.
- Se requiere un proceso futuro para promover contenido documental a Knowledge.

