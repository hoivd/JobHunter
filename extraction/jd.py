import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from extractor import Extractor
from logger import _setup_logger
from utils import Utils
import re 
import json
from typing import Optional


# Lấy config & logger
config = Utils.get_config()
logger = _setup_logger(__name__, level=config["logging"]["level"])


class JDExtractor(Extractor):
    def __init__(self, gemini_manager, prompt_manager, neo4j_driver, debug = False, data_dir = "debug"):
        
        super().__init__(gemini_manager, prompt_manager, neo4j_driver)

    def PDF2Json(self, pdf_path):
        pass

    def Text2Json(self, jd_text: str) -> Optional[dict]:
        """
        Truyền JD vào, query prompt và gửi sang Gemini để lấy JSON kết quả.
        Nếu debug=True thì sẽ lưu JSON vào thư mục data.
        """

        def extract_json(text: str) -> Optional[str]:
            pattern = r"```json\s*(\{.*?\})\s*```"
            match = re.search(pattern, text, re.DOTALL)
            return match.group(1) if match else None

        try:
            # Render prompt từ file jd_extraction.txt
            prompt = self.prompt_manager.render("jd_extraction", jd=jd_text)
            logger.info("🚀 Đã render prompt cho JD Extraction")

            # Gửi prompt sang Gemini
            reps = self.gemini_manager.generate(prompt)

            # Trích xuất JSON string
            json_str = extract_json(reps)
            if not json_str:
                logger.error("❌ Không tìm thấy JSON trong phản hồi Gemini")
                return None

            # Convert sang dict
            json_obj = json.loads(json_str)

            # Nếu bật debug thì lưu lại
            if self.debug:
                file_path = Utils.save_json(json_obj, "jd_extraction", dir_path=self.data_dir + '/jsons', timestamp=True)
                logger.info(f"💾 Đã lưu JSON debug vào {file_path}")

            logger.info("✅ JD Extraction thành công (JD2Json)")
            return json_obj

        except Exception as e:
            logger.error(f"❌ Lỗi khi JD Extraction (JD2Json): {e}")
            raise

