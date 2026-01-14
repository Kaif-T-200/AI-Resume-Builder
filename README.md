<h1 align="center"> # 🧠 AI Resume Builder (Local-First) </h1>

An **AI-powered Resume Builder** that converts raw, unstructured resume data into **professional, ATS-friendly resumes** using Large Language Models.  
The project focuses on **accuracy, structure, and clean formatting** without fabricating information.

🚀 **Live App:**  
https://ai-resume-builder-kaif-t-200.streamlit.app/

---

## ✨ Features

- 📝 Accepts resume input as **Plain Text** or **JSON**
- 🤖 AI-powered extraction and rewriting (no data fabrication)
- 🔁 Supports **multiple AI providers** (OpenAI & Groq)
- 🎨 Multiple resume templates (Minimal, Corporate, Moderate)
- 📄 Export resume in **DOCX** format
- 📊 Structured resume preview in JSON format
- 🧩 Strict schema validation using Pydantic
- 🖥️ Clean and simple UI built with Streamlit

---

## ⚙️ Tech Stack

- **Language:** Python 3.11  
- **UI:** Streamlit  
- **AI Models:** OpenAI / Groq  
- **Data Validation:** Pydantic  
- **Templating:** Jinja2  
- **Document Export:**  
  - DOCX → python-docx  
  - PDF → WeasyPrint (local only)

---

## 🚀 Getting Started (Local Setup)

### Clone the repository
```bash
git clone https://github.com/Kaif-T-200/AI-Resume-Builder.git
cd AI-Resume-Builder
```
### Create virtual environment
```bash
python -m venv venv  
source venv/bin/activate  
```
### Install dependencies
```bash
pip install -e .
```
(Optional – for PDF support)  
```bash
pip install weasyprint
```
### Run the app
```bash
streamlit run app.py
```
---

## 🌐 Deployment Notes

- Deployed on **Streamlit Cloud**
- PDF generation requires system-level dependencies
- Streamlit Cloud does **not support WeasyPrint system libraries**
- DOCX download works fully on cloud
- PDF export works in local environments

---

## 🔮 Future Enhancements

- Resume ATS scoring & keyword optimization  
- Cover letter generation  
- LinkedIn / GitHub profile import  
- Multi-language resume support  
- Resume version history  
- Improved extraction accuracy for edge cases  

---

## 👨‍💻 Author

**Kaif Tarasgar**  
[LinkedIn](https://www.linkedin.com/in/kaif-tarasgar-0b5425326/) • [Twitter/X](https://x.com/Kaif_T_200)

---

## 📄 License

This project is licensed under the **[MIT](https://github.com/Kaif-T-200/AI-Resume-Builder/blob/main/LICENSE).**  
Feel free to use, modify, and distribute with attribution.
