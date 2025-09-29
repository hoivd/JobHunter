
from langfuse import Langfuse
from langfuse import observe, get_client
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

# ====== Cấu hình Langfuse ======
langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

@observe
def test_prompt_extract_jd(prompt: str, candidate_info: str, evaluation: str,job_description: str, model: str = "gemini-1.5-flash"):
    # Tạo prompt hoàn chỉnh
    full_prompt = prompt.format(candidate_info=candidate_info,
                                evaluation=evaluation,
                                job_description=job_description) 
    gemini_model = genai.GenerativeModel(model)
    response = gemini_model.generate_content(full_prompt)
    return response.text
 
if __name__ == "__main__":
    prompt = """
Bạn là một hệ thống lập kế hoạch thông minh để hỗ trợ viết CV.  
Nhiệm vụ của bạn là xác định **mission to complete** – tức là các nhiệm vụ cụ thể cần thực hiện để thu thập đủ thông tin viết CV.  

Đầu vào bạn nhận được:  
- Bộ thông tin ứng viên (candidate_info): {candidate_info}  
- Đánh giá mức độ đầy đủ, thông tin cần bổ sung cũng như lời khuyên (evaluation): {evaluation}  
- Yêu cầu từ Job Description (job_description): {job_description}  

Mission to complete của bạn cần có:  
1. Phân tích kỹ job_description để xác định yêu cầu quan trọng (kỹ năng, công nghệ, kinh nghiệm, thành tựu mong đợi).  
2. Đối chiếu evaluation để biết ứng viên đang thiếu gì.  
3. Từ hai nguồn này, tạo ra các **mission chi tiết**, trong đó:  
   - **name**: tên nhiệm vụ  
   - **goal**: mục tiêu chung cần đạt  
   - **objective**: yêu cầu chi tiết về dữ liệu cần thu thập (ví dụ: không chỉ liệt kê project mà phải có mô tả vai trò, công nghệ, kết quả, thách thức giải quyết → tùy theo JD và evaluation)  
   - **priority**: high nếu liên quan trực tiếp JD, medium nếu là thông tin bổ sung  
   - **methods**: hai phương thức khả thi (Tool GitHub, Tool Ask User)  
4. Xuất kết quả dưới dạng JSON (giữ nguyên khi render, không để .format() thay thế):  

{{
  "missions": [
    {{
      "name": "...",
      "goal": "...",
      "objective": "...",
      "priority": "high/medium",
      "methods": [
        "Tool GitHub: ...",
        "Tool Ask User: ..."
      ]
    }},
    ...
  ],
  "priority_order": ["missions liên quan JD", "missions khác"]
}}

Yêu cầu:  
- Các mission phải chi tiết, bám sát yêu cầu của job_description.  
- Objective phải gắn trực tiếp với evaluation: thông tin cần thu thập phải đầy đủ và cụ thể (không chỉ liệt kê, mà cần mô tả vai trò, công nghệ, kết quả, thành tựu).  
- Luôn ưu tiên mission liên quan JD trước, sau đó mới đến mission bổ sung khác.
""" 
    job_description = """
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
    candidate_info = """
        Early-career AI/ML engineer with hands-on experience in Deep Learning, NLP, and transformer-based models. Built end-to-end systems in academic projects and hackathons, including LLM integration, semantic search, and real-time data pipelines. Strong Python skills (OOP, design patterns) and proven ability to collaborate in team projects. Eager to apply technical expertise to production systems and grow as an AI Engineer. Technical Skills • Machine Learning Frameworks: PyTorch, Tensorflow, Pandas, Scikit-learn, Matplotlib. • Big Data Tools: Apache Hadoop, Apache Spark, Apache Kafka. • Programming Languages: Python, C++. • Database: MySQL, MongoDB. • Other Tools: Git, Docker, Selenium, Jupyter.
"""
    evaluation = """
Đánh giá chi tiết:

Đánh giá mức độ đầy đủ: Thiếu

Các phần còn thiếu hoặc chưa rõ ràng:

Thông tin cá nhân (họ tên, email, số điện thoại, địa chỉ).
Kinh nghiệm làm việc (công ty, vị trí, thời gian, mô tả công việc chi tiết, thành tích cụ thể, định lượng).
Học vấn (tên trường, chuyên ngành, bằng cấp, thời gian học).
Kỹ năng mềm (ví dụ: làm việc nhóm, giải quyết vấn đề, giao tiếp).
Trình bày rõ ràng các dự án/thành tích nổi bật với kết quả cụ thể.
Chứng chỉ/Giải thưởng (nếu có).
Phần tóm tắt/mục tiêu nghề nghiệp có thể cô đọng hơn.
Gợi ý cụ thể những gì cần bổ sung để hoàn thiện CV:

Thông tin cá nhân:

