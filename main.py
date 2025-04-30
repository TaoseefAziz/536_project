import streamlit as st
from modules import document_extractor, web_scraper, llm_inference, latex_generator

def main():
    st.title("DIY Resume Master")
    st.write("Optimize your resume for your dream job using AI!")
    
    # Sidebar for LLM option selection.
    st.sidebar.header("Settings")
    llm_option = st.sidebar.radio("Select LLM Option:", ("OpenAI API (4o mini)", "Local LLM (Ollama)"))
    use_local_llm = True if llm_option == "Local LLM (Ollama)" else False

    # Zoha cold email ────────────────────────────────────────────────────────
    generate_email = st.sidebar.checkbox(
        "Generate Personalized-Email",
        value=True
    )
    # Zoha cold email ────────────────────────────────────────────────────────

    # File uploader for the master resume.
    resume_file = st.file_uploader("Upload your master resume (PDF or DOCX)", type=["pdf", "docx"])

    # Input field for the job posting URL.
    job_url = st.text_input("Enter the job posting URL:")

    if st.button("Optimize Resume"):
        if resume_file is None:
            st.error("Please upload a resume file (PDF or DOCX).")
        else:
            # Check if file extension is supported.
            ext = resume_file.name.split('.')[-1].lower()
            if ext not in ["pdf", "docx"]:
                st.error("Unsupported file format. Please upload a PDF or DOCX file.")
            elif job_url.strip() == "":
                st.error("Please enter a job posting URL.")
            else:
                st.info("Processing your request...")

                # 1. Extract text from the uploaded document.
                with st.spinner("Extracting text from document..."):
                    master_resume_text = document_extractor.extract_text_from_document(resume_file)
                st.text_area("Extracted Resume Text", master_resume_text, height=300)

                # If extraction fails due to unsupported format, show error.
                if master_resume_text.startswith("Unsupported file format"):
                    st.error(master_resume_text)
                    return

                # 2. Scrape the job description.
                with st.spinner("Scraping job description..."):
                    job_description = web_scraper.get_job_description(job_url)
                
                # 3. Generate the optimized resume using LLM.
                with st.spinner("Generating optimized resume..."):
                    optimized_resume = llm_inference.generate_resume_optimization(
                        master_resume_text, job_description, use_local_llm=False
                    )
                
                

                st.subheader("Optimized Resume Text")
                st.text_area("Result", optimized_resume, height=300)

                # 4. Generate LaTeX content and compile to PDF.
                latex_content = latex_generator.generate_latex(optimized_resume)
                with st.spinner("Compiling LaTeX to PDF..."):
                    pdf_result = latex_generator.compile_latex_to_pdf(latex_content)
                
                if pdf_result and pdf_result.endswith(".pdf"):
                    st.success("PDF generated successfully!")
                    with open(pdf_result, "rb") as pdf_file:
                        st.download_button(
                            label="Download Optimized Resume (PDF)",
                            data=pdf_file,
                            file_name="optimized_resume.pdf",
                            mime="application/pdf"
                        )
                else:
                    st.error(f"Failed to generate PDF: {pdf_result}")
# ─── Zoha cold email───
                if generate_email:
                    with st.spinner("Drafting personalised email (local model)…"):
                        cold_email = llm_inference.generate_cold_email(
                            master_resume_text,   # use the same variable from above
                            job_description   # force local model
                        )
                    st.subheader("Personalized-Email Draft")
                    st.text_area("Personalized-Email", cold_email, height=200)
                    st.download_button(
                        "Download Personalized-Email (.txt)",
                        data=cold_email,
                        file_name="Personalized-email.txt",
                        mime="text/plain"
                    )
# ─── Zoha cold email───
if __name__ == "__main__":
    main()
