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

        # Creation of credit_card_number in accordance with luhn algorithm:

        # Creation of a 9-digit card number without checksum

        range_start = 10 ** (9 - 1)
        range_end = (10 ** 9) - 1
        customer_account_number = randint(range_start, range_end)

        inn = 400000

        # Creation of 15-digit number with 400000 as first digits

        new_acc_no = int(f'{inn}{customer_account_number}')

        # Cast number to list for further processing

        number_as_list = [int(element) for element in str(new_acc_no)]

        # Multiplying every second digit of number by two (fist stage)
        # starting from right side of list assuming a 16-digit number

        luhn_stage_one = [element * 2 if counter % 2 == 0 else
                          element for counter, element in enumerate(number_as_list)]

        # If doubling a number results in a two-digit number ->
        # add the digits of the product to get a single digit number
        # -> element - 9 gets the same result

        luhn_stage_two = [element - 9 if element > 9 else element
                          for element in luhn_stage_one]

        # Calculate control digit depending on sum of digits in list

        sum_stage_two = sum(luhn_stage_two)

        check_digit = (10 - sum_stage_two % 10)

        # Add control digit to the credit card number

        number_as_list.append(check_digit)

        # if control_digit == 0 it has to be replaced with 9

        if number_as_list[-1] == 0:
            number_as_list.pop()
            number_as_list.append(9)

        # Cast list to credit card number as int

        credit_card_number_lst = [str(element) for element in number_as_list]

        credit_card_number = int(''.join(credit_card_number_lst))

        # Assign credit_card_number according to luhn algorithm to account number

        new_acc_no = credit_card_number

        new_account = Account()

        if new_acc_no not in self.accounts_dic:
            self.accounts_dic[new_acc_no] = new_account
            return new_acc_no

        else:
            raise IndexError('Account already exists')

    def login(self):
        card_number = int(input("Enter your card number:\n").strip())
        pin_number = int(input("Enter your PIN:\n").strip())

        if card_number not in self.accounts_dic:
            raise KeyError(f'Wrong card number or PIN!')

        else:
            account_for_login = self.accounts_dic[card_number]

        if pin_number != account_for_login.password:
            raise KeyError(f'Wrong card number or PIN!')

        else:
            print('You have successfully logged in!')
            return card_number

    def get_balance(self, account_number):
        account_number = int(account_number)
        account = self.accounts_dic[account_number]
        return account.balance

    def set_balance(self):
        account_number = int(input('Please enter account number ').strip())
        value = int(input('Please enter money to deposit ').strip())
        account = self.accounts_dic[account_number]
        account.balance = value

    def get_password(self, account_number):
        account = self.accounts_dic[account_number]
        return account.password

    def set_password(self, account_number):
        account = self.accounts_dic[account_number]
        account.set_password()


my_bank = Bank()

running_flag = True

while running_flag:

    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")

    user_input = int(input().strip()[0])

    if user_input == 1:
        new_account_number = int(my_bank.create_account())
        my_bank.set_password(new_account_number)
        new_password = my_bank.get_password(new_account_number)
        print("Your card has been created")
        print("Your card number:")
        print(new_account_number)
        print("Your card PIN:")
        print(new_password)

    if user_input == 2:

        try:
            account = my_bank.login()
        except KeyError as error:
            print('Wrong card number or PIN!')
            continue

        while True:
            print('1. Balance')
            print('2. Log out')
            print('0. Exit')

            user_input = int(input().strip()[0])

            if user_input == 0:
                running_flag = False
                break

            if user_input == 2:
                print('You have successfully logged out!')
                break

            if user_input == 1:
                print(f'Balance: {my_bank.get_balance(account)}')
                continue

    if user_input == 0:
        print('Bye!')
        break
