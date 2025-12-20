import json


print("**+-----------|Bugget Keeper|-----------+**")

try:
    with open("expenses.json", "r") as f:
        expenses = json.load(f)
except (json.JSONDecodeError,FileNotFoundError):
    expenses = []
    

while True:
    going = True
    
    
    print("\nchoose what you want or write anything else to exit\n\n1. Add Expense\n2. List All Expenses\n")
    choose = input("your choose is: ")
    
    if choose == "1":
        print("\n*-----write 'stop' anytime to stop this program and cansel dictionary-----*\n")
        while going:
            user_dict = {"amount": None, "category": "Unknown", "description": "nothing"}

            for key in user_dict.keys():
                
                input_u = input(f"enter the '{key}' for your thing: ")
                if input_u.lower() == "stop":
                    going = False
                    break
                elif key == "amount":
                    try:
                        user_dict[key] = float(input_u)
                    except ValueError as e:
                        print(f"\nerror happen : {e}\n\nyou should write a number  'amount' will take as 0, write stop if you want to restart\n")
                else:
                    user_dict[key] = input_u
            
            if going:
                expenses.append(user_dict)
                with open("expenses.json","w") as f:
                    json.dump(expenses,f)
                print(f"\n**+-----------|Saved|-----------+**\n")
            else:
                print("\nExitting...\n")
            
            
            
    elif choose == "2":
        num =1
        if len(expenses) < 1:
            print("your expenses are empty.\n\nExitting...")
        else:    
            print("\n\t   amount|catgagory|descrption")
            for dics in expenses:
                
                print(f"your {num} is: ",end="")
                
                print(*dics.values(), sep="   |     ")
                
                num +=1
        
    else:
        print("\n\nExitting...")
        break
        
with open("expenses.json","w") as f:
    json.dump(expenses,f)
