import re
import fire
from colorama import init
from termcolor import colored

init()
datePattern = re.compile(r"\d{4}/\d{1,2}/\d{1,2}")
currency = '$'
index = 'index.ledger'

transactions = []


class Transaction:
    def __init__(self, date=None, payee=None, account=None, value=None):
        self.date = date
        self.payee = payee
        self.account = account
        self.value = value


def balance():
    with open(index) as fileIndex:
        for lineIndex in fileIndex.readlines():
            if lineIndex.startswith("!include"):
                pathFiles = lineIndex.split()[1]
                with open(pathFiles) as fileTransactions:
                    for lineFile in fileTransactions.readlines():
                        if datePattern.match(lineFile):
                            date = (lineFile.split()[0])
                            payee = (lineFile.strip(date))  # payee
                        if currency in lineFile:
                            account = (lineFile.split()[0])  # account
                            if (lineFile.split()[1]).startswith(currency):
                                value = (lineFile.split()[1]).strip(currency)
                            elif (lineFile.split()[1]).startswith('-'):
                                value = (lineFile.split()[1]).replace('-$', '-')
                            transactions.append(Transaction(date, payee, account, value))
    sum = 0.0
    print colored('------------------------------------','red')
    print colored('   VALUE             ACCOUNT','blue')
    print colored('------------------------------------','red')
    for x in range(0, len(transactions)):
        print '{:^10}{:^30}'.format(transactions[x].value, transactions[x].account)
        total = float(transactions[x].value)
        sum += total
    print colored(' --------','green')
    print colored('{:^10}'.format(sum),'white',)
    print colored(' --------', 'green')


def printable():
    with open(index) as fileIndex:
        for lineIndex in fileIndex.readlines():
            if lineIndex.startswith("!include"):
                filePath = lineIndex.split()[1]
                with open(filePath) as fileTransaction:
                    for lineFile in fileTransaction.readlines():
                        print(lineFile)


def register():
    with open(index) as fileIndex:
        for lineIndex in fileIndex.readlines():
            if lineIndex.startswith("!include"):
                filePath = lineIndex.split()[1]
                with open(filePath) as fileTransaction:
                    for lineFile in fileTransaction.readlines():
                        if datePattern.match(lineFile):
                            date = (lineFile.split()[0])
                            payee = (lineFile.strip(date))  # payee
                        if currency in lineFile:
                            account = (lineFile.split()[0])  # account
                            if (lineFile.split()[1]).startswith(currency):
                                value = (lineFile.split()[1]).strip(currency)
                            elif (lineFile.split()[1]).startswith('-'):
                                value = (lineFile.split()[1]).replace('-$', '-')
                            transactions.append(Transaction(date, payee, account, value))
    sum = 0.0
    print colored('-------------------------------------------------------------------------------------------','red')
    print colored(' DATE              PAYEE                      ACCOUNT              VALUE         TOTAL','blue')
    print colored('-------------------------------------------------------------------------------------------','red')
    for x in range(0, len(transactions)):
        total = float(transactions[x].value)
        sum += total
        print '{:^10}     {:25.17}{:^20}{:^20}{:^10}'.format(transactions[x].date, transactions[x].payee,
                                                             transactions[x].account, transactions[x].value, sum)


if __name__ == '__main__':
    fire.Fire({
        'balance': balance,
        'print': printable,
        'register': register,

    })
