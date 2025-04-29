# Smart Resume Skills Enhancer

Smart Resume Skills Enhancer is a web-based tool that analyzes your resume against a job description and identifies which relevant skills are missing. It uses NLP (Natural Language Processing) to extract and compare skills, helping job seekers improve their resume alignment for specific roles.

![image](https://github.com/user-attachments/assets/087d0e97-668c-4a14-949c-807b4cb6e455)

## Features

- Upload your resume as a PDF
- Paste any job description into the app
- Extract and compare relevant skills using spaCy's NLP pipeline
- View skills found in your resume, skills mentioned in the job description, and those you're missing
- Clean, simple UI with no setup required for end users

## Why This Matters

Many resumes fail to match job descriptions closely enough to pass applicant tracking systems (ATS) or impress hiring managers. This tool helps users:

- Quickly identify missing skills for a specific job
- Improve keyword alignment
- Save time reviewing job descriptions manually

## Technologies Used

- **Python** — core scripting
- **spaCy** — NLP for skill extraction using `PhraseMatcher`
- **Streamlit** — frontend and web deployment
- **PyMuPDF** — text extraction from PDF resumes

## File Overview

```
resume_skill_enhancer/
│
├── streamlit_app.py         # Main Streamlit application
├── skills_list.txt          # Master list of recognized skills
├── requirements.txt         # Project dependencies
├── README.md                # This file
```

## Getting Started

To run the app locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/jasoo4/NLP_Resume_Builder.git
   cd NLP_Resume_Builder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the Streamlit app:
   ```bash
   streamlit run streamlit_app.py
   ```

You can now upload your resume and paste a job description to view the results.

## Roadmap

- Add ranked skill importance based on job description frequency
- Suggest example resume lines for missing skills
- Support `.docx` resumes
- Enable report downloading (PDF or plain text)
- Explore integration with external datasets like O*NET

## Author

Jason Antonellis  

## License

This project is open source under the MIT License.
