import subprocess
import os
import tempfile
import re

def generate_latex(resume_text):
    """
    Generates a LaTeX document string for the given resume text.
    """
    safe_text = escape_latex_special_chars(resume_text)
    latex_template = r"""
\documentclass[11pt]{article}
\usepackage[margin=1in]{geometry}
\usepackage{lmodern}
\usepackage[T1]{fontenc}
\usepackage{setspace}
\usepackage{parskip}
\begin{document}
\begin{center}
    {\LARGE \textbf{Optimized Resume}}\\[1em]
\end{center}
\onehalfspacing
%s
\end{document}
    """ % safe_text
    return latex_template

def compile_latex_to_pdf(latex_string, output_filename="optimized_resume.pdf"):
    """
    Compiles the LaTeX string to a PDF file using pdflatex.
    """
    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            tex_file_path = os.path.join(tmpdirname, "document.tex")
            with open(tex_file_path, "w") as tex_file:
                tex_file.write(latex_string)
            result = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", tex_file_path],
                cwd=tmpdirname,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            # Uncomment the following lines to print debug output:
            # print(result.stdout.decode())
            # print(result.stderr.decode())
            pdf_path = os.path.join(tmpdirname, "document.pdf")
            with open(pdf_path, "rb") as pdf_file:
                pdf_data = pdf_file.read()
            with open(output_filename, "wb") as out_file:
                out_file.write(pdf_data)
            return output_filename
    except subprocess.CalledProcessError as e:
        error_output = e.stdout.decode() + "\n" + e.stderr.decode()
        return f"Error during LaTeX compilation: {error_output}"

def escape_latex_special_chars(text):
    """
    Escapes special characters for LaTeX.
    """
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
    }
    regex = re.compile('|'.join(re.escape(key) for key in replacements.keys()))
    return regex.sub(lambda match: replacements[match.group()], text)

