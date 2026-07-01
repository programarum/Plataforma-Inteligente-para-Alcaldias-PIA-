# Domain

Este directorio recoge el entendimiento inicial del dominio del problema y los conceptos clave del negocio.

## Propósito

Mantener un vocabulario común para el producto y facilitar futuras implementaciones.

## Kernel Core institucional

El núcleo inicial representa la estructura mínima de una alcaldía mediante tres
conceptos:

- **Municipality**: institución municipal principal. Conserva su identidad,
  ubicación, alcalde, periodo de gobierno, misión, visión y estado operativo.
- **Department**: dependencia organizacional perteneciente a una única
  alcaldía. Registra su propósito, responsable y estado operativo.
- **AuditLog**: registro inmutable de una acción sobre una entidad institucional.
  Su actor puede ser desconocido mientras no exista el módulo de usuarios.

Una alcaldía puede contener múltiples dependencias. Una dependencia no puede
crearse para una alcaldía inexistente. Municipality y Department se desactivan
de forma lógica mediante `is_active`; no se eliminan físicamente, preservando la
trazabilidad institucional.

Todos los identificadores son UUID y los timestamps representan instantes UTC.
La propiedad `department` de Municipality representa la división territorial
colombiana y no debe confundirse con las dependencias organizacionales del
módulo Department.

## Documents y Knowledge Core

`Document` representa la metadata de un archivo institucional y siempre se
asocia con una alcaldía y una dependencia. Su ciclo permite actualizar metadata
y archivar sin eliminar el registro. `DocumentChunk` es un fragmento textual
ordenado, proporcionado explícitamente; no implica extracción automática.

`KnowledgeItem` representa conocimiento estructurado procedente de un documento,
norma, meta, indicador o fuente futura. `KnowledgeRelation` establece una
relación dirigida entre dos items con tipo, descripción y confianza entre 0 y 1.

La frontera es deliberada: Documents custodia referencias a archivos; Knowledge
ofrece información estructurada para futuros consumidores. Las capacidades de IA
y RAG consumirán Knowledge y no accederán directamente a Documents.

## Identidad y RBAC

`User` representa un funcionario o administrador vinculado a una alcaldía y,
cuando corresponde, a una dependencia. `Role` agrupa responsabilidades dentro
de una alcaldía y `Permission` identifica una acción granular mediante un código
global único. `UserRole` y `RolePermission` forman las asignaciones RBAC.

Una persona solo puede recibir roles de su misma alcaldía. Las credenciales se
representan exclusivamente mediante un hash; autenticación, sesiones y
evaluación de permisos se incorporarán en el Sprint 6.
