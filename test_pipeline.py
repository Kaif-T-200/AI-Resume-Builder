#!/usr/bin/env python3
"""Quick test to validate the resume pipeline."""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from resume_ai.models import Resume
from resume_ai.providers.openai_provider import OpenAIProvider
from resume_ai.config import OpenAISettings
from resume_ai.pipeline import ResumeProcessor


def test_pipeline():
    """Test the pipeline with a sample resume."""
    sample_text = """
    John Doe
    john@example.com | 555-123-4567 | New York, NY
    
    Software Engineer with 3 years experience in Python and React.
    
    Experience:
    - Junior Dev at Tech Corp (2022-2023): Developed API endpoints, improved performance by 20%
    - Intern at Startup Inc (2021-2022): Built web dashboard
    
    Education:
    - B.S. Computer Science, State University (2021)
    
    Skills:
    Python, JavaScript, React, FastAPI, PostgreSQL, Docker
    """
    
    try:
        print("🔑 Initializing OpenAI provider...")
        settings = OpenAISettings.from_env()
        if not settings.api_key:
            print("❌ OPENAI_API_KEY not set!")
            return False
        
        llm = OpenAIProvider(settings)
        print(f"✓ Using model: {settings.model}")
        
        print("\n📝 Processing resume...")
        processor = ResumeProcessor(llm, template_name="minimal")
        resume = processor.build(sample_text)
        
        print("\n✅ Resume generated successfully!")
        print(f"  Name: {resume.contact.full_name}")
        print(f"  Email: {resume.contact.email}")
        print(f"  Skills: {', '.join(resume.skills[:3])}")
        print(f"  Experience entries: {len(resume.experience)}")
        
        print("\n📄 Full resume JSON:")
        print(json.dumps(resume.model_dump(), indent=2))
        
        return True
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_pipeline()
    sys.exit(0 if success else 1)
