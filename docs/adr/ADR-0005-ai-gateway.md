# ADR-0005: Centralizar el acceso a IA mediante un AI Gateway

- Estado: Accepted
- Fecha: 2026-06-30

## Contexto

PIA podra utilizar distintos modelos y proveedores de inteligencia artificial. El acceso directo desde multiples modulos dificultaria aplicar seguridad, auditoria, limites de consumo, proteccion de datos y cambios de proveedor.

## Decision

Centralizar las solicitudes a modelos de IA mediante un AI Gateway interno. Esta frontera abstraera proveedores y aplicara politicas comunes de autorizacion, trazabilidad, tratamiento de datos, resiliencia y control de costos.

El gateway formara parte del monolito modular en su etapa inicial. Este ADR no implementa proveedores, prompts ni funcionalidades de IA.

## Consecuencias

- Politicas de IA consistentes y auditables.
- Menor acoplamiento de los modulos con proveedores concretos.
- Punto central para observabilidad y control de consumo.
- El gateway debe evitar convertirse en una abstraccion que oculte capacidades necesarias de cada proveedor.

## Alternativas consideradas

- Integracion directa por modulo: rechazada por duplicacion y falta de gobierno central.
- Servicio independiente desde el inicio: rechazado por contradecir la decision de monolito modular sin necesidad operativa demostrada.
