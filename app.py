import streamlit as st
import sqlite3
import datetime

# ---------------- Database Setup ----------------
def init_db():
    conn = sqlite3.connect("talentscout.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS candidates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    location TEXT,
                    experience INTEGER,
                    role TEXT,
                    score REAL,
                    feedback TEXT,
                    date TEXT
                )''')
    conn.commit()
    conn.close()

def save_result_to_db(user_info, avg_score, feedback_summary):
    conn = sqlite3.connect("talentscout.db")
    c = conn.cursor()
    c.execute('''INSERT INTO candidates (name, email, phone, location, experience, role, score, feedback, date)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
              (user_info['name'], user_info['email'], user_info['phone'], user_info['location'],
               user_info['experience'], user_info['role'], avg_score, feedback_summary, str(datetime.date.today())))
    conn.commit()
    conn.close()

def get_all_candidates():
    conn = sqlite3.connect("talentscout.db")
    c = conn.cursor()
    c.execute("SELECT * FROM candidates ORDER BY id DESC")
    data = c.fetchall()
    conn.close()
    return data

# ---------------- Question Bank ----------------
QUESTION_BANK = {
    "Python Engineer": [
        {"question": "What are Python decorators and how are they used?",
         "keywords": ["function", "wrapper", "modify", "behavior", "@"]},
        {"question": "Explain the difference between deep copy and shallow copy in Python.",
         "keywords": ["copy", "object", "reference", "independent", "mutable"]},
        {"question": "What is the Global Interpreter Lock (GIL)?",
         "keywords": ["thread", "lock", "python", "parallel", "performance"]},
        {"question": "What are Python generators and why are they useful?",
         "keywords": ["yield", "iterator", "lazy", "memory", "efficient"]},
        {"question": "How do you handle exceptions in Python?",
         "keywords": ["try", "except", "finally", "error", "raise"]},
    ],

    "Data Analyst": [
        {"question": "Explain the difference between inner join and outer join in SQL.",
         "keywords": ["join", "matching", "rows", "null", "difference"]},
        {"question": "What is data cleaning and why is it important?",
         "keywords": ["missing", "duplicate", "format", "clean", "accuracy"]},
        {"question": "How do you handle outliers in a dataset?",
         "keywords": ["remove", "replace", "median", "z-score", "IQR"]},
        {"question": "What is the use of Pandas library in Python?",
         "keywords": ["dataframe", "series", "manipulation", "analyze", "csv"]},
        {"question": "What are some common visualization libraries in Python?",
         "keywords": ["matplotlib", "seaborn", "plotly", "visualize", "graph"]},
    ],

    "SDE (Software Development Engineer)": [
        {"question": "What is the difference between stack and heap memory?",
         "keywords": ["memory", "allocation", "stack", "heap", "dynamic"]},
        {"question": "Explain OOP concepts in simple terms.",
         "keywords": ["inheritance", "polymorphism", "encapsulation", "abstraction", "class"]},
        {"question": "What are time and space complexities?",
         "keywords": ["big o", "complexity", "time", "space", "performance"]},
        {"question": "How does a hash table work?",
         "keywords": ["key", "value", "hash", "collision", "bucket"]},
        {"question": "What is the difference between REST and GraphQL APIs?",
         "keywords": ["api", "endpoint", "query", "data", "rest"]},
    ],

    "Data Scientist": [
        {"question": "What is the difference between supervised and unsupervised learning?",
         "keywords": ["labels", "classification", "clustering", "training", "output"]},
        {"question": "Explain overfitting and how to prevent it.",
         "keywords": ["overfit", "regularization", "cross-validation", "dropout", "bias"]},
        {"question": "What is the role of feature scaling in machine learning?",
         "keywords": ["normalize", "standardize", "scaling", "range", "training"]},
        {"question": "Explain the confusion matrix and its components.",
         "keywords": ["true", "false", "positive", "negative", "accuracy"]},
        {"question": "What is the difference between bagging and boosting?",
         "keywords": ["ensemble", "model", "boost", "combine", "trees"]},
    ]
}

