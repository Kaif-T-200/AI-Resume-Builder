# Resume AI (local-first)

Local-first AI-powered resume builder pipeline using Python and OpenAI. Focus is on input normalization, AI rewriting without fabrication, and rendering to PDF/DOCX.

## Quick start
1. Create and activate a virtualenv.
2. Install: `pip install -e .` (add `.[pdf]` for PDF support).
3. Set `OPENAI_API_KEY` (and optionally `OPENAI_MODEL`).
4. Run CLI: `python -m resume_ai.cli samples/sample_plain.txt --pdf out/resume.pdf`.

## Structure
- `src/resume_ai/models.py` — Pydantic resume schema.
- `src/resume_ai/pipeline.py` — extraction + rewrite + render pipeline.
- `src/resume_ai/providers/` — LLM provider abstraction and OpenAI impl.
- `src/resume_ai/templating/templates/` — Jinja2 templates (minimal, corporate).
- `src/resume_ai/renderers/` — PDF (WeasyPrint) and DOCX (python-docx) renderers.
- `samples/` — example inputs.

## Notes
- The prompts enforce “no fabrication”; missing data stays empty.
- PDF rendering requires system deps for WeasyPrint (Cairo, Pango). Use DOCX as a lighter fallback.
