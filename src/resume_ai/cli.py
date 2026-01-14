import json
from pathlib import Path
import typer

from resume_ai.pipeline import ResumeProcessor
from resume_ai.providers.openai_provider import OpenAIProvider

app = typer.Typer(add_completion=False)


@app.command()
def build(
    input_path: Path = typer.Argument(..., help="Path to input file (txt or json)"),
    template: str = typer.Option("minimal", help="Template name"),
    pdf: Path = typer.Option(None, help="Optional PDF output path"),
    docx: Path = typer.Option(None, help="Optional DOCX output path"),
):
    raw_text = input_path.read_text(encoding="utf-8")
    provider = OpenAIProvider()
    processor = ResumeProcessor(provider, template_name=template)
    resume = processor.build(raw_text, output_pdf=str(pdf) if pdf else None, output_docx=str(docx) if docx else None)
    typer.echo(json.dumps(resume.model_dump(), indent=2))


def run():
    app()


if __name__ == "__main__":
    run()
