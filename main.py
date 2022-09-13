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


class Bank():

    def __init__(self):
        self.accounts_dic = {}

    def create_account(self):

        # Creation of credit_card_number in accordance with luhn algorithm:

        # Creation of a 14-digit card number without checksum

        range_start = 10 ** (14 - 1)
        range_end = (10 ** 14) - 1
        customer_account_number = randint(range_start, range_end)

        inn = 4

        # Creation of 15-digit number with 4 as first digit

        new_acc_no = int(f'{inn}{customer_account_number}')

        # Cast number to list for further processing

        # This is the part of the credit card number without control digit:
        # It will be used for creating the credit card number with the
        # control digit when the control digit has been calculated according
        # to luhn algorithm

        number_as_list = [int(element) for element in str(new_acc_no)]
        print(number_as_list)

        # Separation of number as list for usage in luhn-algorithm

        numbers_not_to_process = number_as_list[::2]
        numbers_to_process = number_as_list[1::2]

        # Multiplying every second digit of number by two (fist stage)

        processed_numbers_stage_one = [
            element * 2 for element in numbers_to_process
        ]

        # If doubling a number results in a two-digit number ->
        # add the digits of the product to get a single digit number

        processed_numbers_stage_two = [1 + (element - 10) if element > 9
                                       else element for element in processed_numbers_stage_one
                                       ]

        # Combining numbers_not_to_process with processed_numbers (stage 2)

        luhn_numbers_stage_one = list(zip(
            numbers_not_to_process, processed_numbers_stage_two))

        # flatten luhn_numbers_stage_one

        luhn_numbers_stage_two = [element for sub_element in
                                  luhn_numbers_stage_one for element in sub_element]

        # add last digit of numbers_as_list (missing because of zip-function)

        luhn_numbers_stage_two.append(number_as_list[-1])

        # Calculate control digit depending on sum of digits in list

        control_digit = sum(luhn_numbers_stage_two) % 10

        if control_digit == 0:
            luhn_numbers_stage_two.append(0)

        else:
            luhn_numbers_stage_two.append(10 - control_digit)

        # debug: Show if number % 10 == 0

        print(luhn_numbers_stage_two)
        print(sum(luhn_numbers_stage_two) % 10 == 0)

        # Separate control_digit in order to add it to the credit card number
        control_digit_for_credit_card_number = luhn_numbers_stage_two.pop()

        # Add control_number to numbers_as_list in oder to create
        # a credit card number with control digit

        number_as_list.append(control_digit_for_credit_card_number)

        # debug print credit_card_number with control_digit

        print(number_as_list)

        # Cast list to credit card number as int

        pre_processed_number = [str(element) for element in number_as_list]

        credit_card_number = int(''.join(pre_processed_number))

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
        pin_number = int(input(("Enter your PIN:\n").strip()))

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
