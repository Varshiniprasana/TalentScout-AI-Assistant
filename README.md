1.PROJECT OVERVIEW
TalentScout AI Interview Assistant is an AI chatbot for helping pre-screen technology candidates. The chatbot asks for resume information. Then it prompts technical interview questions based on the candidate's tech stack. It collects responses. It analyzes the responses. It delivers results. The system uses LLMs such as GPT-3/4 to generate and score questions
2.Features
1. collects Personal Information Collection 
2.collect Tech Stack (Languages, Frameworks, Databases, Tools)
3.Technical Question Generation
4.Questions generated dynamically based on declared tech stack.
5.Scoring based on keyword matching.
6.Assigns 0 marks for answers containing “I don’t know” or similar phrases.
7.Provides feedback for improvement.
8.Supports multiple roles: AI/ML Intern, SDE, Data Scientist
9.Tailors questions according to the selected role.

3.User Interface

Developed using Streamlit.

Clean and intuitive interface.

Conversation history displayed above the input bar.

Send button for submitting answers.

Data Handling & Privacy

No sensitive data is stored permanently.

Simulated data handling ensures compliance with privacy best practices.
4.Installation Instructions:
1.clone the repository
git clone <GITHUB_REPO_URL>
cd TalentScout_Chatbot
2.Install dependencies:
pip install -r requirements.txt
3.open api key:
export OPENAI_API_KEY='your_api_key'  # Linux/Mac
setx OPENAI_API_KEY "your_api_key"    # Windows
5.How to run:
streamlit run app.py
(or)
python -m streamlit run app.py
Prompts:
Prompts are designed to guide the LLM to:

Gather structured candidate information.

Generate relevant questions per role and tech stack.

Evaluate candidate responses against predefined keywords.

Assign scores dynamically, with 0 for “I don’t know” responses.
6.challenges and solution:
challenge:Responses that are unknown or irrelevant.
solution:Inserting keyword matching and 0 marks for when saying "I don't know."

challenge:Generate questions dynamically for various tech stacks.
solution:Prompts were used to help generate questions for each declared language/framework/tool to use in interviews.

challenge:Maintaining coherent conversation flow.
solution:Streamlit session state was used to provide the chatbot context from previous inputs.
