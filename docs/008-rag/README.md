# Retrieval-Augmented Generation

La futura recuperación aumentada se apoyará en elementos aprobados del Knowledge
Core. `DocumentChunk` prepara una unidad textual trazable, pero en este sprint no
se genera automáticamente, no tiene embeddings y no participa en recuperación.

Un flujo futuro podrá transformar documentos y chunks en Knowledge Items,
indexarlos y recuperar conocimiento con referencias a sus fuentes. RAG no debe
saltar esa frontera ni consultar archivos institucionales directamente.

