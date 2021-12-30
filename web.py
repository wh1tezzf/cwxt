'''Provide functions for CWXT web version'''

def sumMoney(doctors, money, doctor_dict):
    for i in range(0,len(money)):
        doctor_name = doctors[i]
        amount = money[i]
        if amount > 0.0:
            if doctor_name in doctor_dict:
                doctor_dict[doctor_name] = doctor_dict[doctor_name] + amount
            else:
                doctor_dict.update({doctor_name: amount})
    return doctor_dict


def sumAmount(doctors, totals, commission, doctor_dict):
    total = 0
    for i in range(0,len(totals)):

        if totals[i] > 0.0:
            total += totals[i]
    total = total*commission
    doctor_dict['投资方分配金额'] += total
    return doctor_dict
