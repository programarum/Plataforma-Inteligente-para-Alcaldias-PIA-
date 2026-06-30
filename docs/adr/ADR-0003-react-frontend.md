# ADR-0003: Usar React para el frontend web

- Estado: Accepted
- Fecha: 2026-06-30

## Contexto

PIA requiere interfaces web para flujos institucionales, consulta de informacion y administracion. La interfaz debe permitir composicion de componentes, tipado y crecimiento incremental.

## Decision

Usar React con TypeScript para las aplicaciones web de PIA. Las aplicaciones consumiran contratos publicados por la API y compartiran solo los elementos que tengan una responsabilidad transversal comprobada.

Este ADR no selecciona librerias adicionales ni implementa una aplicacion durante el Sprint 1.

## Consecuencias

- Ecosistema amplio para interfaces empresariales.
- Componentes reutilizables y comprobables de forma aislada.
- Necesidad de gobernar dependencias, estado y accesibilidad.
- Separacion explicita entre contratos de API y presentacion.

## Alternativas consideradas

- Vue y Angular: opciones viables, no seleccionadas para mantener la tecnologia aprobada para el producto.
- Renderizado exclusivo del servidor: insuficiente para las interacciones previstas.
