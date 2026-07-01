# Knowledge module

Representa conocimiento estructurado que puede originarse en documentos,
normas, metas, indicadores o futuras fuentes. `KnowledgeItem` es la unidad que
consumirán posteriormente búsqueda y RAG; `KnowledgeRelation` conecta elementos
mediante relaciones dirigidas y una confianza explícita.

El módulo no ejecuta IA, embeddings, recuperación semántica ni llamadas a
modelos. Cuando el origen es un documento, el caso de uso valida que exista sin
leer ni procesar su archivo.

