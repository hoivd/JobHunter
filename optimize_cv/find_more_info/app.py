# app.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from .state import State
from .multi_agent import AgentSystem   # ⚡ chỉnh lại path import cho đúng project
import re
async def generate_cv(cv_info: str, jd_info: str, ws):
    # Load API key từ .env
    print("load key")
    load_dotenv(dotenv_path="D:/JobHunter/optimize_cv/.env")
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("⚠️ GOOGLE_API_KEY chưa được set trong file .env")

    # Khởi tạo LLM Gemini
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0,
        api_key=api_key,
    )

    # State đầu vào
    state: State = {
        "cv_info": cv_info,
        "jd_info": jd_info,
        "jd_extracted": "",
        "analysis_result": "",
        "plan_result": "",
        "completed_cv": "",
        "current_step": "agent_jd_extraction",
    }

    # Chạy AgentSystem duy nhất
    agent_system = AgentSystem(llm=llm, ws=ws)
    final_state = await agent_system.run(state)

    # In kết quả
    print("\n=== FINAL RESULT ===")
    print("JD Extracted:", final_state.get("jd_extracted"))
    print("Analysis Result:", final_state.get("analysis_result"))
    print("Plan Result:", final_state.get("plan_result"))
    print("Completed CV:", final_state.get("completed_cv"))

    def extract_latex_from_codeblock(text: str):
            """
            Trích xuất JSON từ block ```json ... ``` trong chuỗi text.
            Trả về dict (hoặc list) nếu parse được, ngược lại trả về None.
            """
            pattern = r"```latex\s*(.*?)\s*```"
            match = re.search(pattern, text, re.DOTALL)

            if not match:
                return None

            json_str = match.group(1)
            return json_str
    cv = extract_latex_from_codeblock(final_state.get("completed_cv"))

    return cv


