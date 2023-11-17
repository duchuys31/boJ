import openpyxl
import random
from model import Area, JD, Major, session


wb = openpyxl.load_workbook('data.xlsx')

sheet = wb.active

data = []

majors = set()
majors.add('')
areas = ['Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng', '']

for row in sheet.iter_rows(values_only=True):
    data.append(list(row))
    
for i in range(1, len(data)):
    majors.add(data[i][0])
    
for area in areas:
    new_area = Area(name=area)
    session.add(new_area)
    session.commit()
for major in majors:
    new_major = Major(name=major)
    session.add(new_major)
    session.commit()

for i in range(1, len(data)):
    row = data[i]
    new_jd = JD(
        name=row[1],
        major=row[0],
        experience=row[2],
        area=row[3],
        address=row[4],
        salary=row[5],
        company=row[6],
        describe=row[7],
        benefit=row[8],
        skill=row[9],
        contact=row[10],
        tags=''
    )
    session.add(new_jd)
    session.commit()




