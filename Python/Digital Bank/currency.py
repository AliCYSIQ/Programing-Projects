import requests as req
import sys



while True:    
    
    base_currency = input("Convert from which currency?: ").upper()
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    resonse = req.get(url)
    if resonse.status_code == 200:
        break
    else:
        print("\nplease write the currency correct, we will start again\n")

data = resonse.json()
while True:    
    
    target_currency = input("Convert to which currency?").upper()
    if data["rates"].get(target_currency,"other") != "other":
        break
    else:
        print("\nplease write the currency correct, we will start again\n")




while True:    
    try:
        Amount = float(input("please enter how much you want to convert: "))
        break
    except (ValueError,TypeError):
        print("please enter vaild number like 100.5 without any other litters or character\n")




rate = float(data["rates"].get(target_currency))

print(f"{Amount} {base_currency} on {data["date"]} eqaul {round(rate * Amount,3)} in {target_currency}  ")