if __name__ == "__main__":
    from gemini_llm import GeminiLLM
    from prompt_manager import PromptManager
    from cypher.cleaner import Neo4jCleaner
    from cypher.cypher_manager import Neo4jDriver

    delete_db = True
    gm = GeminiLLM()
    pm = PromptManager()
    with Neo4jDriver() as neo_driver:
        if delete_db:
            Neo4jCleaner.delete_all(neo_driver)
        

        app = JDExtractor(gm, pm, neo_driver, debug=True)

        jd_text1 = f"""VIC - AI Engineer (Machine Learning/ Deep Learning)
    Viettel Group
    You'll love it
    Tầng 5, Trụ sở chính của Tập đoàn Viettel, Lô D26, Khu đô thị mới Cầu Giấy, phường Yên Hòa, Cau Giay, Ha Noi
    At office
    1 day ago
    Skills:
    Job Expertise:
    Job Domain:
    Top 3 reasons to join us
    Dẫn đầu thị trường
    Cơ hội thử thách và phát triển bản thân
    Môi trường làm việc năng động
    Job description
    Tham gia thiết kế, xây dựng và phát triển các nền tảng dùng chung phục vụ xử lý dữ liệu, huấn luyện, tối ưu, triển khai, vận hành và giám sát các mô hình Machine Learning (ML), Deep Learning (DL), Large Language Models (LLM) với khả năng chịu tải và dự phòng.
    Phát triển và triển khai các ứng dụng chatbot dựa trên LLM, hỗ trợ truy vấn dữ liệu, tương tác với hệ thống nội bộ, tích hợp với các agent khác; nghiên cứu, thiết kế và xây dựng kiến trúc multi-agent đảm bảo hiệu quả và khả năng mở rộng.
    Thiết kế, phát triển, kiểm thử và tối ưu các công cụ (tools) hỗ trợ LLM, đảm bảo tính chính xác, độ tin cậy, khả năng hoạt động ổn định trong môi trường thực tế.
    Xây dựng, quản lý và vận hành các agent (low-code hoặc full-code), hỗ trợ tích hợp vào hệ sinh thái ứng dụng hiện có; giám sát và tối ưu hiệu suất hoạt động của agent.
    Tham gia công tác quản trị hệ thống, bao gồm cài đặt, cấu hình, tối ưu hạ tầng triển khai ML/DL/AI; đảm bảo an toàn, bảo mật, khả năng mở rộng và duy trì tính sẵn sàng cao.
    Tìm hiểu nghiệp vụ, khảo sát, so sánh, đánh giá và báo cáo các giải pháp, công nghệ ML/DL/AI phù hợp nhằm đáp ứng yêu cầu. Từ đó xây dựng tài liệu thiết kế tổng thể, thiết kế chi tiết, thiết kế cơ sở dữ liệu; triển khai hệ thống và quản lý source code cho các ứng dụng phần mềm liên quan.
    Your skills and experience
    Tốt nghiệp Đại học loại khá trở lên chuyên ngành CNTT hoặc các ngành liên quan.
    TOIEC >=550 hoặc tương đương.
    Có kinh nghiệm phát triển ứng dụng ML/DL/AI, triển khai và vận hành dịch vụ trên môi trường thực tế.
    Từ 2 năm kinh nghiệm trở lên
    Kiến thức về lập trình, cấu trúc dữ liệu & giải thuật;
    Kỹ năng sử dụng ngôn ngữ lập trình Python, Java;
    Kiến thức về các loại CSDL (SQL/NoSQL);
    Kiến thức về Machine Learning, Deep Learning, Generative AI.
    Có hiểu biết về quản trị hệ thống, hạ tầng triển khai AI (Docker, Kubernetes, Cloud AI services) là một lợi thế.
    Sử dụng thành thạo một trong các thư viện học máy: Scikit-learn, TensorFlow, Keras, PyTorch, LangChain, HuggingFace;
    Why you'll love working here
    Thu nhập hấp dẫn, thỏa thuận theo năng lực và kinh nghiệm.
    Đầy đủ các khoản thưởng: Thưởng lễ Tết, quà tặng, du lịch nghỉ mát, hỗ trợ ăn trưa, cước điện thoại…
    Nghỉ phép linh hoạt: 12 ngày phép + 3 ngày nghỉ mát + 1 ngày sáng tạo mỗi năm.
    Bảo hiểm toàn diện: Hưởng đầy đủ BHXH, BHYT, BHTN theo quy định, cộng thêm gói bảo hiểm riêng từ Viettel. Chế độ chăm sóc y tế đặc biệt cho CBNV và người thân với trang thiết bị hiện đại.
    Môi trường làm việc cởi mở và năng động, khuyến khích trao đổi ý tưởng ở mọi cấp, cho phép bạn làm việc, sáng tạo theo cách riêng.
    Được khơi gợi cảm hứng làm việc với văn phòng xanh, không gian mở, hiện đại tiêu chuẩn quốc tế.
    Được thư giãn, khơi nguồn sáng tạo với Happy Time mỗi ngày.
    Thưởng thức bữa trưa thơm ngon tại Tập đoàn, được chọn lọc bởi các chuyên gia dinh dưỡng.
    Cơ hội tham gia gắn kết với tập thể, tổ chức với các hoạt động team building
    Viettel Group
    3.6
    SHOW US YOUR WAY


    Company type
    Company industry
    Company size
    IT Product
    Telecommunication
    1000+
    Country
    Working days
    Vietnam
    Monday - Friday
        """

        jd_text2 = f"""Data Scientist - eKYC
    Trusting Social
    2,000 - 3,000 USD
    Havana Tower - 132 Ham Nghi, District 1, Ho Chi Minh 
    At office
    20 hours ago
    Skills:
    Job Expertise:
    Job Domain:
    Top 3 reasons to join us
    Top Salary, Awesome Benefits
    Premium healthcare for 3 members in family
    Grab to work, Lunch allowance for all employee
    Job description
    Trusting Social is an AI Fintech pioneer that's revolutionizing credit access in emerging markets. Our mission is "Advancing AI to Meet the Financial Needs of Everyday Consumers with Empathy." We've assessed over 1 billion consumers across four countries, and we're on a mission to provide 100 million credit lines using the power of AI and Big Data.

    How You'll Make an Impact
    As a Data Scientist, eKYC at Trusting Social, you will be instrumental in building cutting-edge digital identity verification products for our eKYC (electronic Know Your Customer) projects. Your expertise in machine learning and computer vision will be crucial for developing robust systems to prevent fraud and money laundering. This role offers the opportunity to make a significant impact on revenue while also enhancing financial security, aligning with our strong social mission.

    What You'll Do
    Develop Advanced ML Models: Build various machine learning models in computer vision, implementing novel solutions for diverse ML problems (supervised, semi-supervised, unsupervised, one-class).
    Research & Implement Cutting-Edge Algorithms: Research, design, and implement advanced ML models and algorithms to solve practical problems, optimizing for both performance and speed.
    Build Practical Vision Systems: Work with high-dimensional image and video data to develop practical vision systems with a direct impact on revenue and profitability.
    Optimize for Deployment: Optimize and deploy "tiny" ML solutions for limited computation power devices like mobile and web platforms.
    Your skills and experience
    We need a qualified, proactive, and technically skilled Computer Vision Data Scientist:

    Educational Background: BS/MS/PhD. in Computer Science, Statistics, Mathematics, or a related field.
    Experience: 4+ years of experience in advanced Machine Learning, with a strong preference for experience in Computer Vision and Image Processing.
    Technical Proficiency: Must be proficient in Python and have experience with ML frameworks like TensorFlow, PyTorch, and ONNX.
    Problem-Solving & Insights: You're exceptional at asking the right questions that lead to actionable business insights, and you possess an aptitude for critically evaluating data outcomes, uncovering key insights, and challenging assumptions.
    Tooling Familiarity: Experience with managing data science and computer vision toolkits such as JupyterHub, CVAT, and OpenCV is a plus.
    Fundamental Understanding: A solid understanding of machine learning techniques and algorithms.
    Communication Skills: Ability to communicate complex quantitative analysis in a clear, precise, and actionable manner, coupled with great overall communication skills.
    Tech Adaptability: A keen interest and proven ability to leverage new technologies to enhance work quality and productivity.
    Why you'll love working here
    Competitive compensation package, including 13th-month salary and performance bonuses
    Comprehensive health care coverage for you and your dependents
    Generous leave policies, including annual leave, sick leave, and flexible work hours
    Convenient central district 1 office location, next to a future metro station
    Onsite lunch with multiple options, including vegetarian
    Grab for work allowance and fully equipped workstations
    Fun and engaging team building activities, sponsored sports clubs, and happy hour every Thursday
    Unlimited free coffee, tea, snacks, and fruit to keep you energized
    An opportunity to make a social impact by helping to democratize credit access in emerging markets.
    Trusting Social
    4.2
    Making Financial Inclusion a Reality using Machine Learning and AI

    Company type
    Company industry
    Company size
    IT Service and IT Consulting
    Financial Services
    301-500
    Country
    Working days
    Singapore
    Monday - Friday

        """

        jd_text3 = f"""    AI Engineer (Python,GenAI) - Up to 50M
    NTT DATA VDS
    800 - 1,900 USD
    98 Nguy Nhu Kon Tum, Thanh Xuan, Ha Noi
    At office
    19 hours ago
    Skills:
    Job Expertise:
    Job Domain:
    Top 3 reasons to join us
    Bonus Bao Viet insurance
    OT compensation: up to 400%
    Free account Udemy
    Job description
    1. Technical development activities:


    + Technical analysis of business requirements to implement the application/system


    + Draft and update use cases, user stories when required


    + Setup development/integration environments (Infrastructure, CI/CD Pipeline, Monitoring),  implementation of CI/CD pipelines to automate the software delivery process and integrate tests into the CI/CD pipeline to ensure software quality


    + Design, build, review reliable BE and FE code for Generative AI application which will be deployed in Cloud based or on Premises.


    + Design, build, review reliable Data processing workflow code which will be deployed in Cloud based or on Premises.


    + Prepare unit test cases, E2E automation test and plans.


    + Analysis and resolution of incidents, provision of new (bug fix) releases for delivery and rollout of the software


    + Follow guidelines from Control, Quality and Procedures Section: JIRA workflow, DevOps and build strategies, software development standards and best practices, security instructions,…

        """
        app.extract_text(jd_text1)
        app.extract_text(jd_text2)
        app.extract_text(jd_text3)