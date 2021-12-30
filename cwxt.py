
import pandas as pd
import sys

excel_name = sys.argv[1]
df = pd.read_excel(excel_name, sheet_name=None)

# lets grab the last two columns of 治疗检查
sumExam = pd.DataFrame(df['治疗检查'], columns=['接诊医生','治疗检查费分配金额', '实际金额'])

#print(sumExam['治疗检查费分配金额'])

#dictionary to store all amounts of doctors
doctor_dict = {'投资方分配金额': 0}

# sum up doctors' amounts
def addUpMoney(doctors, money):
    for i in range(0,len(money)):
        doctor_name = doctors[i]
        amount = money[i]
        if type(doctor_name) != type(float): #the empty cells are of type float
        #print(sumExam['治疗检查费分配金额'][i])
            if doctor_name in doctor_dict:
                doctor_dict[doctor_name] = doctor_dict[doctor_name] + amount
            else:
                doctor_dict.update({doctor_name: amount})

        # return doctor_dict

# sums up the actual amount
def addUpAmount(doctors, totals, commission):
    for i in range(0,len(doctors)):
        doctor_name = doctors[i]
        amount = totals[i]*commission
        if type(doctor_name) != type(float):
            doctor_dict['投资方分配金额'] += amount

#type of 检查费 is float
#lets use a dictionary to store doctor's salary
addUpMoney(sumExam['接诊医生'], sumExam['治疗检查费分配金额'])
addUpAmount(sumExam['接诊医生'], sumExam['实际金额'], 0.5)

# lets move onto 挂号费
sumRegister = pd.DataFrame(df['挂号费'], columns= ['接诊医生','挂号费分配金额', '挂号费用'])

#print(sumRegister)

#lets use a dictionary to store doctor's salary
addUpMoney(sumRegister['接诊医生'], sumRegister['挂号费分配金额'])
addUpAmount(sumRegister['接诊医生'], sumRegister['挂号费用'], 0.2)
#lets move onto 配镜
sumGlasses = pd.DataFrame(df['配镜'], columns= ['接诊医生','分配金额1','验光师','分配金额2','来源1','分配金额3','来源2','分配金额4', '实际金额'])

#lets add up the amounts for each doctor
addUpMoney(sumGlasses['接诊医生'], sumGlasses['分配金额1'])
addUpMoney(sumGlasses['验光师'], sumGlasses['分配金额2'])
addUpMoney(sumGlasses['来源1'], sumGlasses['分配金额3'])
addUpMoney(sumGlasses['来源2'], sumGlasses['分配金额4'])
addUpAmount(sumGlasses['接诊医生'], sumGlasses['实际金额'], 0.2)
#iterate through dictionary and change the precision of float to two decimal digits
for key in doctor_dict:
    doctor_dict[key] = float("{0:.2f}".format(doctor_dict[key]))

print(doctor_dict)