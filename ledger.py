import re
import fire

datePattern = re.compile(r"\d{4}/\d{1,2}/\d{1,2}")
currency = '$'

transactions = []


class Transaction:
    def __init__(self):
        self.date = ''
        self.payee = ''
        self.account = ''
        self.value = float


def handle():
    with open('index.ledger') as file:
        for line in file.readlines():
            if line.startswith(";"):
                continue
            if line.startswith("!include"):
                with open(line.split()[1]) as f:
                    for li in f.readlines():
                        transaction = Transaction()
                        # print(li)
                        transactions.append(transaction)
                        if datePattern.match(li):
                            date = (li.split()[0])
                            transaction.date = date
                            # print(date) #date
                            transaction.payee = (li.strip(date))  # payee
                        if currency in li:
                            transaction.account = (li.split()[0])  # account
                            if (li.split()[1]).startswith('$'):
                                transaction.value = (li.split()[1]).strip('$')
                            elif (li.split()[1]).startswith('-'):
                                transaction.value = (li.split()[1]).replace('-$', '-')

                            print '{}      {}'.format(transaction.account, (float(transaction.value)))

                            # yield ' {}         {}'.format(transaction.account, transaction.value)


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
    handle()

    # not access list transaction
    # mydicts = {k: dict(v) for k, v in transactions.items()}



if __name__ == '__main__':
    fire.Fire({
        'balance': handle,
        'print': printable,
        'register': register,

    })
