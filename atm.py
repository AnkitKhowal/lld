# The ATM system should support basic operations such as balance inquiry, cash withdrawal, and cash deposit.
# Users should be able to authenticate themselves using a card and a PIN (Personal Identification Number).
# The system should interact with a bank's backend system to validate user accounts and perform transactions.
# The ATM should have a cash dispenser to dispense cash to users.
# The system should handle concurrent access and ensure data consistency.
# The ATM should have a user-friendly interface for users to interact with.

import random
from abc import ABC, abstractmethod

class ATM:
    
    def __init__(self,id, location,cashdispenser, bankService):
        self.__id = id
        self.__location = location
        self.__cashdispenser = cashdispenser
        self.__bankService = bankService

    def authenticate_user(self, card , pin):
        print("User with card authenticated", card)
    
    def checkBalance(self, accountNumber):
        acc = self.__bankService.getAccount(accountNumber)
        transaction = ReadBalanceTransaction(random.randint(1,1000),acc)
        self.__bankService.processTransaction(transaction)
    
    def cash_withdrawal(self,accountNumber, amount):
        acc = self.__bankService.getAccount(accountNumber)
        transaction = WithDrawTransaction(random.randint(1,1000),acc, amount)
        self.__bankService.processTransaction(transaction)
        self.__cashdispenser.dispenseCash(amount)
    
    def deposit_cash(self,accountNumber, amount):
        acc = self.__bankService.getAccount(accountNumber)
        transaction = DepositCashTransaction(random.randint(1,1000),acc, amount)
        self.__bankService.processTransaction(transaction)


class Account:

    def __init__(self,number, user_email, balance):
        self.__number = number
        self.__userEmail = user_email
        self.__balance = balance
    
    def get_account_number(self):
        return self.__number

    def get_balance(self):
        print("Total Balance in Account", self.__balance)
        return self.__balance

    def deposit(self, amount):
        self.__balance = self.__balance + amount
        return self.__balance

    def withdraw(self, amount):
        self.__balance = self.__balance - amount
        return self.__balance


class BankService:
    def __init__(self):
        self.bankaccountMap = {}
    
    def createAccount(self, accountNumber, user, initialBalance):
        self.bankaccountMap[accountNumber] = Account(accountNumber, user, initialBalance)
        return accountNumber

    def getAccount(self, accountNumber):
        return self.bankaccountMap[accountNumber]
    
    def processTransaction(self, transaction):
        transaction.execute()


class Card:
    def __init__(self, cardNumber, pin):
        self.__carNumber = cardNumber
        self.__pin = pin
    
    def cardNumber(self):
        return self.__carNumber
    
    def getPin(self):
        return self.__pin


class CashDispenser:

    def __init__(self, initialCash):
        self.__cashAvailable = initialCash
    
    def dispenseCash(self, amount):
        if amount > self.__cashAvailable:
            print("Amount Not available Now")
        self.__cashAvailable -=amount
        print("Cash Dispensed", amount)

class Transaction(ABC):
    def __init__(self, id, account, amount=0):
        self._id=id
        self._amount=amount
        self._account=account

    @abstractmethod
    def execute(self):
        pass



class WithDrawTransaction(Transaction):
    def __init__(self, id, account, amount):
        super().__init__(id, account, amount)
    
    def execute(self):
        self._account.withdraw(self._amount)

class DepositCashTransaction(Transaction):
    def __init__(self, id, account, amount):
        super().__init__(id, account, amount)
    
    def execute(self):
        self._account.deposit(self._amount)

class ReadBalanceTransaction(Transaction):
    def __init__(self, id, account):
        super().__init__(id,account)
    
    def execute(self):
        self._account.get_balance()


if __name__=="__main__":
    bankingSvc = BankService()
    cashDispenser = CashDispenser(10000)
    atm1 = ATM(1,"xyz",cashDispenser, bankingSvc)

    acc1 = bankingSvc.createAccount(1, "akhowal@ea.com", 500)
    acc2 = bankingSvc.createAccount(2, "gka@ea.com", 500)

    c1 = Card(1, "1234")

    atm1.authenticate_user(c1, 1234)
    atm1.checkBalance(acc1)

    atm1.cash_withdrawal(acc1, 200)
    atm1.checkBalance(acc1)

    atm1.deposit_cash(acc1, 900)
    atm1.checkBalance(acc1)

# There is a bank service responsible for creating bank accounts-it keep a map of accountNumbers and the accounts
# its does three things createAccounts in Bank , get Particular accounts based on account Number and execute transactions for account
# when you create  an account , an account object is created , accout is responsible for crud of balance

# there is a cash dispenser component , the cash dispenser represents the total amount of cash in ATM, when we withdraw cash
# we reduce the amount of money in cash dispenser

# Their is ATM Component that the users will use  , Atm will basically allow users to check balance , withdraw balance , deposit balance
# User will first authenticate itself using a card and pin
# Then it will check balance of its account , to check balance we pass the accountNumber which comes by reading the card
# atm will call the bank service and try to get the account based on account number
# then it will create a transaction based on the Transaction type which is read balance
# and call the banki service to execute the transaction  on the account

# similar for Deposit account
# it will call banking service to give the acc for the account Number provided
# it will then create a trasaction object to deposit amount in the account
# then it will call the banking service to execute the transaction
