# Dominio de PIA

El dominio representa las capacidades institucionales que PIA apoya. El Kernel Core introduce las primeras entidades base de una alcaldia sin incorporar identidad, autenticacion ni procesos administrativos.

## Areas iniciales

- Identidad, acceso y seguridad.
- Gestion y recuperacion de conocimiento institucional.
- Busqueda y consulta documental.
- Asistencia mediante inteligencia artificial.
- Auditoria y trazabilidad.
- Integraciones y canales de experiencia.

## Kernel Core

### Municipality

Representa una alcaldia dentro de PIA. Conserva su nombre, ubicacion territorial, alcalde, periodo de gobierno, mision, vision, estado y marcas temporales. El campo `department` identifica la division territorial colombiana o su equivalente en el pais correspondiente.

### Department

Representa una dependencia organizacional que pertenece a una `Municipality`, por ejemplo una secretaria o direccion. Conserva nombre, descripcion, responsable, estado y marcas temporales. No debe confundirse con el campo territorial `Municipality.department`.

### AuditLog

Representa un registro inmutable de una accion institucional. Conserva actor, accion, tipo e identificador de la entidad, metadata y fecha. En esta etapa solo existen su modelo y repositorio; la captura automatica de eventos se definira posteriormente.

## Reglas iniciales

- Los identificadores son UUID.
- Las marcas temporales se generan en UTC.
- Una dependencia organizacional debe pertenecer a una alcaldia existente.
- La desactivacion conserva los registros y cambia `is_active` a `false`.
- No se implementa eliminacion fisica para las entidades del Kernel Core.

## Modelado

Cada nueva capacidad debe modelarse con especialistas del dominio. El lenguaje ubicuo, los limites modulares y las invariantes se documentan antes de codificarse. Las dependencias entre modulos deben ser explicitas y respetar la arquitectura aprobada.

## Estado

El Kernel Core inicial esta implementado. Las demas areas continúan sujetas a descubrimiento y definicion funcional.
