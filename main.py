import os
import json
import datetime as DT

payments_path = os.path.join("data", "operations.json")

def load_payments(path):
    """Загружает всю информацию о платежах"""
    if not os.path.exists(path):
        return []
    with open(path, 'r', encoding='utf=8') as file:
        data = json.load(file)
        return data

def list_of_classes(list):
    """создаёт список экземпляров класса"""
    list_classes = []
    for payment in list:
        state = payment.get('state')
        if state == "CANCELED":
            continue
        date = payment.get('date')
        description = payment.get('description')
        from_is = payment.get('from')
        to = payment.get('to')
        amount_1 = payment.get('operationAmount')
        if amount_1 is None:
            continue
        else:
            amount = amount_1.get('amount')
            currency_1 = amount_1.get('currency')
            currency = currency_1.get('name')
        copy = Payment(state, date, description, from_is, to, amount, currency)
        list_classes.append(copy)
        list_classes.sort(key=lambda payment: payment.date, reverse=True)
    return list_classes

class Payment():
    def __init__(self, state, date, description, from_is, to, amount, currency):
        self.state = state
        self.date = date[:10]
        self.date = DT.datetime.strptime(self.date, '%Y-%m-%d')
        self.date = self.date.strftime('%Y.%m.%d')
        self.description = description
        self.from_is = from_is
        self.to = to
        self.amount = amount
        self.currency = currency

    def from_is_correct(self):
        """корректирует номер счёта или карты в указанный формат"""
        if self.from_is == None:
            return self.from_is
        else:
            list = self.from_is.split()
            if len(list[-1]) == 20:
                list[-1] = "**"+list[-1][-4:]
            if len(list[-1]) == 16:
                result = list[-1][:4] + " " + list[-1][4:6] + "** " + "****" + " " + list[-1][-4:]
                list[-1] = result
            return " ".join(list)

    def to_correct(self):
        """корректирует номер счёта или карты в указанный формат"""
        if self.to == None:
            return self.to
        else:
            list = self.to.split()
            if len(list[-1]) == 20:
                list[-1] = "**"+list[-1][-4:]
            if len(list[-1]) == 16:
                result = list[-1][:4] + " " + list[-1][4:6] + "** " + "****" + " " + list[-1][-4:]
                list[-1] = result
            return " ".join(list)

    def result(self):
        """выводит ответ"""
        return (f'{self.date} {self.description}\n'
               f'{self.from_is_correct()} -> {self.to_correct()}\n'
               f'{self.amount} {self.currency}\n')


all_payments = load_payments(payments_path)
list_classes = list_of_classes(all_payments)


for i in range(0, 5):
    print(list_classes[i].result())