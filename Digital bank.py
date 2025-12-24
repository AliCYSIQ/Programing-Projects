import sqlite3


conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS accounts (owner TEXT,balance REAL)")
conn.commit()


class BankAccount:

    def __init__(self, owner: str, initial_balance: float = 0.0):

        self.owner = owner
        self.balance = initial_balance 
        print(f"\nnow you create account in our bank , the owner name is {owner} and you have ${initial_balance} as initial balance.\n")
        

    def deposit(self, amount: float) -> None:

        
        if amount <= 0:
            raise ValueError("Only positive numbers are allowed.")
        self.balance += amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE owner = ?",(self.balance,self.owner,))
        conn.commit()
        print(f"you diposit {amount}$, now you have ${self.balance} in your account")

    def withdraw(self, amount: float) -> None:
        
        if amount < 0 or self.balance < amount:
            raise ValueError("pleas make sure you write a postive number and number that you have in your account.")
        
        self.balance -= amount
        cursor.execute("UPDATE accounts SET balance = ? WHERE owner = ?",(self.balance,self.owner,))
        conn.commit()
        print(f"you withdraw ${amount} , now you have ${self.balance} in your account")

    def get_info(self) -> str:
        return f"Account: {self.owner} | Balance: ${self.balance}"


def main():
    
    
    print("\n--- welcome to our digital bank ---\n\n")
    while True:
        
        choose= input("1. Create a New Account\n2. Access an exists Account\n3. Exit\n\nYour Choose is: ").strip()
        if choose == '1':
            Create_New_Account()
        elif choose == '2':
            Access_exists_Account()
        elif choose == '3':
            conn.commit()
            conn.close()
            break
        else:
            print("\nplease write 1-3 only, do not use any other number or letter or char\n")

def Create_New_Account() -> None:
    
    while True:
                result = ''
                name = input("Please enter name to a new account('stop' to exit): ").lower()
                if name != "":
                    cursor.execute("SELECT owner FROM accounts WHERE owner = ?",(name,))
                    result = cursor.fetchone()
                    
                else:
                    print("please enter a name and DO NOT LEVET IT EMPTY!")
                

                if name == 'stop':
                    break
                
                elif result == None:
                    
                    while True:
                        try:
                            init_balance = float(input("please enter the initial deposit of this account: "))
                            if init_balance >= 0:
                                break
                            else:
                                print("please write a number more than(or equal) a zero")
                        except ValueError:
                            print("please enter a float number")
                    BankAccount(name,init_balance)
                    cursor.execute("INSERT INTO accounts VALUES (?, ?)", (name,init_balance,))
                    conn.commit()
                    break
                else:
                    print("the name is already taken , use another name ")

def Access_exists_Account() -> None:             
            name = input("please enter your name: ").strip().lower()
            cursor.execute("SELECT owner FROM accounts WHERE owner = ?",(name,))
            result = cursor.fetchone()
            
            while result == None:
                print('account not found')
                name = input("please enter your name: ").strip().lower()
                cursor.execute("SELECT owner FROM accounts WHERE owner = ?",(name,))
                result = cursor.fetchone()
            cursor.execute("SELECT balance FROM accounts WHERE owner = ?",(name,))
            balance = cursor.fetchone()[0]
            current_user = BankAccount(name,balance)
            print("\nloggin in...\n\n")
            while True:
                action = input("1. Deposit\n2. withdraw\n3. Info\n4. Log Out\n what action you want to take :")
                if action == '1':
                    try:
                        Amount = float(input("\n\nhow much you want to deposit: "))
                        try:
                            current_user.deposit(Amount)
                        except ValueError:
                            print("\nplease enter a number more than 0")
                    except ValueError:
                        print("\nplease write a float number")
                    
                elif action == '2':
                    try:
                        Amount = float(input("\n\nhow much you want to withdraw: "))
                        try:
                            current_user.withdraw(Amount)
                        except ValueError:
                            print("\nplease enter a number more than zero and less than (or equal) your balance")
                    except ValueError:
                        print("\nplease write a float number")
                    
                elif action == '3':                    
                    print(current_user.get_info())
                elif action == '4':
                    break
                else:
                    print("\nplease enter a vaild action")    


if __name__ == "__main__":
    main()