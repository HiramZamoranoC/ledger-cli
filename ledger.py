import re
import fire
from termcolor import colored

DATA_PATTERN = re.compile(r"\d{4}/\d{1,2}/\d{1,2}")
DOLLAR_SIGN = '$'
INDEX = 'index.ledger'


class Transaction:
    def __init__(self, date=None, payee=None, account=None, value=None):
        self.date = date
        self.payee = payee
        self.account = account
        self.value = value


def getTransactionFile(transactions):
    with open(INDEX) as indexFile:
        for lineIndex in indexFile.readlines():
            if lineIndex.startswith("!include"):
                pathFile = lineIndex.split()[1]
                openTransactionFile(pathFile, transactions)



def openTransactionFile(pathFile, transactions):
    with open(pathFile) as transactionFile:
        for lineFile in transactionFile.readlines():
            try:
                if DATA_PATTERN.match(lineFile):
                    date = (lineFile.split()[0])
                    payee = (lineFile.strip(date))
                if DOLLAR_SIGN in lineFile:
                    account = (lineFile.split()[0])
                    if (lineFile.split()[1]).startswith(DOLLAR_SIGN):
                        value = (lineFile.split()[1]).strip(DOLLAR_SIGN)
                    elif (lineFile.split()[1]).startswith('-'):
                        value = (lineFile.split()[1]).replace('$', '')
                    transactions.append(Transaction(date, payee, account, value))
            except ImportError:
                print 'Format incorrect in ' + pathFile + ' file'
                continue


def register():
    transactions = []
    getTransactionFile(transactions)
    sum = 0.0
    print colored('-------------------------------------------------------------------------------------------', 'red')
    print colored(' DATE              PAYEE                      ACCOUNT              VALUE         TOTAL', 'blue')
    print colored('-------------------------------------------------------------------------------------------', 'red')
    for x in range(0, len(transactions)):
        total = float(transactions[x].value)
        sum += total
        print '{:^10}     {:25.17}{:^20}{:^20}{:^10}'.format(transactions[x].date, transactions[x].payee,
                                                             transactions[x].account, transactions[x].value, sum)


def balance():
    transactions = []
    getTransactionFile(transactions)
    sum = 0.0
    print colored('------------------------------------', 'red')
    print colored('   VALUE             ACCOUNT', 'blue')
    print colored('------------------------------------', 'red')
    for x in range(0, len(transactions)):
        print '{:^10}{:^30}'.format(transactions[x].value, transactions[x].account)
        total = float(transactions[x].value)
        sum += total
    print colored(' --------', 'green')
    print colored('{:^10}'.format(sum), 'white', )
    print colored(' --------', 'green')


def printable():
    with open(INDEX) as indexFile:
        for lineIndex in indexFile.readlines():
            if lineIndex.startswith("!include"):
                filePath = lineIndex.split()[1]
                with open(filePath) as transactionFile:
                    for lineFile in transactionFile.readlines():
                        print(lineFile)


if __name__ == '__main__':
    fire.Fire({
        'balance': balance,
        'print': printable,
        'register': register,

    })
