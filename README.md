# PIA - Plataforma Inteligente para Alcaldias

PIA es una plataforma empresarial para apoyar la transformacion digital de las alcaldias. Su proposito es organizar el conocimiento institucional, facilitar procesos administrativos y ofrecer bases confiables para la atencion ciudadana y la toma de decisiones.

El producto se concibe como una solucion modular, auditable y preparada para crecer sin fragmentar prematuramente su operacion. En esta etapa el repositorio contiene exclusivamente su fundacion documental y estructural.

## Objetivos

- Centralizar y preservar el conocimiento institucional.
- Mejorar la trazabilidad de procesos y decisiones.
- Facilitar la integracion responsable de capacidades de inteligencia artificial.
- Proteger la informacion institucional y los datos de la ciudadania.
- Proveer experiencias web, de escritorio y administrativas coherentes.

## Arquitectura

PIA adopta un monolito modular. Los limites de dominio y las responsabilidades se documentan antes de implementar funcionalidades. Las decisiones principales se registran en [Architecture Decision Records](docs/adr/README.md).

Componentes previstos:

- API: FastAPI.
- Aplicaciones web: React.
- Aplicacion de escritorio: Tauri.
- Persistencia: PostgreSQL.
- Capacidades de IA: acceso mediante un AI Gateway.

Estas tecnologias estan documentadas como decisiones arquitectonicas; aun no se implementan en la estructura nueva de `apps/`.

## Estructura del repositorio

```text
apps/             Aplicaciones desplegables
packages/         Modulos compartidos de PIA
infrastructure/   Configuracion de infraestructura
docs/             Documentacion del producto y ADR
tests/            Pruebas transversales
tools/            Herramientas internas del repositorio
```

## Estado

Version inicial: `0.1.0`. Sprint 1: fundacion del repositorio.

Consulta [ROADMAP.md](ROADMAP.md), [CONTRIBUTING.md](CONTRIBUTING.md) y la [documentacion](docs/README.md) para conocer los siguientes pasos.

## Licencia

Distribuido bajo Apache License 2.0. Consulta [LICENSE](LICENSE).
