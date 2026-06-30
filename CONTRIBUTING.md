# Guia de contribucion

Gracias por contribuir a PIA. Todo cambio debe respetar la arquitectura vigente, incluir documentacion cuando corresponda y mantener el repositorio verificable.

## Flujo de trabajo

1. Crea una rama corta desde la rama principal actualizada.
2. Realiza cambios pequenos y enfocados.
3. Agrega o actualiza pruebas y documentacion.
4. Ejecuta las validaciones disponibles.
5. Abre un pull request usando la plantilla del repositorio.

## Conventional Commits

Los commits siguen el formato:

```text
<type>(<scope>): <description>
```

Tipos habituales: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci` y `build`.

Ejemplos:

```text
chore(project): initialize repository foundation
docs(architecture): clarify module boundaries
test(api): cover health endpoint
```

La descripcion debe usar modo imperativo, ser concisa y representar un unico cambio logico.

## Criterios para pull requests

- Explicar el problema y la solucion.
- Relacionar el issue correspondiente cuando exista.
- Incluir pruebas proporcionales al cambio.
- No introducir dependencias sin justificacion y aprobacion.
- Registrar las decisiones arquitectonicas significativas mediante ADR.
- Mantener compatibilidad con las tecnologias, patrones y estructura aprobados.

## Revision

Al menos una persona mantenedora debe revisar los cambios antes de integrarlos. Los comentarios se resuelven mediante acuerdos tecnicos documentados y un trato respetuoso.