Họ và tên đầy đủ:
Số điện thoại: (Định dạng quốc tế nếu cần)
Email: (Sử dụng email chuyên nghiệp)
Địa chỉ: (Có thể chỉ ghi Tỉnh/Thành phố để bảo mật)
LinkedIn profile: (Nếu có, rất quan trọng với ngành công nghệ)
Tóm tắt/Mục tiêu nghề nghiệp (Objective/Summary):

Cô đọng lại phần hiện tại, tập trung vào 2-3 điểm mạnh cốt lõi và mục tiêu rõ ràng, ví dụ: "Early-career AI/ML Engineer with hands-on experience in Deep Learning, NLP, and transformer-based models. Proven ability to build end-to-end systems for semantic search and LLM integration in academic settings. Seeking to leverage strong Python skills and collaborative spirit to contribute to impactful production systems at [Tên công ty mong muốn/Lĩnh vực]."
Hoặc chuyển thành Mục tiêu nghề nghiệp nếu bạn mới ra trường và muốn nhấn mạnh hướng đi.
Kinh nghiệm làm việc (Work Experience): Đây là phần quan trọng nhất cần bổ sung.

Cấu trúc cho mỗi mục:
Tên Công ty/Tổ chức:
Vị trí:
Thời gian làm việc: (Tháng/Năm - Tháng/Năm hoặc Hiện tại)
Mô tả công việc & Thành tích: Sử dụng gạch đầu dòng, tập trung vào hành động và kết quả (kỹ thuật STAR: Situation, Task, Action, Result).
Ví dụ cho các dự án hackathon/học thuật: Thay vì chỉ liệt kê, hãy cấu trúc như sau:
Dự án/Cuộc thi: [Tên dự án/Cuộc thi]
Vai trò: [Ví dụ: ML Engineer, Data Scientist]
Thời gian: [Tháng/Năm]
Mô tả & Thành tích:
"Developed an end-to-end LLM integration system for [mục đích, ví dụ: question answering] using [tên mô hình/framework], resulting in [thành tích định lượng, ví dụ: 20% improvement in response accuracy]."
"Built a real-time data pipeline with [công cụ, ví dụ: Apache Kafka] for [mục đích, ví dụ: data ingestion], processing [số lượng/tốc độ dữ liệu, ví dụ: 1000 messages/sec]."
"Implemented a semantic search engine using transformer-based models, achieving [thành tích định lượng, ví dụ: 90% precision] for relevant document retrieval."
"Collaborated with a team of [số người] engineers to design and deploy a [loại hệ thống] prototype within [thời gian, ví dụ: 48 hours] hackathon."
Học vấn (Education):

Tên Trường:
Chuyên ngành: (Ví dụ: Khoa học Máy tính, Trí tuệ Nhân tạo, Kỹ thuật Phần mềm)
Bằng cấp: (Ví dụ: Cử nhân, Thạc sĩ)
Thời gian học: (Năm tốt nghiệp hoặc Năm bắt đầu - Năm kết thúc)
GPA: (Nếu cao và muốn làm nổi bật)
Các khóa học liên quan/Luận văn tốt nghiệp: (Nếu liên quan trực tiếp đến vị trí ứng tuyển)
Kỹ năng (Skills):

Kỹ năng cứng: Giữ nguyên danh sách hiện tại, có thể phân loại rõ ràng hơn như bạn đã làm.
Kỹ năng mềm (Soft Skills): Bổ sung các kỹ năng như:
Làm việc nhóm (Teamwork)
Giải quyết vấn đề (Problem-solving)
Giao tiếp (Communication)
Tư duy phản biện (Critical Thinking)
Khả năng học hỏi nhanh (Fast Learner)
Quản lý thời gian (Time Management)
Dự án cá nhân/Đóng góp mã nguồn mở (Personal Projects/Open Source Contributions):

Nếu có các dự án cá nhân thú vị hoặc đã đóng góp cho các dự án mã nguồn mở, hãy trình bày chúng ở đây với cấu trúc tương tự như kinh nghiệm làm việc.
Bao gồm liên kết tới GitHub repository nếu có.
Chứng chỉ/Giải thưởng (Certifications/Awards):

Chứng chỉ: Liệt kê các chứng chỉ liên quan (ví dụ: chứng chỉ AWS Machine Learning, Google Cloud ML, Coursera Specializations...).
Giải thưởng: Liệt kê các giải thưởng học thuật, cuộc thi, hackathon mà bạn đã đạt được.
Lời khuyên thêm:

Độ dài: Với kinh nghiệm early-career, CV nên gói gọn trong 1 trang A4.
Từ khóa: Đảm bảo CV chứa các từ khóa quan trọng có trong mô tả công việc mà bạn ứng tuyển.
Trình bày: Sử dụng font chữ dễ đọc, bố cục rõ ràng, khoảng trắng hợp lý.
Kiểm tra lỗi: Đọc kỹ lại để loại bỏ lỗi chính tả và ngữ pháp.
"""
    result = test_prompt_extract_jd(
        prompt,
        candidate_info,
        evaluation,
        job_description,
        "gemini-2.5-flash-lite"
    )
    print(result)
    langfuse.flush()