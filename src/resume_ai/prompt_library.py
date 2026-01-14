from textwrap import dedent


def extraction_prompt(raw_text: str) -> str:
        return dedent(
            """
                You are a resume JSON extractor. Convert the user's input to this exact JSON structure:
                {{
                    "contact": {{"full_name": "string or null", "email": "string or null", "phone": "string or null", "location": "string or null", "links": []}},
                    "summary": "string or null",
                    "experience": [{{"title": "string or null", "company": "string or null", "location": "string or null", "start_date": "YYYY-MM-DD or null", "end_date": "YYYY-MM-DD or null", "current": false, "bullets": [], "technologies": [], "employment_type": "string or null"}}],
                    "projects": [{{"name": "string or null", "role": "string or null", "bullets": [], "stack": [], "link": "string or null", "outcome": "string or null"}}],
                    "education": [{{"institution": "string or null", "degree": "string or null", "field": "string or null", "start_date": "YYYY-MM-DD or null", "end_date": "YYYY-MM-DD or null", "gpa": "string or null"}}],
                    "skills": ["string"],
                    "certifications": [{{"name": "string or null", "issuer": "string or null", "date_obtained": "YYYY-MM-DD or null", "credential_id": "string or null"}}],
                    "achievements": ["string"],
                    "extracurricular": ["string"],
                    "languages": ["string"],
                    "interests": ["string"]
                }}

                RULES (CRITICAL):
                - Extract only what exists in the input. Use null or empty arrays for missing data.
                - NEVER invent employers, dates, certifications, or experience.
                - Return ONLY valid JSON. No markdown, code blocks, or explanations.
                - Dates must be YYYY-MM-DD format or null.
                - Arrays like "bullets", "skills", "languages" must always be arrays (can be empty).
                - Keep all field names exactly as shown above.

                USER INPUT:
                {raw_text}
        
                Return ONLY the JSON object, nothing else:
                """
            ).format(raw_text=raw_text).strip()


def rewrite_prompt(structured_json: str) -> str:
    return dedent(
        f"""
        You improve resume text for clarity and impact without adding false information.
        
        RULES (CRITICAL):
        - Do NOT add new employers, dates, certifications, or skills.
        - Only improve wording of existing bullets.
        - Use action verbs, but keep facts accurate.
        - Tense: current roles (present), past roles (past).
        - Return ONLY valid JSON. No markdown, code blocks, or explanations.
        - Keep exact field names and structure from input.

        INPUT JSON:
        {structured_json}
        
        Return ONLY the improved JSON object, nothing else:
        """
    ).strip()
