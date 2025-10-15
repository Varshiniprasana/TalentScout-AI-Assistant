import openai
import re
import random

openai.api_key = "YOUR_OPENAI_API_KEY"

class InterviewBot:
    def __init__(self, language="en"):
        self.state = "greet"
        self.candidate = {}
        self.tech_stack = {}
        self.role = ""
        self.language = language
        self.questions = []
        self.current_question_index = 0

        
        self.role_questions_prompt = """
        You are an expert interviewer.
        Candidate Role: {role}
        Candidate Tech Stack: {tech_stack}
        Generate 3-5 challenging technical questions for each technology.
        Respond in {language}.
        """

    def handle_input(self, user_input):
        if self.state == "greet":
            self.state = "name"
            return self._bot_speak("Hello! Let's start your interview. What's your full name?")
        
        elif self.state == "name":
            self.candidate["name"] = user_input
            self.state = "email"
            return self._bot_speak("Please enter your email address.")
        
        elif self.state == "email":
            if not self._valid_email(user_input):
                return self._bot_speak("Please enter a valid email address.")
            self.candidate["email"] = user_input
            self.state = "phone"
            return self._bot_speak("Your phone number, please.")
        
        elif self.state == "phone":
            self.candidate["phone"] = user_input
            self.state = "experience"
            return self._bot_speak("How many years of experience do you have?")
        
        elif self.state == "experience":
            self.candidate["experience"] = user_input
            self.state = "role"
            return self._bot_speak("What position/role are you applying for?")
        
        elif self.state == "role":
            self.role = user_input
            self.state = "location"
            return self._bot_speak("Where are you currently located?")
        
        elif self.state == "location":
            self.candidate["location"] = user_input
            self.state = "languages"
            return self._bot_speak("Please list the programming languages you are proficient in, separated by commas.")
        
        elif self.state == "languages":
            self.tech_stack["languages"] = [x.strip() for x in user_input.split(",")]
            self.state = "frameworks"
            return self._bot_speak("Please list the frameworks you are proficient in, separated by commas.")
        
        elif self.state == "frameworks":
            self.tech_stack["frameworks"] = [x.strip() for x in user_input.split(",")]
            self.state = "databases"
            return self._bot_speak("Please list the databases you are proficient in, separated by commas.")
        
        elif self.state == "databases":
            self.tech_stack["databases"] = [x.strip() for x in user_input.split(",")]
            self.state = "tools"
            return self._bot_speak("Please list the tools you are proficient in, separated by commas.")
        
        elif self.state == "tools":
            self.tech_stack["tools"] = [x.strip() for x in user_input.split(",")]
            self._generate_questions()
            self.state = "interview"
            return self._ask_next_question()
        
        elif self.state == "interview":
            score, feedback = self._analyze_answer(user_input, self.questions[self.current_question_index-1])
            response = f"Score for this answer: {score}/10\nFeedback: {feedback}\n"
            response += self._ask_next_question()
            return self._bot_speak(response)
        
        else:
            return self._bot_speak("Sorry, I didn't understand that.")

    def _bot_speak(self, message):
        return message

    def _valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)

    def _generate_questions(self):
        tech_list = self.tech_stack.get("languages", []) + self.tech_stack.get("frameworks", []) + self.tech_stack.get("databases", []) + self.tech_stack.get("tools", [])
        tech_stack_str = ", ".join(tech_list)
        prompt = self.role_questions_prompt.format(role=self.role, tech_stack=tech_stack_str, language=self.language)
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI technical interviewer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.7
        )
        questions_text = response.choices[0].message.content.strip()
        
        self.questions = [q.strip() for q in questions_text.split("\n") if q.strip() != ""]

    def _ask_next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            return f"Please answer the following question:\n{question}"
        else:
            self.state = "done"
            return "Interview completed! Thank you for your time."

    def _analyze_answer(self, answer, question):
        
        prompt = f"""
        You are an expert interviewer.
        Question: {question}
        Candidate Answer: {answer}
        Provide a score out of 10 and a short feedback.
        Respond in {self.language}.
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI technical evaluator."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        text = response.choices[0].message.content.strip()
        
        score_match = re.search(r"(\d{1,2})/10", text)
        score = int(score_match.group(1)) if score_match else random.randint(5,10)
        return score, text

