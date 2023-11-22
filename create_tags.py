from model import JD, session
from openai import OpenAI
import json
client = OpenAI()




JDs = session.query(JD).all()

for i in range(len(JDs)):
    print(f"JD {i}")
    JD = JDs[i]
    if JD.name == "" or len(JD.tags) > 0:
        continue
    promt = f"""
Tôi có đoạn thông tin về  1 Job Description sau:
[{JD.skill}]
Yêu cầu:
- Đưa ra 1 danh sách có nhiều từ khóa nhất có thể  bằng tiếng Việt trong đoạn thông tin trên.
- Yêu cầu các từ đưa ra là tiếng việt phải ngắn gọn nhất có thể và tối ưu nhất có thể về mặt độ dài, mỗi từ khóa có độ dài không quá 2
- Mỗi từ khóa đều đại diện cho 1 kĩ năng nhất định liên quan tới công việc và yêu cầu về kĩ năng đó nếu có
- Đưa ra hai phiên bản 1 phiên bản bao gồm các từ là tiếng việt và 1 phiên bản bao gồm các từ  là tiếng anh. 
- Với mỗi phiên bản, tất cả các từ khóa của phiên bản đều ở trong  [] 
- Mỗi từ khóa cách nhau bằng dấu phẩy, ngoài ra không có thêm kí tự đặc biệt nào khác
- Chỉ đưa ra 2 phiên bản theo yêu cầu và không đưa ra thêm bất kì một chữ cái nào khác
Chú ý: Trong câu trả lời đưa ra chỉ có 2 cặp [] duy nhất và không sử dụng bất kì kí tự đặc biệt nào
    """
    print(promt)
    while True:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
                    {"role": "user", "content": promt}
                ]
            )
            print(response.choices[0].message.content)
            datas = json.loads(response.choices[0].message.content)
            tags = set()
            for data in datas.values():
                print(data)
                start_index = data.find('[')
                end_index = data.find(']')
                text = data[start_index + 1:end_index]
                words = [word.strip().lower().replace("_", " ") for word in text.split(',')]
                for word in words:
                    tags.add(word)
            JD.tags = ""
            for word in tags:
                JD.tags += f"{word}, "
            print(JD.tags)
            session.add(JD)
            session.commit()
            break
        except Exception as e:
            print(str(e))
    
    