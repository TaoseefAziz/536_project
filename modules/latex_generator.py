import subprocess
import os
import tempfile
import re
import unicodedata
from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader


def generate_latex(resume_text):
    parsed = parse_structured_resume(resume_text)
    print("Parsed keys:", parsed.keys())
    print("Values:", {k: len(v.strip()) for k, v in parsed.items()})


    env = Environment(loader=FileSystemLoader("templates"))
    env.filters['escape_tex'] = escape_latex_special_chars  # register filter

    template = env.get_template("resume_template.tex")
    latex_code = template.render(parsed)
    return latex_code




def compile_latex_to_pdf(latex_string, output_filename="optimized_resume.pdf"):
    """
    Compiles the LaTeX string to a PDF file using pdflatex.
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            tex_file_path = os.path.join(tmpdirname, "document.tex")
            with open(tex_file_path, "w", encoding="utf-8") as tex_file:
                tex_file.write(latex_string)
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file_path],
                cwd=tmpdirname,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            pdf_path = os.path.join(tmpdirname, "document.pdf")
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            with open(output_filename, "wb") as out_file:
                out_file.write(pdf_data)
            return output_filename
    except subprocess.CalledProcessError as e:
        error_output = e.stdout.decode(errors="replace") + "\n" + e.stderr.decode(errors="replace")
        return f"Error during LaTeX compilation: {error_output}"


def split_resume_sections(text):
    """
    Dynamically splits resume text into ordered LaTeX-ready sections using keyword-based heuristics.
    Returns tuple in order: contact, education, experience, projects, tech, other.
    """
    section_patterns = {
        r"(contact|linkedin|email|phone|github)": "contact",
        r"education": "education",
        r"(experience|work)": "experience",
        r"(project|portfolio)": "projects",
        r"(technical skills|technologies|tools|programming)": "tech",
        r"(additional|certificates|references|summary)": "other"
    }

    current_section = "other"
    sections = OrderedDict()

    lines = text.splitlines()
    for line in lines:
        lower = line.strip().lower()
        matched = False
        for pattern, section_name in section_patterns.items():
            if re.search(pattern, lower):
                current_section = section_name
                matched = True
                break

        if current_section not in sections:
            sections[current_section] = []
        if not matched or section_name != current_section:
            sections[current_section].append(line.strip())

    for name in ["contact", "education", "experience", "projects", "tech", "other"]:
        if name not in sections:
            sections[name] = []

    # Format skills with LaTeX \item and strip markdown-style bullets
    tech_latex = "\n".join(
        f"\\item {line.lstrip('-* ').strip()}" for line in sections["tech"] if line.strip()
    )

    return (
        "\n".join(sections["contact"]).strip(),
        "\n".join(sections["education"]).strip(),
        "\n".join(sections["experience"]).strip(),
        "\n".join(sections["projects"]).strip(),
        tech_latex,
        "\n".join(sections["other"]).strip()
    )


def escape_latex_special_chars(text):

    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    replacements = {
        '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#',
        '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}',
        '^': r'\^{}', '\\': r'\textbackslash{}',
    }
    regex = re.compile('|'.join(re.escape(key) for key in replacements.keys()))
    return regex.sub(lambda match: replacements[match.group()], text)



def parse_structured_resume(text):
    """
    Dynamically parses LLM-structured resume text based on SECTION headers.
    """
    default_fields = {
        "name": "",
        "location": "",
        "email": "",
        "phone": "",
        "linkedin": "",
        "github": "",
        "summary": "",
        "education": "",
        "experience": "",
        "mentorship": "",
        "projects": "",
        "skills": ""
    }

    sections = default_fields.copy()
    # Map non-standard or aliased keys to our internal schema
    key_aliases = {
        "work_experience": "experience",
        "teaching_&_mentorship": "mentorship",
        "teaching_and_mentorship": "mentorship",
        "projects": "projects",
        "skills": "skills"
    }

    current = None
    lines = text.splitlines()

    for line in lines:
        if line.strip().lower().startswith("section:"):
            raw_key = line.split(":", 1)[1].strip().lower().replace(" ", "_")
            key = key_aliases.get(raw_key, raw_key)  # Normalize aliases
            if key not in sections:
                sections[key] = ""  # Allow custom fields, too
            current = key
            continue


        if current:
            sections[current] += line.strip() + "\n"

    return {k: v.strip() for k, v in sections.items()}