if __name__ == "__main__":
    # Ví dụ test
    cv_info = """
    Early-career AI/ML engineer with hands-on experience in Deep Learning, NLP, and transformer-based models. Built end-to-end systems in academic projects and hackathons, including LLM integration, semantic search, and real-time data pipelines. Strong Python skills (OOP, design patterns) and proven ability to collaborate in team projects. Eager to apply technical expertise to production systems and grow as an AI Engineer. Technical Skills • Machine Learning Frameworks: PyTorch, Tensorflow, Pandas, Scikit-learn, Matplotlib. • Big Data Tools: Apache Hadoop, Apache Spark, Apache Kafka. • Programming Languages: Python, C++. • Database: MySQL, MongoDB. • Other Tools: Git, Docker, Selenium, Jupyter.

    """

    jd_info = """
            Software Engineering Internship – AI Systems Development- Fall 2025
About GeoComply

We’re GeoComply! We are at the forefront of geolocation, cybersecurity, and anti-fraud innovation, developing and delivering cutting-edge technologies to help ensure regulatory compliance, combat bad online actors, alleviate user friction, and protect businesses from fraud.

Achieving significant business and revenue growth over the past three years and dubbed a tech “Unicorn,” GeoComply has been trusted by leading global brands and regulators for over ten years. Our compliance-grade geolocation technology solutions are installed on over 400 million devices and analyze over 12 billion transactions a year.

At the heart of it all is the people, united by a deep commitment to problem-solving and revolutionizing how people and businesses use the internet to instill confidence in every online interaction. With teams across five countries, three continents, and a global customer base, we have no plans to slow down.

Internship term: September- December
Duration: 4 Months
Hours: 40 hours per week
Work: Ho Chi Minh office

The Role
We are seeking a Software Engineering Intern to join our ML team. In this role, you will contribute to the ongoing development of our multi-agent fraud detection system, leveraging large language models (LLMs), advanced data processing, and modular system design. As an intern, you’ll find yourself constantly challenged and excited about the next big thing.
Key Responsibilities
Develop and implement advanced machine learning models to detect location spoofing patterns within large datasets.
Contribute to the enhancement of a multi-agent AI system designed to detect fraud across complex data streams.
Develop and refine AI agents to improve reasoning, validation, and decision-making capabilities.
Extend platform functionality to handle diverse data formats and integrate new data sources.
Build tools and utilities to support automated analysis, testing, and verification.
Collaborate with engineers and researchers to design, implement, and test system improvements.
Key Technologies You’ll Work With
AI/ML: Large Language Models, multi-agent frameworks, semantic search, transformer models
Programming: Advanced Python development (object-oriented design, design patterns)
Data Processing: XML/JSON parsing, embeddings, structured/unstructured data handling
System Architecture: Multi-agent systems, modular design, configuration management.
Projects You May Work On
Platform Enhancement: Expanding support for multiple data types and fraud scenarios.
AI Agent Development: Enhancing multi-agent reasoning, validation, and detection accuracy.
Tool Development: Creating automated analysis, monitoring, and verification utilities.
System Integration: Connecting various AI modules, APIs, and external data sources.
Who You Are
Currently pursuing or recently graduated in Computer Science, Statistics, Mathematics, or a related quantitative field of study.
Strong Python programming skills, with experience in object-oriented design.
Familiarity or interest in AI/ML concepts, particularly language models and transformers.
Solid problem-solving skills and ability to tackle complex technical challenges.
Enthusiasm for learning new technologies and applying them in real-world projects.
Coursework or project experience in AI, ML, or data systems is a plus.

To check out our amazing benefits and learn more about the internship program, please visit: https://www.geocomply.com/careers/internship/ 

Not sure if you qualify for this role?  We encourage you to apply anyways. At GeoComply, Passion, Hunger and Drive, (aka PhD) count for more than relevant experience or specific skills. 

Our workplace is built on mutual respect and inclusion. We know that diversity of experience and thought has led to connection, innovation, and our company’s success. We welcome applicants of all backgrounds, experiences, beliefs, and identities.

EMPOWER your future with GeoComply. Apply Today!
Salary Range
- ,
Apply Now!

Interested in joining our team? Send us your resume and a cover letter. We can’t wait to meet you!

Commitment to Diversity and Equity.
If you don't tick every box in this job description, please don't rule yourself out. Research suggests that women and other people in underrepresented groups tend to only apply if they meet every requirement. We focus on hiring people who value inclusion, collaboration, adaptability, courage, and integrity rather than ticking boxes, so if this resonates with you, please apply.

Search Firm Representatives Please Read Carefully
We do not accept unsolicited assistance from search firms for employment opportunities. All CVs or resumes submitted by search firms to any employee at our company without a valid written agreement in place for this position will be considered the sole property of our company. No fee will be paid if a candidate is hired by GeoComply due to an agency referral where no existing agreement exists with the GeoComply Talent Acquisition Team. Where agency agreements are in place, introductions must be through engagement by the GeoComply Talent Acquisition Team.


Why GeoComply?

Joining the GeoComply team means you’ll be part of an award-winning company to work, learn and grow. We are fast-paced, high-impact, and have a can-do team culture.

To be successful in our organization, you need an eager attitude, professionalism, and the confidence to willingly work to prove yourself and your ideas, and earn the trust of the organization.

Here’s why we think you’d love working with us.

We’re working towards something big
We’ve built a reputation as the global market leader for geolocation compliance solutions for over 10 years. We’re trusted by customers from all over the world, and the next few years will be particularly exciting as we continue to scale across new markets.

Our values aren’t just a buzzword
Our values are the foundation for what we as a company care about most. They signify the commitment we make to each other around how we act and what we stand for. They are our north star as we work together to build a company we’re all proud to be a part of. Learn more, here.

Diversity, equity, and inclusion are at the core of who we are
In collaboration with our team and external partners, we promote DEI in our recruitment and hiring practices; scholarships and financial aid; training and mentorship programs; employee benefits, and more.

Learning is at the heart of our employee experience
At GeoComply, we foster an environment that empowers every employee to gain the knowledge and abilities needed to perform at their very best and help our organization grow. From a professional development budget to local training opportunities, knowledge-sharing sessions and more, we are continually investing in employee career growth and development.

We believe in being a force for good
We profoundly care about our impact on the world and strive to make meaningful contributions to the communities we work and live in. Our Impact division focuses on philanthropic and social responsibility initiatives, including supporting our local communities, advancing equality, and harnessing our technology to protect vulnerable groups. Learn more, here.

We care about our team
Our GeoComply team is talented, driven and hard-working, and is known for its positive attitude and energy.  At GeoComply, we take care of our employees with the total package. Team members are generously rewarded with competitive salaries, incentives, and a comprehensive benefits program.

We value in-person collaboration
GeoComply culture thrives on a dynamic mix of in-person energy and independent focus and we champion a hybrid work model that blends the energy of in-person collaboration with the flexibility to work from home. Our 3-day in-office policy fosters teamwork and innovation, while also recognizing the importance of individual work styles and needs.

- - - - - - - - - -

At GeoComply, we live our value of Act with Integrity. Our workplace is built on mutual respect and inclusion, and we welcome applicants of all backgrounds, experiences, beliefs, and identities. Creating an accessible interview experience for all candidates is important to us. If you have any requests (big or small) throughout our hiring process, please don’t hesitate to let us know so we can do our best to prioritize your needs.

We care about your privacy and want you to be informed about your rights. Please read our Applicant Privacy Notice before applying for the position.
    """

    cv = generate_cv(cv_info, jd_info)
    print(cv)