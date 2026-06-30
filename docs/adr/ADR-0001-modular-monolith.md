# ADR-0001: Adoptar un monolito modular

- Estado: Accepted
- Fecha: 2026-06-30

## Contexto

PIA debe integrar varias capacidades institucionales y crecer de manera incremental. Un sistema distribuido desde el inicio agregaria costos de despliegue, observabilidad, consistencia y operacion que no se justifican en la etapa actual.

## Decision

Construir PIA como un monolito modular. La solucion tendra una unidad de despliegue backend principal y modulos internos con responsabilidades, contratos y propiedad logica claramente definidos. La comunicacion entre modulos debe ocurrir mediante interfaces explicitas.

No se adoptan microservicios. Una separacion futura requerira evidencia operativa, limites estables y un nuevo ADR.

## Consecuencias

- El despliegue y la operacion iniciales son mas simples.
- Las transacciones y la consistencia pueden gestionarse dentro de una sola aplicacion.
- La disciplina sobre limites modulares es esencial para evitar acoplamiento indebido.
- Los modulos podran evolucionar sin asumir desde ahora el costo de una red distribuida.

## Alternativas consideradas

- Microservicios: rechazados por su complejidad prematura.
- Monolito sin modulos: rechazado porque dificulta mantener limites y evolucionar el producto.
