import os
import openai
import subprocess


def generate_with_ollama(system_prompt, user_prompt, model="llama3.2:latest"):
    """
    Calls the local Ollama model using the CLI to generate a response based on the prompt.
    """
    try:
        # clean up the prompts to remove any null characters
        system_prompt = system_prompt.replace('\x00', '')
        user_prompt = user_prompt.replace('\x00', '')
        
        # Combine prompts for Ollama (since it doesn't natively support system/user separation)
        combined_prompt = f"System: {system_prompt}\n\nUser: {user_prompt}"
        
        result = subprocess.run(
            ["ollama", "run", model, combined_prompt],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        return output
    except subprocess.CalledProcessError as e:
        return f"Error during local LLM call: {e.stderr}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def extract_job_requirements(job_description, use_local_llm=False):
    """
    Extracts keywords and important qualities from a job description.
    
    Args:
        job_description (str): The job description text
        use_local_llm (bool): If True, uses the local Ollama model; otherwise, uses OpenAI API
    
    Returns:
        str: A structured analysis of the job requirements
    """
    system_prompt = (
        "You are an expert HR analyst specializing in job requirement analysis. "
        "Extract and categorize the key requirements from the provided job description into these categories:\n"
        "1. Technical Skills: Hard skills and technical knowledge required\n"
        "2. Soft Skills: Communication, teamwork, leadership qualities desired\n"
        "3. Experience: Specific work experiences or background preferred\n"
        "4. Education: Required degrees, certifications, or training\n"
        "5. Keywords: Important terms and phrases that appear frequently or with emphasis\n\n"
        "Be precise and thorough, focusing only on what is explicitly stated or strongly implied in the job description."
    )
    
    user_prompt = (
        "Please analyze the following job description and extract the key requirements, qualifications, and desired attributes:\n\n"
        f"{job_description}\n\n"
        "Format your response as a structured list under the categories mentioned, focusing on elements that would be important "
        "for tailoring a resume to this position."
    )
    
    if use_local_llm:
        return generate_with_ollama(system_prompt, user_prompt)
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            job_requirements = response.choices[0].message.content.strip()
            return job_requirements
        except Exception as e:
            return f"Error during OpenAI API call: {str(e)}"

def generate_resume_optimization(master_resume_text, job_description, use_local_llm=False):
    """
    Generates an optimized resume text using the provided master resume and job description.
    Uses a two-step process:
    1. Extract key requirements from the job description
    2. Optimize the resume based on those requirements
    
    Args:
        master_resume_text (str): The complete master resume text
        job_description (str): The job description text
        use_local_llm (bool): If True, uses the local Ollama model; otherwise, uses OpenAI API
    
    Returns:
        str: The optimized resume text
    """
    # Step 1: Extract key requirements from the job description
    job_requirements = extract_job_requirements(job_description, use_local_llm)
    print(f"Extracted Job Requirements: {job_requirements}")  # Debugging line to check extracted requirements
    print(f"Master Resume Text: {master_resume_text}")  # Debugging line to check master resume text 
    
    # Step 2: Optimize the resume based on the requirements
    system_prompt = (
        "You are an expert resume optimization assistant with experience in HR and recruiting. "
        "Your task is to create a tailored, single-page resume that matches the candidate's "
        "qualifications with the key requirements extracted from the job description. Follow these guidelines carefully:"
        "\n\n"
        "1. ACCURACY: Never fabricate experiences, skills, or qualifications not present in the master resume.\n"
        "2. RELEVANCE: Prioritize experiences and skills that directly align with the extracted requirements.\n"
        "3. KEYWORDS: Incorporate the identified keywords when they genuinely match the candidate's background.\n"
        "4. LEADERSHIP: Highlight relevant leadership experiences when they align with the job requirements.\n"
        "5. QUANTIFICATION: Emphasize quantifiable achievements and metrics when available.\n"
        "6. FORMATTING: Ensure the output is LaTeX-compatible without requiring further formatting adjustments.\n"
        "7. LENGTH: The final resume must fit on a single page - be concise and selective.\n"
        "8. OUTPUT: Provide ONLY the optimized resume text without explanations, notes, or additional commentary.\n"
        "9. LATEX GUIDELINES: LaTeX output should be compatible with pdfLaTeX.\n\n"
    )
    
    user_prompt = (
        "Please optimize my master resume based on the key requirements extracted from the job description. "
        "IMPORTANT: Use ONLY information present in my master resume - do not add or fabricate any details.\n\n"
        "EXTRACTED JOB REQUIREMENTS:\n"
        f"{job_requirements}\n\n"
        "MASTER RESUME:\n"
        f"{master_resume_text}\n\n"
        "Create a focused single-page resume that highlights relevant experiences and skills from my master resume "
        "that best match these job requirements. Provide only the pdfLaTeX-compatible resume text."
    )
    
    if use_local_llm:
        return generate_with_ollama(system_prompt, user_prompt)
    else:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1024
            )
            optimized_resume = response.choices[0].message.content.strip()
            return optimized_resume
        except Exception as e:
            return f"Error during OpenAI API call: {str(e)}"