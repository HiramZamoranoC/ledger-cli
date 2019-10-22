import re
import fire

datePattern = re.compile(r"\d{4}/\d{1,2}/\d{1,2}")
currency = '$'

transactions = []


class Transaction:
    def __init__(self, date=None, payee=None, account=None, value=None):
        self.date = date
        self.payee = payee
        self.account = account
        self.value = value


def balance():
    with open('index.ledger') as file:
        for lineIndex in file.readlines():
            if lineIndex.startswith(";"):
                continue
            if lineIndex.startswith("!include"):
                with open(lineIndex.split()[1]) as file2:
                    for lineFile in file2.readlines():
                        if datePattern.match(lineFile):
                            date = (lineFile.split()[0])
                            payee = (lineFile.strip(date))  # payee
                        if currency in lineFile:
                            account = (lineFile.split()[0])  # account
                            if (lineFile.split()[1]).startswith('$'):
                                value = (lineFile.split()[1]).strip('$')
                            elif (lineFile.split()[1]).startswith('-'):
                                value = (lineFile.split()[1]).replace('-$', '-')
                            transactions.append(Transaction(date, payee, account, value))
    sum = 0.0
    print ('------------------------------------')
    print ('   VALUE             ACCOUNT')
    print ('------------------------------------')
    for x in range(0, len(transactions)):
        print '{:^10}{:^30}'.format(transactions[x].value, transactions[x].account)
        total = float(transactions[x].value)
        sum += total
    print(' --------')
    print '{:^10}'.format(sum)


def printable():
    with open('index.ledger') as file:
        for line in file.readlines():
            if line.startswith(";"):
                continue
            if line.startswith("!include"):
                with open(line.split()[1]) as f:
                    for li in f.readlines():
                        print(li)


def register():
    with open('index.ledger') as file:
        for lineIndex in file.readlines():
            if lineIndex.startswith(";"):
                continue
            if lineIndex.startswith("!include"):
                with open(lineIndex.split()[1]) as file2:
                    for lineFile in file2.readlines():
                        if datePattern.match(lineFile):
                            date = (lineFile.split()[0])
                            payee = (lineFile.strip(date))  # payee
                        if currency in lineFile:
                            account = (lineFile.split()[0])  # account
                            if (lineFile.split()[1]).startswith('$'):
                                value = (lineFile.split()[1]).strip('$')
                            elif (lineFile.split()[1]).startswith('-'):
                                value = (lineFile.split()[1]).replace('-$', '-')
                            transactions.append(Transaction(date, payee, account, value))
    sum = 0.0
    print ('--------------------------------------------------------------------------------------')
    print(' DATE              PAYEE                      ACCOUNT              VALUE         TOTAL')
    print ('--------------------------------------------------------------------------------------')
    for x in range(0, len(transactions)):
        total = float(transactions[x].value)
        sum += total
        print '{:^10}     {:25.17}{:^20}{:^20}{:^10}'.format(transactions[x].date, transactions[x].payee, transactions[x].account ,transactions[x].value, sum)










if __name__ == '__main__':
    fire.Fire({
        'balance': balance,
        'print': printable,
        'register': register,

    })