# ---------------- Evaluation Function ----------------
def evaluate_answer(answer, keywords):
    answer_lower = answer.lower()
    unknown_phrases = ["i don't know", "dont know", "not sure", "no idea", "idk"]
    if any(phrase in answer_lower for phrase in unknown_phrases):
        return 0, "Answer not attempted. Score: 0/10"
    matched = sum(1 for kw in keywords if kw in answer_lower)
    if matched == 0:
        return 3, "Relevant keywords missing, needs improvement."
    elif matched < len(keywords) / 2:
        return 6, "Partially correct answer."
    elif matched >= len(keywords) / 2:
        return 9, "Good understanding shown."
    else:
        return 10, "Excellent and complete answer!"

# ---------------- Streamlit Layout ----------------
st.set_page_config(page_title="TalentScout AI", page_icon="🤖", layout="centered")
st.title("🤖 TalentScout AI - Smart Interview Assistant")

init_db()

menu = st.sidebar.selectbox("Select Mode", ["Candidate Mode", "Recruiter Dashboard"])

# ---------------- Candidate Mode ----------------
if menu == "Candidate Mode":
    if "stage" not in st.session_state:
        st.session_state.stage = "personal_info"
        st.session_state.user_info = {}
        st.session_state.current_question = 0
        st.session_state.results = []

    # Step 1: Personal Info
    if st.session_state.stage == "personal_info":
        st.subheader("📝 Candidate Information")

        with st.form("personal_form"):
            name = st.text_input("Full Name")
            email = st.text_input("Email")
            phone = st.text_input("Phone Number")
            location = st.text_input("Current Location")
            experience = st.number_input("Years of Experience", 0, 50)
            role = st.selectbox("Select the Role Applying For", list(QUESTION_BANK.keys()))
            submit_btn = st.form_submit_button("Start Interview")

        if submit_btn:
            if all([name, email, phone, location, experience, role]):
                st.session_state.user_info = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "experience": experience,
                    "role": role,
                }
                st.session_state.stage = "interview"
                st.success(f"Welcome {name}! Starting your {role} interview.")
                st.experimental_rerun()
            else:
                st.warning("Please fill all details before proceeding.")

    # Step 2: Interview
    elif st.session_state.stage == "interview":
        role = st.session_state.user_info["role"]
        questions = QUESTION_BANK[role]
        idx = st.session_state.current_question

        if idx < len(questions):
            q = questions[idx]["question"]
            st.markdown(f"### Question {idx + 1}: {q}")
            answer = st.text_area("Your Answer:")

            if st.button("Submit Answer"):
                if answer.strip():
                    score, feedback = evaluate_answer(answer, questions[idx]["keywords"])
                    st.session_state.results.append((q, answer, score, feedback))
                    st.session_state.current_question += 1
                    st.experimental_rerun()
                else:
                    st.warning("Please enter an answer.")
        else:
            st.session_state.stage = "summary"
            st.experimental_rerun()

    # Step 3: Summary
    elif st.session_state.stage == "summary":
        user = st.session_state.user_info
        total = sum(score for _, _, score, _ in st.session_state.results)
        avg = round(total / len(st.session_state.results), 2)
        st.subheader(f"✅ Interview Completed for {user['name']}")
        st.write(f"**Role:** {user['role']} | **Experience:** {user['experience']} years")
        st.metric("Final Average Score", f"{avg}/10")

        feedback_summary = ""
        for i, (q, a, s, fb) in enumerate(st.session_state.results, 1):
            feedback_summary += f"Q{i}: {q} | Score: {s}/10\n"

        save_result_to_db(user, avg, feedback_summary)

        if avg >= 8:
            st.success("Excellent performance! You have strong technical skills.")
        elif avg >= 6:
            st.info("Good attempt! Some areas need refinement.")
        else:
            st.warning("Needs improvement. Review the fundamentals before the next interview.")

        if st.button("Restart Interview"):
            for key in ["stage", "user_info", "current_question", "results"]:
                st.session_state.pop(key, None)
            st.experimental_rerun()

# ---------------- Recruiter Dashboard ----------------
else:
    st.subheader("📋 Recruiter Dashboard - Candidate Results")
    data = get_all_candidates()
    if data:
        for row in data:
            st.write(f"**Name:** {row[1]} | **Role:** {row[6]} | **Score:** {row[7]}/10 | **Date:** {row[9]}")
            st.caption(f"Feedback: {row[8][:150]}...")
            st.write("---")
    else:
        st.info("No candidates recorded yet.")


