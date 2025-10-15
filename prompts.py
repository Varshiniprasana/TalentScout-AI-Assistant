# prompts.py

INFO_PROMPT = """
Collect the following information from the candidate:
- Full Name
- Email
- Phone Number
- Years of Experience
- Desired Position(s)
- Current Location
- Tech Stack (programming languages, frameworks, databases, tools)
Respond in JSON format.
"""

TECH_QUESTION_PROMPT = """
Candidate has the following tech stack: {tech_stack}.
Generate 3-5 technical questions per technology to assess proficiency.
Format output as JSON with each tech as key and list of questions as value.
"""
