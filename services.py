from model import JD, session, Skill, User
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def update(chat_id, major='', experience=0, area=''):
    try:
        user = session.query(User).filter_by(chat_id=str(chat_id)).first()
        if user:
            user.major = major if major != '' else user.major
            user.experience = experience if experience != 0 else user.experience
            user.area = area if area != '' else user.area
        else:
            user = User(
                chat_id=str(chat_id),
                major=major,
                experience=experience,
                area=area
            )
            session.add(user)
        session.commit()
        session.refresh(user)
        return user
    
    except Exception as e:
        session.rollback()
        print(f"Error occurred: {str(e)}")

    finally:
        session.close()

def insert_skill(chat_id, skill):
    try:
        new_skill = Skill(
            user = str(chat_id), 
            describe = skill
        )
        session.add(new_skill)
        session.commit()
    except Exception as e:
        print(str(e))
    
# def match_jd(chat_id, s):
#     user = session.query(User).filter_by(chat_id=str(chat_id)).first()
#     skills = session.query(Skill).filter_by(user=str(chat_id)).all()
#     jds = session.query(JD).filter(JD.experience <= user.experience).filter_by(major=user.major, area=user.area)
#     compatibilities = []
#     for jd in jds:
#         tags = [word.strip().lower().replace("_", " ") for word in jd.tags.strip().split(',')]
#         point = 0
#         for tag in tags:
#             if len(tag) == 0:
#                 continue
#             for skill in skills:
#                 point += skill.describe.lower().count(tag.lower())
#         print(point)
#         print(jd.tags)
#         print(skills)
#         compatibilities.append((point, jd))
#     compatibilities.sort(key=lambda x: x[0], reverse=True)
#     return compatibilities[:min(s, len(compatibilities))]


def match_jd(chat_id, s):
    user = session.query(User).filter_by(chat_id=str(chat_id)).first()
    skills = session.query(Skill).filter_by(user=str(chat_id)).all()
    jds = session.query(JD).filter(JD.experience <= user.experience).filter_by(major=user.major, area=user.area)
    compatibilities = []
    
    # Tạo một vectorizer TF-IDF
    vectorizer = TfidfVectorizer()

    for jd in jds:
        tags = [word.strip().lower().replace("_", " ") for word in jd.tags.strip().split(',')]
        # Tạo một danh sách các kỹ năng mà ứng viên có
        user_skills = [skill.describe.lower() for skill in skills]
        jd_skills = [skill.strip().lower() for skill in jd.skill.split(',')]

        # Tạo một ma trận TF-IDF từ tags và user_skills
        tfidf_matrix_skills = vectorizer.fit_transform(user_skills + jd_skills)

        # Tính toán độ tương tự cosine giữa tags và user_skills
        cosine_sim_skills = cosine_similarity(tfidf_matrix_skills[:len(user_skills)], tfidf_matrix_skills[len(user_skills):])

        # Tính điểm bằng cách lấy trung bình của các giá trị cosine similarity
        point = cosine_sim_skills.mean()
        
        for tag in tags:
            if len(tag) == 0:
                continue
            for skill in skills:
                point += skill.describe.lower().count(tag.lower()) * 10
        

        compatibilities.append((point, jd))

    compatibilities.sort(key=lambda x: x[0], reverse=True)
    for x in compatibilities:
        print(x[0], x[1].tags)
    return compatibilities[:min(s, len(compatibilities))]
        
        
                
    

    