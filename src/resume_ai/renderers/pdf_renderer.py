from pathlib import Path
from typing import Any

from resume_ai.models import Resume

try:
    from weasyprint import HTML  # type: ignore
except ImportError:
    HTML = None


class PDFRenderer:
    def __init__(self, jinja_env: Any):
        self.jinja_env = jinja_env

    def render(self, resume: Resume, *, template_name: str, output_path: str) -> None:
        if HTML is None:
            raise ImportError("weasyprint is required for PDF rendering; install with `pip install '.[pdf]'`")

        template = self.jinja_env.get_template(f"{template_name}.html")
        html_content = template.render(resume=resume)
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        HTML(string=html_content).write_pdf(target=str(output_file))
