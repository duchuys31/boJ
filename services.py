from model import JD, session, Skill, User


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
    
def match_jd(chat_id, s):
    user = session.query(User).filter_by(chat_id=str(chat_id)).first()
    skills = session.query(Skill).filter_by(user=str(chat_id)).all()
    jds = session.query(JD).filter(JD.experience <= user.experience).filter_by(major=user.major, area=user.area)
    compatibilities = []
    for jd in jds:
        tags = [word.strip().lower().replace("_", " ") for word in jd.tags.split(',')]
        point = 0
        for tag in tags:
            if len(tag) == 0:
                continue
            for skill in skills:
                point += skill.describe.lower().count(tag.lower())
        compatibilities.append((point, jd))
    compatibilities.sort(key=lambda x: x[0], reverse=True)
    return compatibilities[:min(s, len(compatibilities))]
    
        
        
                
    

    