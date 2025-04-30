import os
import openai
import subprocess


def generate_with_ollama(prompt, model="llama3.2:latest"):
    """
    Calls the local Ollama model using the CLI to generate a response based on the prompt.
    """
    try:
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        return f"Error during local LLM call: {e.stderr}"


def generate_resume_optimization(master_resume_text, job_description, use_local_llm=False):
    """
    Generates an optimized resume using the master resume and job description.
    Returns a LaTeX-friendly structured output using SECTION headers.
    """
    prompt = rf"""
You are an expert resume optimization assistant.

Your task is to generate an optimized resume based on the candidate's master resume and a specific job description.

🎯 GOAL:
- Extract **ALL relevant** experience, education, skills, certifications, achievements, and tools/platforms used from the master resume.
- Rephrase or enhance it only if necessary to match the job description.
- Keep every key accomplishment and number intact.

📌 FORMAT:
Respond using this **exact SECTION-based format**. Do **NOT** use LaTeX commands like \section*.  
Use LaTeX-friendly formatting **inside sections only** (e.g., \textbf{{}}, \begin{{itemize}}...\end{{itemize}}).

---

SECTION: Name  
<Full name>

SECTION: Location  
<City, State>

SECTION: Email  
<Email address>

SECTION: Phone  
<Phone number>

SECTION: LinkedIn  
<LinkedIn URL>

SECTION: GitHub  
<GitHub URL>

SECTION: Summary  
<2–4 sentence summary of the candidate’s strengths and experience>

SECTION: Education  
<Include degree, institution, location, and dates. Use LaTeX formatting.>

SECTION: Work Experience  
Use \begin{{itemize}}...\end{{itemize}} with rich bullet points, responsibilities, impact metrics, and tools used.

SECTION: Teaching & Mentorship  
<Optional — only include if the original resume has it. Use bullet formatting.>

SECTION: Projects  
<List projects with \textbf{{title}} and bullet point highlights. Show outcomes and tech used.>

SECTION: Skills  
Group into: Design Tools, Web Tech, Soft Skills, etc. Use LaTeX \textbf{{}} and commas.

---

✅ Use real values.  
❌ Do not include placeholder text or brackets.  
✅ Keep numbers (e.g., "boosted engagement by 32%").  
✅ Retain brand names, platforms (Adobe, HTML/CSS, etc.), and job titles.

---

Master Resume:
{master_resume_text}

Job Description:
{job_description}

Optimized Resume:
"""



    if use_local_llm:
        return generate_with_ollama(prompt)
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1800
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error during OpenAI API call: {str(e)}"


# ─── Zoha cold email───
def generate_cold_email(
    master_resume_text: str,
    job_description: str,
    *,
    recipient_title: str = "Hiring Manager",
    use_local_llm: bool = False
) -> str:
    """
    Creates a concise (≤150 words) cold-outreach email that:
    • greets the recipient (by title),
    • references the exact job title & company if present,
    • highlights 1–2 keyword-matching strengths from the resume,
    • ends with a polite call-to-action.
    """
    prompt = f"""
You are an expert career-coach copywriter.

Task: Write a short, persuasive cold-outreach email (max 150 words)
to **{recipient_title}** for the role described below, using the
candidate information provided. Do not invent achievements
that aren’t in the resume.

Tone: warm, professional, confident.
Style: plain text, no markup.

Master Resume (full):
\"\"\"{master_resume_text}\"\"\"

Job Description:
\"\"\"{job_description}\"\"\"

Cold Email:
"""
    if use_local_llm:
        return generate_with_ollama(prompt)
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=350
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"Error during OpenAI API call: {e}"
# ─── Zoha cold email───