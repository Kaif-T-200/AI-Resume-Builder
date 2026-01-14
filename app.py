import json
import io
import os
import streamlit as st
from pathlib import Path
from src.resume_ai.pipeline import ResumeProcessor
from src.resume_ai.providers.openai_provider import OpenAIProvider
from src.resume_ai.providers.groq_provider import GroqProvider
from src.resume_ai.config import OpenAISettings


def main():
    st.set_page_config(page_title="AI Resume Builder", layout="wide", initial_sidebar_state="expanded")
    
    st.title("🚀 AI Resume Builder")
    st.markdown("Transform your raw resume into a polished, ATS-friendly document using AI.")
    
    # Sidebar: Settings
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # API Key inputs
        st.subheader("AI Provider")
        openai_key = st.text_input(
            "OpenAI API Key (Optional)",
            type="password",
            help="Paste your OpenAI API key here"
        )
        
        groq_key = st.text_input(
            "Groq API Key (Optional)",
            type="password",
            help="Paste your Groq API key here (free tier available)"
        )
        
        # Determine which provider to use (allow user choice if both provided)
        available_providers = []
        if openai_key:
            available_providers.append("OpenAI")
        if groq_key:
            available_providers.append("Groq")

        if len(available_providers) > 1:
            provider_name = st.selectbox(
                "Choose which provider to use",
                available_providers,
                help="If OpenAI is rate limited, use Groq (Llama 3.3 70B model, fast & free)"
            )
        elif available_providers:
            provider_name = available_providers[0]
        else:
            provider_name = None

        api_key = openai_key if provider_name == "OpenAI" else groq_key if provider_name == "Groq" else None
        
        template = st.selectbox(
            "Choose Template",
            ["minimal", "corporate", "moderate"],
            help="Select a resume template style"
        )
        st.divider()
        if not api_key:
            st.warning("⚠️ Please provide an OpenAI or Gemini API key above.")
        else:
            st.success(f"✓ Using {provider_name}")
    
    # Main content
    col1, col2 = st.columns([1.5, 1], gap="medium")
    
    with col1:
        st.header("📝 Enter Your Resume Data")
        input_mode = st.radio("Input Format", ["Plain Text", "JSON"], horizontal=True)
        
        if input_mode == "Plain Text":
            raw_input = st.text_area(
                "Paste your resume or unfinished data",
                height=300,
                placeholder="E.g., John Doe\nSoftware Engineer at Acme Corp (2023-2024)\n- Built React dashboards\n..."
            )
        else:
            raw_input = st.text_area(
                "Paste JSON resume data",
                height=300,
                value=json.dumps({
                    "contact": {"full_name": "", "email": "", "phone": "", "location": ""},
                    "experience": [],
                    "education": [],
                    "skills": []
                }, indent=2),
                placeholder='{"contact": {...}, "experience": [...], ...}'
            )
    
    with col2:
        st.header("💾 Export Options")
        col_pdf, col_docx = st.columns(2)
        with col_pdf:
            export_pdf = st.checkbox("PDF", value=True)
        with col_docx:
            export_docx = st.checkbox("DOCX", value=False)
        
        st.divider()
        st.subheader("Preview")
        st.info("Resume JSON will appear here after generation.")
    
    # Generate button
    st.divider()
    if st.button("✨ Generate Resume", type="primary", use_container_width=True):
        if not raw_input.strip():
            st.error("Please enter your resume data.")
            return
        
        if not api_key:
            st.error("❌ Please provide an API key (OpenAI or Groq) in the sidebar.")
            return
        
        try:
            with st.spinner("🤖 Analyzing your resume with AI..."):
                # Initialize provider based on which key was provided
                if provider_name == "OpenAI":
                    from src.resume_ai.config import OpenAISettings
                    settings = OpenAISettings(api_key=openai_key)
                    llm = OpenAIProvider(settings)
                elif provider_name == "Groq":
                    llm = GroqProvider(api_key=groq_key)
                else:
                    st.error("❌ No API key provided!")
                    return
                
                # Process resume
                processor = ResumeProcessor(llm, template_name=template)
                resume = processor.build(raw_input)
                
            st.success("✅ Resume generated successfully!")
            
            # Show structured resume
            with st.expander("📊 Structured Resume (JSON)", expanded=False):
                st.json(resume.model_dump())
            
            # Export section with both download buttons
            st.subheader("⬇️ Download Your ATS-Friendly Resume")
            col_pdf, col_docx = st.columns(2)
            
            with col_pdf:
                try:
                    pdf_path = "/tmp/resume.pdf"
                    with st.spinner("Generating PDF..."):
                        processor.build(raw_input, output_pdf=pdf_path)
                    with open(pdf_path, "rb") as f:
                        pdf_data = f.read()
                    st.download_button(
                        label="📥 PDF",
                        data=pdf_data,
                        file_name="resume.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
                except ImportError:
                    st.warning("⚠️ PDF support requires WeasyPrint. Install with: `pip install weasyprint`")
                except Exception as e:
                    st.error(f"PDF Error: {str(e)}")
            
            with col_docx:
                try:
                    docx_path = "/tmp/resume.docx"
                    with st.spinner("Generating DOCX..."):
                        processor.build(raw_input, output_docx=docx_path)
                    with open(docx_path, "rb") as f:
                        docx_data = f.read()
                    st.download_button(
                        label="📥 DOCX",
                        data=docx_data,
                        file_name="resume.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        use_container_width=True
                    )
                except Exception as e:
                    st.error(f"DOCX Error: {str(e)}")
        
        except ValueError as e:
            st.error(f"❌ API Key Error: {str(e)}")
            st.info("Ensure your API key is valid and has API credits available.")
        except RuntimeError as e:
            error_str = str(e)
            st.error(f"❌ API Error: {error_str}")
            if "404" in error_str or "Not Found" in error_str:
                st.info("💡 Model not found. Please verify your API key is valid for the Gemini API.")
            elif "rate limit" in error_str.lower():
                st.info("💡 Rate limit exceeded. Try again later or use a different API key.")
            else:
                st.info("Please check your API key, internet connection, and try again.")
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON Parse Error: {str(e)}")
            st.info("The AI didn't return valid JSON. Try simplifying your input or try again.")
        except Exception as e:
            error_msg = str(e)
            if "validation error" in error_msg.lower():
                st.error(f"❌ Data Validation Error:\n{error_msg[:500]}")
                st.info("Some fields don't match the expected format. Try with simpler data.")
            else:
                st.error(f"❌ Error: {error_msg[:500]}")
            st.info("Please check your API key, internet connection, and try again.")
    
    st.divider()
    st.markdown(
        """
        ---
        **Tips:**
        - Use plain text for quick input; AI will extract and structure automatically.
        - JSON input should follow the schema: contact, experience, education, skills, projects, etc.
        - The AI improves clarity without fabricating facts or false experience.
        - All templates are ATS-optimized and print-friendly.
        """
    )


if __name__ == "__main__":
    main()
