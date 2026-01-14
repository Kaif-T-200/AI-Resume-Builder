import json
import re
from typing import Any, Optional

from resume_ai.models import Resume
from resume_ai.prompt_library import extraction_prompt, rewrite_prompt
from resume_ai.providers.base import LLMProvider
from resume_ai.renderers.pdf_renderer import PDFRenderer
from resume_ai.renderers.docx_renderer import DocxRenderer
from resume_ai.templating.templates import get_template_env


class ResumeProcessor:
    def __init__(self, llm: LLMProvider, template_name: str = "minimal"):
        self.llm = llm
        self.template_name = template_name
        self.env = get_template_env()

    def parse_input(self, raw_input: str) -> str:
        return raw_input.strip()

    def _normalize_resume_input(self, data: dict) -> dict:
        """Normalize user JSON to internal schema and add sensible defaults."""
        defaults = {
            "contact": {"full_name": None, "email": None, "phone": None, "location": None, "links": []},
            "summary": None,
            "experience": [],
            "projects": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "achievements": [],
            "extracurricular": [],
            "languages": [],
            "interests": [],
        }

        def sentence_bullets(text: str) -> list[str]:
            # Split by sentence-ish boundaries and remove empties
            parts = re.split(r"(?<=[.!?])\s+", text.strip())
            return [p.strip() for p in parts if p.strip()]

        normalized = defaults.copy()

        # Contact
        contact = data.get("contact", {}) if isinstance(data, dict) else {}
        contact_links = contact.get("links", []) or []
        
        # Handle links as dict (convert to list of values) or list
        if isinstance(contact_links, dict):
            contact_links = list(contact_links.values())
        elif not isinstance(contact_links, list):
            contact_links = []

        normalized_links = []
        for link in contact_links:
            if isinstance(link, dict):
                val = link.get("value") or link.get("url") or link.get("link") or link.get("href")
                if val:
                    normalized_links.append(str(val))
            elif isinstance(link, str):
                if link.strip():
                    normalized_links.append(link.strip())
            else:
                # fallback to string cast
                normalized_links.append(str(link))
        contact_links = normalized_links
        
        normalized["contact"] = {
            "full_name": contact.get("full_name") or contact.get("name"),
            "email": contact.get("email"),
            "phone": contact.get("phone"),
            "location": contact.get("location"),
            "links": contact_links,
        }

        def as_str(val: Any) -> Optional[str]:
            if val is None:
                return None
            return str(val)

        # Experience
        exp_list = []
        experiences = data.get("experience", []) if isinstance(data, dict) else []
        if not isinstance(experiences, list):
            experiences = []
        
        for exp in experiences:
            if not isinstance(exp, dict):
                continue
            description = exp.get("description") or ""
            bullets = exp.get("bullets") or sentence_bullets(description) if description else []
            bullets = [b for b in bullets if isinstance(b, str) and b.strip()]
            
            exp_list.append({
                "title": exp.get("title") or exp.get("job_title"),
                "company": exp.get("company"),
                "location": exp.get("location"),
                "start_date": as_str(exp.get("start_date")),
                "end_date": as_str(exp.get("end_date")),
                "current": exp.get("current", False) is True,
                "bullets": bullets,
                "technologies": [t for t in (exp.get("technologies", []) or []) if isinstance(t, str) and t.strip()],
                "employment_type": exp.get("employment_type"),
            })
        normalized["experience"] = exp_list

        # Education
        edu_list = []
        for edu in data.get("education", []) if isinstance(data, dict) else []:
            end_date = edu.get("end_date") or edu.get("graduation_year")
            end_date = as_str(end_date)
            edu_list.append({
                "institution": edu.get("institution"),
                "degree": edu.get("degree"),
                "field": edu.get("field"),
                "start_date": as_str(edu.get("start_date")),
                "end_date": end_date,
                "gpa": edu.get("gpa"),
            })
        normalized["education"] = edu_list

        # Projects
        proj_list = []
        projects = data.get("projects", []) if isinstance(data, dict) else []
        if not isinstance(projects, list):
            projects = []
        
        for proj in projects:
            if not isinstance(proj, dict):
                continue
            description = proj.get("description") or ""
            bullets = proj.get("bullets") or sentence_bullets(description) if description else []
            bullets = [b for b in bullets if isinstance(b, str) and b.strip()]
            
            proj_list.append({
                "name": proj.get("name"),
                "role": proj.get("role"),
                "bullets": bullets,
                "stack": [s for s in (proj.get("stack", []) or []) if isinstance(s, str) and s.strip()],
                "link": proj.get("link"),
                "outcome": proj.get("outcome"),
            })
        normalized["projects"] = proj_list

        normalized["skills"] = [s for s in (data.get("skills", []) if isinstance(data, dict) else []) if isinstance(s, str) and s.strip()]
        normalized["certifications"] = [c for c in (data.get("certifications", []) if isinstance(data, dict) else []) if isinstance(c, dict)]
        normalized["achievements"] = [a for a in (data.get("achievements", []) if isinstance(data, dict) else []) if isinstance(a, str) and a.strip()]
        normalized["extracurricular"] = [e for e in (data.get("extracurricular", []) if isinstance(data, dict) else []) if isinstance(e, str) and e.strip()]
        if not normalized["extracurricular"] and isinstance(data, dict):
            alt_vol = data.get("volunteering") or data.get("volunteer") or []
            if isinstance(alt_vol, list):
                normalized["extracurricular"] = [v for v in alt_vol if isinstance(v, str) and v.strip()]
        normalized["languages"] = [l for l in (data.get("languages", []) if isinstance(data, dict) else []) if isinstance(l, str) and l.strip()]
        normalized["interests"] = [i for i in (data.get("interests", []) if isinstance(data, dict) else []) if isinstance(i, str) and i.strip()]

        return normalized

    def _extract_json(self, text: str) -> dict:
        """Extract JSON from LLM response, handling markdown code blocks and extra text."""
        text = text.strip()
        
        # Remove markdown code blocks
        match = re.search(r'```(?:json)?\s*({.*?})\s*```', text, re.DOTALL)
        if match:
            text = match.group(1)
        
        # Find JSON object if wrapped in text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            text = match.group(0)
        
        # Clean up common issues
        text = text.strip()
        
        # Parse JSON
        data = json.loads(text)
        
        # Ensure all required keys exist with defaults
        defaults = {
            "contact": {"full_name": None, "email": None, "phone": None, "location": None, "links": []},
            "summary": None,
            "experience": [],
            "projects": [],
            "education": [],
            "skills": [],
            "certifications": [],
            "achievements": [],
            "extracurricular": [],
            "languages": [],
            "interests": [],
        }
        
        # Merge with defaults
        for key, default_value in defaults.items():
            if key not in data:
                data[key] = default_value
        
        return data

    def build(self, raw_input: str, *, output_pdf: Optional[str] = None, output_docx: Optional[str] = None) -> Resume:
        parsed = self.parse_input(raw_input)

        # If user provided JSON, normalize and only run rewrite
        resume_data: dict[str, Any]
        try:
            user_json = json.loads(parsed)
            if isinstance(user_json, dict):
                resume_data = self._normalize_resume_input(user_json)
                rewritten = self.llm.complete(
                    system_prompt="You improve resume text without fabrication. Return ONLY valid JSON, no markdown or extra text.",
                    user_prompt=rewrite_prompt(json.dumps(resume_data)),
                    temperature=0.1,
                )
                resume_data = self._extract_json(rewritten)
            else:
                raise ValueError
        except Exception:
            # Fall back to extraction flow for plain text
            extraction = self.llm.complete(
                system_prompt="You extract resume data to JSON only. Return ONLY valid JSON, no markdown or extra text.",
                user_prompt=extraction_prompt(parsed),
                temperature=0.1,
            )
            resume_data = self._extract_json(extraction)
            rewritten = self.llm.complete(
                system_prompt="You improve resume text without fabrication. Return ONLY valid JSON, no markdown or extra text.",
                user_prompt=rewrite_prompt(json.dumps(resume_data)),
                temperature=0.1,
            )
            resume_data = self._extract_json(rewritten)

        # Validate and create Resume object
        try:
            resume = Resume.model_validate(resume_data)
        except Exception as e:
            # Try to clean up and retry
            if resume_data.get("certifications"):
                resume_data["certifications"] = [c for c in resume_data["certifications"] if isinstance(c, dict) and c.get("name")]
            if resume_data.get("skills"):
                resume_data["skills"] = [s for s in resume_data["skills"] if isinstance(s, str) and s.strip()]
            resume = Resume.model_validate(resume_data)

        if output_pdf:
            pdf_renderer = PDFRenderer(self.env)
            pdf_renderer.render(resume, template_name=self.template_name, output_path=output_pdf)

        if output_docx:
            docx_renderer = DocxRenderer()
            docx_renderer.render(resume, output_path=output_docx)

        return resume
