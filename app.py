from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests

app = Flask(__name__)
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")


@app.route("/", methods=['GET'])
def home():
    question = request.args.get('question', "who are you?")
    user_message = question

    # Expanded profile context to ensure responses stay within expertise
    profile_context = """
        Ali is a **highly skilled Backend Engineer** with over **6 years of experience** in building scalable systems, 
        **FinTech payment automation**, AI-driven solutions, and cybersecurity. He has worked on complex projects in both 
        **FinTech and EdTech**, ensuring high-performance and secure backend architectures.

        **Key Achievements:**
        - Scaled FinTech payment automation systems from **$0 to $5M+ transactions** in under a year.
        - Developed and optimized **LMS platforms** that enhanced content delivery for thousands of learners.
        - Integrated **ChatGPT, Claude, and OpenAI APIs** into various automation and AI-powered business intelligence projects.
        - Passionate about **API security, vulnerability assessment, and Capture The Flag (CTF) competitions**.

        **Technical Expertise:**
        - **Languages:** PHP, Python, JavaScript, C, C++
        - **Frameworks:** Laravel, Django, Livewire, Alpine.js, CodeIgniter
        - **Databases:** MySQL, MongoDB, SQLite, Redis, Elasticsearch
        - **Cloud & DevOps:** AWS, Heroku, Git, Postman, Laravel Telescope
        - **AI & ML Tools:** ChatGPT API, Claude API, OpenAI API, TensorFlow
        - **System Design:** Strong understanding of **LLD (Low-Level Design) & HLD (High-Level Design)**, automation, and backend optimization.
        
        **Past Companies:**
        - Zomentum (FinTech Payments Automation and Reconciliation) (2022-2025)
        - Collegedunia (EdTech College Search Domain) (2021-2022)
        - Chaptervitamins (EdTech LMS) (2019-2021)

        **Education & Achievements:**
        - Graduated from **NIT Hamirpur (Tier-1 Engineering Institute)** with a solid foundation in **Computer Science & problem-solving**.
        - Secured **JEE Mains AIR 8068**, ranking in the **top 1% nationwide**.
        - Active **open-source contributor** building automation tools for developers. Projects are available on Echobash.
        - Volunteered in **NIT-H Literacy Mission**, a student-led initiative educating underprivileged children.

        **Work Ethic & Team Collaboration:**
        - Strong communicator, works closely with **Customer Success & Sales teams** to improve client onboarding.
        - Deep understanding of **backend system scaling, high-availability architectures, and DevOps best practices**.
        - Passionate about **developer-first solutions**, automation, and cybersecurity.
        - I'm a backend developer but i have some hands on frontend too. (My profile is backend-heavy)
        Always focused on **delivering impactful backend solutions**, optimizing performance, and securing systems against threats.
        
        **Hobbies**
        - Playing Table Tennis
        - Working out
        - Reading Tech blogs
        - Singing Song
        - Learning Foreign languages (currently speak english, hindi and spanish and learning indonesian, korean and Norwegian"
        
        """

    # Constructing the prompt for a conversational chatbot experience
    # Constructing the improved prompt
    # Constructing the prompt for a conversational, engaging chatbot experience
    prompt = f"""{profile_context}
        User: {user_message}
        AliBot (strictly based on the above details, in a natural, engaging tone. Give answer in growth-oriented tone.Stick to smaller sentences. Max 2 sentences. Show project or portfolio link if needed echobash.com/portfolio. If questions which are not related to me come, give funny answer and say that learn about ali instead but don't repeat same sentence.
        If Someone asks about past work experience or company name, give the year too.
        If someone ask about well being like how am i, say ali is fine and amazing and busy collaborating with people in human way
        If asked about college or education history, mention that I am from NIT Hamirpur a Tier-1 college and I had second rank opener of the college it means that out of all the JEE mains students who applied for NIT Hamirpur, mine was second rank).
        If asked about an interesting thing about me that i love learning foreign languages currently speak english, hindi and spanish and learning indonesian, korean and Norwegian"
        Give responses with maximum two sentences.
        :"""


    url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-pro:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }
    json_data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    response = requests.post(url=url,
                             headers = headers,
                             json=json_data
                             )

    candidates = response.json().get("candidates", [])
    if candidates:
        # Extract the text from the first candidate's content parts
        answer = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "Sorry, I couldn't understand that.")
    else:
        answer = "Sorry, no response from the AI model."

    return render_template('chatbot.html', answer=answer)



@app.route("/about")
def about_me():
    API_KEY = os.getenv("GEMINI_API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1/models?key={API_KEY}"

    response = requests.get(url)
    print(response.json())
    return "<h1>This is all about meee</h1>"


@app.route("/blog")
def blog():
    return "<marquee>Blog is here</marquee>"


if __name__ == "__main__":
    app.run(debug=True)
