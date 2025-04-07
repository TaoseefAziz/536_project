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
    Generates an optimized resume text using the provided master resume and job description.
    If use_local_llm is True, calls the local Ollama model; otherwise, uses the OpenAI API.
    """
    prompt = (
        "You are a resume optimization assistant. "
        "Given the following master resume and job description, generate an optimized resume "
        "tailored for the job. Emphasize relevant skills and experiences.\n\n"
        "Master Resume:\n"
        f"{master_resume_text}\n\n"
        "Job Description:\n"
        f"{job_description}\n\n"
        "Optimized Resume:"
    )
    if use_local_llm:
        # Call the local Ollama model using the helper function
        return generate_with_ollama(prompt)
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Replace with your specific model name if needed.
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1024
            )
            optimized_resume = response.choices[0].message.content.strip()
            return optimized_resume
        except Exception as e:
            return f"Error during OpenAI API call: {str(e)}"


