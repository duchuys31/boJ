from model import JD, session
from openai import OpenAI
import json
client = OpenAI()




JDs = session.query(JD).all()

for i in range(len(JDs)):
    print(f"JD {i}")
    JD = JDs[i]
    if JD.name == "":
        continue
    promt = f"""
Tôi có đoạn thông tin về  1 Job Description sau:
##########################################
{JD.skill}
##########################################
Yêu cầu về câu trả lời đưa ra:
- Đưa ra 1 danh sách các kĩ năng mà ứng viên cần có để apply công việc.
- Các kĩ năng đưa ra phải ngắn gọn nhất có thể và tối ưu nhất có thể về mặt số lượng từ
- Mỗi kĩ năng đưa ra có độ dài không quá 2
- Mỗi từ khóa đều đại diện cho 1 kĩ năng chuyên ngành nhất định liên quan tới ngành {JD.major}
- Không đưa ra các từ khóa có kĩ năng không rõ rang quá chung chung cho các ngành nghề
- Tất cả các kĩ năng tim được đều ở chung trong  [] 
- Mỗi từ khóa cách nhau bằng dấu phẩy, ngoài ra không có thêm kí tự đặc biệt nào khác
Các chú ý quan trọng: 
- Trong câu trả lời đưa ra chỉ có cặp [] duy nhất 
    """
    print(promt)
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": promt}
                ]
            )
            print(response.choices[0].message.content)
            data = response.choices[0].message.content
            tags = set()
            start_index = data.find('[')
            end_index = data.find(']')
            if start_index == -1 or end_index == -1 or end_index < start_index:
                continue
            text = data[start_index + 1:end_index]
            words = [word.strip().lower().replace("_", " ") for word in text.split(',')]
            for word in words:
                tags.add(word)
            JD.tags = ""
            for word in tags:
                JD.tags += f"{word}, "
            print("##################################")
            print("Skills:\n", JD.tags)
            print("##################################")
            print(JD.tags)
            session.add(JD)
            session.commit()
            break
        except Exception as e:
            print(str(e))
    
    