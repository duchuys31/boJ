from model import session, User


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

    