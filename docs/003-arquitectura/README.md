# Arquitectura de PIA

PIA se desarrollara como un monolito modular: una unidad de despliegue principal con modulos internos cohesionados y limites claros. Este enfoque reduce complejidad operativa inicial y permite evolucionar el producto de forma controlada.

## Principios arquitectonicos

- Dependencias explicitas entre modulos.
- Separacion entre dominio, aplicacion e infraestructura.
- Contratos estables para interfaces internas y externas.
- Seguridad, observabilidad y auditoria como capacidades transversales.
- Persistencia relacional central con propiedad logica de datos por modulo.
- Acceso a proveedores de IA mediante una frontera controlada.

## Componentes previstos

- `apps/api`: API backend con FastAPI.
- `apps/web`: experiencia web con React.
- `apps/desktop`: experiencia de escritorio.
- `apps/admin`: experiencia administrativa.
- `packages`: modulos y capacidades compartidas.
- `infrastructure`: recursos de despliegue y operacion.

La implementacion de estos componentes corresponde a sprints posteriores.

## Decisiones

Las decisiones vigentes y su motivacion se encuentran en el [indice de ADR](../adr/README.md).
