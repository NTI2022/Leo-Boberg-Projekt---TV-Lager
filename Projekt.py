"""__author__  = "Leo Boberg"
__version__ = "1.0.0"
__email__   = "leo.boberg@elev.ga.ntig.se"""

# Importering av olika funktioner
import csv
import os
import locale
import sys

class bcolors:  # Klass för olika färger
    PURPLE = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Funktion för att ladda in datan från csv-filen
def load_data(filename):
    products = []
    
    with open(filename, 'r', encoding="UTF-8") as file:  # Öppnar csv och sorterar datan
        reader = csv.DictReader(file)
        for row in reader:
            id = int(row['id'])
            name = row['name']
            desc = row['desc']
            price = float(row['price'])
            quantity = int(row['quantity'])
            
            products.append(
                {
                    "id": id,
                    "name": name,
                    "desc": desc,
                    "price": price,
                    "quantity": quantity
                }
            )
    return products

def remove_product(products, id):  # Funktion för att ta bort en produkt
    # Leta efter produkten med det angivna ID:t
    for i, product in enumerate(products):
        if product["id"] == id:
            products.pop(i)  # Tar bort produkten utan att påverka ID:n för andra produkter
            return f"Produkt med ID {id} har tagits bort."
    return f"Produkt med ID {id} hittades inte."

def view_product(products, id):  # Funktion för att kunna se en specifik produkt
    os.system('cls')  # Tömmer skärmen innan man visar
    
    for product in products:
        if product["id"] == id:
            # Header för produktinformation
            header = (
                f"{bcolors.PURPLE}{'ID':<5}{bcolors.DEFAULT} "
                f"{bcolors.GREEN}{'NAMN':<35}{bcolors.DEFAULT} "
                f"{bcolors.GREEN}{'BESKRIVNING':<80}{bcolors.DEFAULT} "
                f"{bcolors.GREEN}{'PRIS':<10}{bcolors.DEFAULT} "
                f"{bcolors.GREEN}{'KVANTITET':<10}{bcolors.DEFAULT}\n"
                f"{bcolors.BLUE}{'-' * 143}{bcolors.DEFAULT}\n"
            )
            
            # Produktens data i tabell
            name = product['name']
            desc = product['desc']
            price = locale.currency(product['price'], grouping=True)
            quantity = product['quantity']
            row = f"{id:<5} {name:<35} {desc:<80} {price:<14} {quantity:<10}"
            
            return f"{header}{row}\n{bcolors.BLUE}{'-' * 143}{bcolors.DEFAULT}"
        
    return "Produkten hittas inte"
    

def view_products(products):  # Huvudfunktionen för att se alla produkter
    header = (
        f"{bcolors.PURPLE}{'ID':<5}{bcolors.DEFAULT} "
        f"{bcolors.GREEN}{'NAMN':<35}{bcolors.DEFAULT} "
        f"{bcolors.GREEN}{'BESKRIVNING':<80}{bcolors.DEFAULT} "
        f"{bcolors.GREEN}{'PRIS':<10}{bcolors.DEFAULT} "
        f"{bcolors.GREEN}{'KVANTITET':<10}{bcolors.DEFAULT}\n"
        f"{bcolors.BLUE}{'-' * 143}{bcolors.DEFAULT}\n"
        f"{bcolors.YELLOW}{'Lägga till produkt = L, Visa = V, Ändra = Ä, Ta bort en produkt = T, Sortera efter pris = S eller Avsluta programmet = A'}{bcolors.DEFAULT}"
    )

    separator = f"{bcolors.BLUE}{'-' * 143}{bcolors.DEFAULT}"  # linje
    
    rows = []
    for index, product in enumerate(products, 1):
        name = product['name']
        desc = product['desc']
        price = product['price']
        quantity = product['quantity']
        
        price = locale.currency(price, grouping=True)
        row = f"{product['id']:<5} {name:<35} {desc:<80} {price:<14} {quantity:<10}"

        rows.append(row)
    
    inventory_table = "\n".join([header, separator] + rows)
    
    return f"{inventory_table}"

def add_product(products, name, desc, price, quantity):  # Funktion för att kunna lägga till nya produkter
    # Få det största ID:t i produkterna och lägg till 1
    max_id = max((product['id'] for product in products), default=0)
    id = max_id + 1

    products.append(
        {
            "id": id,
            "name": name,
            "desc": desc,
            "price": price,
            "quantity": quantity
        }
    )
    return f"Lade till produkt: {id}"

def update_product(products, id, name, desc, price, quantity):  # Funktion för att ändra och uppdatera en produkt
    for product in products:
        if product["id"] == id:
            product["name"] = name
            product["desc"] = desc
            product["price"] = price
            product["quantity"] = quantity
            return f"Produkten med ID {id} har uppdaterats."
    return f"Produkten med ID {id} hittades inte."

def save_products(filepath, products):  # Funktion för att spara den nya datan till csv-filen
    csv_file_path = filepath
    
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "desc", "price", "quantity"])
        writer.writeheader()
        writer.writerows(products)

        print(f"Data successfully saved to {csv_file_path}")

def exit_program():  # Funktion för att avsluta programmet
    print("Avslutar...")
    sys.exit()

def sort_products_by_price(products):
    # Sorteringsfunktion 
    def get_price(product):
        return product['price']

    # Sortera produkterna med hjälp av get_price funktionen
    products.sort(key=get_price)
    

locale.setlocale(locale.LC_ALL, 'sv_SE.UTF-8')  # Automatiskt svenskt alfabet

os.system('cls')
csv_file_path = "db_products.csv"

products = load_data(csv_file_path)

while True:  # Huvudloopen
    try:
        os.system('cls')
        print(view_products(products))
        print(f"{bcolors.BLUE}{'-' * 143}{bcolors.DEFAULT}")

        choice = input("\nVad vill du göra: ").strip().upper()

        if choice == "L":  # Lägg till
            name = input("Namn på produkten: ")
            desc = input("Beskrivning av produkten: ")
            price = float(input("Pris: "))
            quantity = int(input("Antal av produkten: "))
            print(add_product(products, name, desc, price, quantity))
            save_products(csv_file_path, products)

        elif choice == "V":  # Visa
            id = int(input("Ange produkt-ID: "))
            if any(product['id'] == id for product in products):
                print(view_product(products, id))  # Töm skärmen och visa produkten
                input("Tryck på Enter för att fortsätta...")
            else:
                print("Ogiltig produkt")
                input("Tryck på Enter för att fortsätta...")  
                os.system('cls') 

        elif choice == "T":  # Ta bort
            id = int(input("Ange produkt-ID: "))
            print(remove_product(products, id))
            save_products(csv_file_path, products)

        elif choice == "Ä":  # Ändra
            id = int(input("Ange produkt-ID: "))
            if any(product['id'] == id for product in products):
                name = input(f"Nytt namn på produkten: ")
                desc = input(f"Ny beskrivning på produkten: ")
                price = float(input(f"Nytt pris på produkten: "))
                quantity = int(input(f"Nytt antal på produkten: "))
                print(update_product(products, id, name, desc, price, quantity))
                save_products(csv_file_path, products)
            else:
                print("Ogiltig produkt")
                input("Tryck på Enter för att fortsätta...")  
                os.system('cls') 

        elif choice == "S":  # Sortera efter pris
            print(sort_products_by_price(products))

        elif choice == "A":  # Kallar på avslutningsfunktionen
            exit_program()

    except ValueError:
        print("Välj en produkt med siffror")
