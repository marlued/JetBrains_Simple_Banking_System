from random import randint


class Account:

    def __init__(self):
        self._account_number = None
        self._name = None
        self._balance = 0
        self._password = None

    @property
    def password(self):
        """The password property"""
        return self._password

    @property
    def balance(self):
        """The balance property"""
        return self._balance

    @balance.setter
    def balance(self, value):
        self._balance += value

    def set_password(self):
        # range_start and _end to assure a 4-digit account number
        range_start = 10 ** (4 - 1)
        range_end = (10 ** 4) - 1
        new_password = randint(range_start, range_end)
        self._password = new_password
        return new_password


class Bank:

    def __init__(self):
        self.accounts_dic = {}

    def create_account(self):
        inn = 400_000

        # range_start and _end to assure a 9-digit account number
        range_start = 10 ** (9 - 1)
        range_end = (10 ** 9) - 1
        customer_account_number = randint(range_start, range_end)

        checksum = randint(0, 9)
        new_acc_no = int(f'{inn}{customer_account_number}{checksum}')

        new_account = Account()

        if new_acc_no not in self.accounts_dic:
            self.accounts_dic[new_acc_no] = new_account
        else:

            raise IndexError('Account already exists')

    def get_balance(self):
        account_number = int(input('Please enter account number ').strip())
        account = self.accounts_dic[account_number]
        account_password = account.password
        user_password = int(input('Please enter your password ').strip())
        if account_password == user_password:
            return account.balance
        else:
            raise KeyError('Wrong Password for account')

    def set_balance(self):
        account_number = int(input('Please enter account number ').strip())
        value = int(input('Please enter money to deposit ').strip())
        account = self.accounts_dic[account_number]
        account.balance = value

    def get_password(self):
        account_number = int(input('Please enter account number ').strip())
        account = self.accounts_dic[account_number]
        return account.password

    def set_password(self):
        account_number = int(input('Please enter account number ').strip())
        account = self.accounts_dic[account_number]
        account.set_password()
