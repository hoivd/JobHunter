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

    delete_db = False
    gm = GeminiLLM()
    pm = PromptManager()
    with Neo4jDriver() as neo_driver:
        if delete_db:
            Neo4jCleaner.delete_all(neo_driver)
        

        app = JDExtractor(gm, pm, neo_driver, debug=True)

        jd_text1 = f"""AI Architect (Python, Microservices, Docker)
        ABBANK
        Sign in to view salary

        36 Hoàng Cầu, Dong Da, Ha Noi  At office 11 days ago
        Skills:
        Job Expertise:
        Job Domain:
        Top 3 reasons to join us
        Lương/ thưởng hấp dẫn
        Cơ hội thăng tiến nghề nghiệp cao
        Môi trường làm việc thân thiện, năng động
        Job description
        1. Trách nhiệm trong Xây dựng và quản lý thiết kế nền tảng AI:
        Thiết kế và xây dựng nền tảng AI nhằm phát triển các ứng dụng AI với các agentic AI và tinh chỉnh các mô hình sử dụng LLM, VLM.
        Dẫn dắt nhóm phát triển AI thực hiện dự án bằng cách cung cấp hướng dẫn kỹ thuật trong suốt vòng đời phát triển phần mềm.
        Xác định chiến lược AI và hợp tác chặt chẽ với các bên liên quan trong doanh nghiệp để đảm bảo các giải pháp AI phù hợp với mục tiêu của tổ chức.
        Thiết kế và tối ưu hóa các mô hình AI để đảm bảo khả năng mở rộng, hiệu suất và hiệu quả.
        Cung cấp sự lãnh đạo và cố vấn kỹ thuật cho các kỹ sư AI, thúc đẩy văn hóa đổi mới và cải tiến liên tục.
        Tiến hành nghiên cứu và phát triển chuyên sâu để khám phá các công nghệ và phương pháp luận AI mới.
        Giám sát việc tích hợp các giải pháp AI với các hệ thống và quy trình kinh doanh hiện có, đảm bảo việc triển khai và vận hành suôn sẻ.
        Phối hợp với ban lãnh đạo để xác định tầm nhìn và lộ trình AI cho tổ chức
        2. Thúc đẩy và lan tỏa việc sử dụng AI tới ABBankers và đội ngũ công nghệ:
        Định kỳ tổ chức các buổi truyền thông về AI và cách sử dụng các ứng dụng AI trên thị trường, và các ứng dụng AI do ABBANK phát triển để giúp người dùng nâng cao nhận thức về AI, nâng cao năng suất, hiệu quả trong công việc.
        Thu thập các usecase từ người dùng nghiệp vụ ABBANK để đưa vào danh sách phát triển.
        Thường xuyên tổ chức hoặc dẫn dắt tổ chức các buổi giới thiệu về sản phẩm AI, công nghệ AI, đề xuất ứng dụng AI, ... tới đội ngũ công nghệ nhằm lan tỏa và thúc đẩy việc ứng dụng AI và tích hợp AI vào các giải pháp công nghệ
        3. Xây dựng kế hoạch ngân sách và quản lý ngân sách bộ phận:
        Phối Lập ngân sách cho hoạt động của Đơn vị một cách chính xác và hiệu quả.
        Your skills and experience
        Bằng cấp: Tốt nghiệp Đại học trở lên các chuyên ngành Công nghệ thông tin/ Điện tử viễn thông/ Toán tin.
        Kinh nghiệm:
        Có từ 5 năm kinh nghiệm trở lên trong lĩnh vực AI; đã tham gia trực tiếp xây dựng và dẫn dắt xây dựng các ứng dụng AI
        Kỹ năng kỹ thuật:
        Thành thạo ngôn ngữ Python
        Có kinh nghiệm toàn diện với LangChain API, LLamaIndex và các công nghệ cơ sở dữ liệu (MongoDB, PostgreSQL, ChromaDB, VespaDB, v.v.).
        Có kinh nghiệm sâu rộng với microservices, Docker và tối ưu hóa, mở rộng microservices.
        Why you'll love working here
        Lương và phúc lợi hấp dẫn:
        Mức lương cạnh tranh, phản ánh trực tiếp kỹ năng và kinh nghiệm của ứng viên (chi tiết sẽ được thảo luận trong buổi phỏng vấn)
        13 ngày nghỉ phép linh hoạt, bao gồm ngày sinh nhật và các dịp quan trọng khác
        Bảo hiểm đầy đủ theo luật lao động, cùng với ABBANK CARE - chương trình phúc lợi bổ sung đặc biệt dành cho ABBankers
        Lãi suất vay ưu đãi - Quyền lợi đặc biệt dành cho nhân viên ABBANK
        Cơ hội phát triển nghề nghiệp hấp dẫn:
        Gia nhập các dự án chuyển đổi quy mô lớn, cộng tác cùng các chuyên gia hàng đầu để áp dụng công nghệ mới nhất trong ngành ngân hàng
        Lộ trình phát triển sự nghiệp rõ ràng, được tạo điều kiện cho cả sự phát triển kỹ thuật và quản lý
        Hỗ trợ đào tạo và chứng chỉ trong lĩnh vực IT, ngân hàng/tài chính
        Môi trường làm việc năng động:
        Mô hình làm việc linh hoạt, trẻ trung, khuyến khích đổi mới và sáng tạo
        Văn phòng được trang bị hiện đại, kèm theo các thiết bị tiên tiến nhất dành cho nhân viên
        Tổ chức thường xuyên các hoạt động ngoại khóa (team building, hội thảo, và các sự kiện văn nghệ), tạo điều kiện cho nhân viên gắn kết và phát triển

        ABBANK
        Cung ứng các sản phẩm - dịch vụ tài chính ngân hàng trọn gói
        Company typeCompany industryCompany size
        Non-IT
        Banking
        1000+
        CountryWorking daysOvertime policy
        VietnamMonday - FridayNo OT
        """

        jd_text2 = f"""At Jabil we strive to make ANYTHING POSSIBLE and EVERYTHING BETTER. We are proud to be a trusted partner for the world's top brands, offering comprehensive engineering, manufacturing, and supply chain solutions. With over 50 years of experience across industries and a vast network of over 100 sites worldwide, Jabil combines global reach with local expertise to deliver both scalable and customized solutions. Our commitment extends beyond business success as we strive to build sustainable processes that minimize environmental impact and foster vibrant and diverse communities around the globe.
SUMMARY
Under limited supervision designs, develops and maintains test procedures, tester hardware and software for electronic circuit board production.

ESSENTIAL DUTIES AND RESPONSIBILITIES include the following. Other duties may be assigned.

Review circuit board designs for testability requirements.
Support manufacturing with failure analysis, tester debugging, reduction of intermittent failures and downtime of test equipment.
Prepare recommendations for testing and documentation of procedures to be used from the product design phase through to initial production.
Generate reports and analysis of test data, prepares documentation and recommendations.
Review test equipment designs, data and RMA issues with customers regularly.
Design, and direct engineering and technical personnel in fabrication of testing and test control apparatus and equipment.
Direct and coordinate engineering activities concerned with development, procurement, installation, and calibration of instruments, equipment, and control devices required to test, record, and reduce test data.
Determine conditions under which tests are to be conducted and sequences and phases of test operations.
Direct and exercise control over operational, functional, and performance phases of tests.
Perform moderately complex assignments of the engineering test function for standard and/or custom devices.
Analyze and interpret test data and prepares technical reports for use by test engineering and management personnel.
Develop or use computer software and hardware to conduct tests on machinery and equipment.
Perform semi-routine technique development and maintenance, subject to established Jabil standards, including ISO and QS development standards.
May provide training in new procedures to production testing staff.
Adhere to all safety and health rules and regulations associated with this position and as directed by supervisor.
Comply and follow all procedures within the company security policy.

MINIMUM REQUIREMENTS
Bachelors of Science in Electronics or Electrical Engineering from four-year college or university preferred; or related experience and/or training; or equivalent combination of education and experience.

LANGUAGE SKILLS
Ability to read, analyze, and interpret general business periodicals, professional journals, technical procedures, or governmental regulations. Ability to write reports, business correspondence, and procedure manuals. Ability to effectively present information and respond to questions from groups of managers, clients, customers, and the general public.

MATHEMATICAL SKILLS
Ability to work with mathematical concepts such as probability and statistical inference, and fundamentals of plane and solid geometry and trigonometry. Ability to apply concepts such as fractions, percentages, ratios, and proportions to practical situations.

REASONING ABILITY
Ability to define problems, collect data, establish facts, and draw valid conclusions. Ability to interpret an extensive variety of technical instructions in mathematical or diagram form and deal with several abstract and concrete variables.

PHYSICAL DEMANDS
The physical demands described here are representative of those that must be met by an employee to successfully perform the essential functions of this job. The employee is frequently required to walk, and to lift and carry PC’s and test equipment weighing up to 50 lbs. Specific vision abilities required by this job include close vision and use of computer monitor screens a great deal of time.




WORK ENVIRONMENT
The work environment characteristics described here are representative of those an employee encounters while performing the essential functions of this job. Individual’s primary workstation is located in the office area, with some time spent each day on the manufacturing floor. The noise level in this environment ranges from low to moderate.
BE AWARE OF FRAUD: When applying for a job at Jabil you will be contacted via correspondence through our official job portal with a jabil.com e-mail address; direct phone call from a member of the Jabil team; or direct e-mail with a jabil.com e-mail address. Jabil does not request payments for interviews or at any other point during the hiring process. Jabil will not ask for your personal identifying information such as a social security number, birth certificate, financial institution, driver’s license number or passport information over the phone or via e-mail. If you believe you are a victim of identity theft, contact your local police department. Any scam job listings should be reported to whatever website it was posted in.
Jabil, including its subsidiaries, is an equal opportunity employer and considers qualified applicants for employment without regard to race, color, religion, national origin, sex, sexual orientation, gender identity, age, disability, genetic information, veteran status, or any other characteristic protected by law.

Accessibility Accommodation
If you are a qualified individual with a disability, you have the right to request a reasonable accommodation if you are unable or limited in your ability to use or access Jabil.com/Careers site as a result of your disability. You can request a reasonable accommodation by sending an e-mail to Always_Accessible@Jabil.com with the nature of your request and contact information. Please do not direct any other general employment related questions to this e-mail. Please note that only those inquiries concerning a request for reasonable accommodation will be responded to.
#whereyoubelong
        """
        app.extract_text(jd_text1)