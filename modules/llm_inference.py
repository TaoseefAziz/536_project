import os
import openai

# Set your OpenAI API key in your environment variables.
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_resume_optimization(master_resume_text, job_description, use_local_llm=False):
    """
    Generates an optimized resume text using the provided master resume and job description.
    
    If use_local_llm is True, returns a stub response for local LLM inference.
    Otherwise, it calls the OpenAI API using the 4o mini engine.
    """
    if use_local_llm:
        # Stub for local LLM inference (to be replaced with an actual call to Ollama or a local model).
        return "Local LLM functionality is not yet implemented. [Stub response]"
    else:
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

