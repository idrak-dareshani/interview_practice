import streamlit as st
import anthropic
import re
import os
from dotenv import load_dotenv

load_dotenv()
apiKey = os.getenv("ANTHROPIC_API_KEY")

# Initialize Claude client
client = anthropic.Anthropic(api_key=apiKey)

def generate_mcqs(role, skills, exp, num_qs=5):
    prompt = f"""
    You are an expert interview coach. Generate {num_qs} multiple-choice questions 
    for a candidate applying for the role: {role}.
    Candidate's skills: {', '.join(skills)}.
    Experience: {exp} years.

    STRICT FORMAT:
    Q1. Question text
    A) Option 1
    B) Option 2
    C) Option 3
    D) Option 4
    Answer: B

    Q2. Question text
    ...
    """
    response = client.messages.create(
        model="claude-4-sonnet-20250514",
        max_tokens=1200,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )
    return response.content[0].text

def get_feedback(role, skills, exp, results):
    prompt = f"""
    The candidate just completed an interview practice.

    Role: {role}
    Skills: {skills}
    Experience: {exp} years

    Results:
    {results}

    Please provide:
    1. A brief evaluation of their performance
    2. Strengths
    3. Weaknesses
    4. Suggestions for improvement
    """
    response = client.messages.create(
        model="claude-4-sonnet-20250514",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.6,
    )
    return response.content[0].text

# === Streamlit UI ===
st.title("🎯 AI Interview Practice")
st.write("Practice multiple-choice interview questions tailored to your skills")

# Candidate profile
role = st.text_input("Role (e.g., Data Scientist, Backend Developer or any professional role)")
skills = st.text_input("Enter your skills (comma-separated)")
exp = st.number_input("Years of experience", min_value=0, max_value=50, step=1)
num_qs = st.slider("How many Questions?", 1, 10, 5)

if st.button("Generate Questions"):
    if not role or not skills:
        st.warning("Please enter both role and skills")
    else:
        with st.spinner("Generating Questions..."):
            mcqs_text = generate_mcqs(role, [s.strip() for s in skills.split(",")], exp, num_qs)
            st.session_state.mcqs = mcqs_text
            st.session_state.answers = {}

# Display MCQs interactively
if "mcqs" in st.session_state:
    st.subheader("Your Questions")

    # Remove any intro text before Q1
    raw_text = st.session_state.mcqs
    
    match = re.search(r"(Q\s*1\.|1\.)", raw_text)
    if match:
        mcqs_text = raw_text[match.start():]
    else:
        mcqs_text = raw_text

    # Split questions using regex
    questions = re.split(r"(?:Q\s*\d+\.|\n\d+\.)", mcqs_text)
    questions = [q.strip() for q in questions if q.strip()]

    q_data = []    # store (question, options, correct)
    for idx, q in enumerate(questions, 1):
        parts = q.split("Answer:")
        question_block = parts[0].strip()
        correct = parts[1].strip() if len(parts) > 1 else None

        # Extract question and options
        lines = [line.strip() for line in question_block.splitlines() if line.strip()]
        if not lines:
            continue

        question_text = lines[0]
        options = [line for line in lines[1:] if re.match(r"^[A-D]\)", line)]

        if options:
            st.markdown(f"**Q{idx}. {question_text}**")
            choice = st.radio(
                f"Choose your answer for Q{idx}", 
                options, 
                key=f"q{idx}",
                index=None)
            st.session_state.answers[idx] = (choice, correct, question_text)
            q_data.append((question_text, options, correct))

    if st.button("Finish Quiz"):
        correct_count = 0
        wrong_count = 0
        results_text = []

        st.markdown("---")

        unanswered = [idx for idx, (choice, _, _) in st.session_state.answers.items() if not choice]
        if unanswered:
            st.warning(f"Please answer all questions before finishing. Unanswered: {unanswered}")
        else:

            st.subheader("📊 Summary")
            for idx, (choice, correct, question_text) in st.session_state.answers.items():
                        if correct and choice.startswith(correct):
                            st.success(f"Q{idx}: ✅ Correct — {question_text}")
                            correct_count += 1
                        else:
                            st.error(f"Q{idx}: ❌ Wrong — {question_text} | Correct answer: {correct}")
                            wrong_count += 1

                        results_text.append(f"Q{idx}: Your Answer = {choice}, Correct = {correct}")

            st.write(f"Correct: {correct_count}, Wrong: {wrong_count}, Total: {correct_count + wrong_count}")

            st.markdown("---")

            # Generate AI feedback
            with st.spinner("Generating feedback..."):
                feedback = get_feedback(role, skills, exp, "\n".join(results_text))
                st.subheader("💡 AI Feedback")
                st.write(feedback)