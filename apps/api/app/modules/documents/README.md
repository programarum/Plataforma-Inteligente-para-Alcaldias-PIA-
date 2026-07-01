# Documents module

Representa archivos institucionales mediante metadata; no almacena ni procesa
binarios. `Document` conserva identidad, ubicación lógica, clasificación y
pertenencia institucional. `DocumentChunk` permite registrar fragmentos
textuales ordenados manualmente como preparación para futuros procesos.

El módulo separa API, casos de uso, dominio y persistencia SQLAlchemy. En este
sprint no realiza carga de archivos, OCR, extracción de PDF ni embeddings.

