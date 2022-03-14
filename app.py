from os import system
from day_sim import simulate_day
import datetime
from config import STARTDATE

number_of_production_days = 0

def clear():
    # define our clear function
    _ = system('cls')

def menu(day):
    global number_of_production_days
    clear()
    day += datetime.timedelta(days=1)
    if datetime.date.weekday(day) == 5:
        day += datetime.timedelta(days=2)
    elif datetime.date.weekday(day) == 6:
        day += datetime.timedelta(days=1)
    print(day)
    print(f"Aantal productiedagen: {number_of_production_days}")
    print("MENU")
    print("======================")
    print("1. simuleer 1 dag")
    print("2. Bekijk huidige MES queue")
    print("3. Bekijk wijzigingen in MES queue")
    print("4. Bekijk gestarte orders")
    print("5. Bekijk afgeronde orders")
    print("6. Bekijk alle orders in ERP")
    print("q. Stoppen")


def print_mes_queue(mes, select):
    counter = 0
    dates = []
    if select == 'all':
        print(f"Aantal orders in MES queue: {len(mes)}")
        for po in mes:
            dates.append(po.finish_date_mes)
        dates = list(set(dates))
        days = len(dates)
        print(f"Aantal dagen in MES queue: {days}")
        for po in mes:
            print(po)
            counter += 1
            if counter % 24 == 0:
                input("klik op een toets om verder te gaan")
        input("klik op een toets om verder te gaan")
    elif select == 'changed':
        for po in mes:
            if po.changed_by_arjen:
                print(po)
                counter += 1
                if counter % 24 == 0:
                    input("klik op een toets om verder te gaan")
        input("klik op een toets om verder te gaan")

def print_started(started):
    counter = 0
    print(f"Aantal orders in productie: {len(started)}")
    for po in started:
        print(po)
        counter += 1
        if counter % 24 == 0:
            input("klik op een toets om verder te gaan")

    input("klik op een toets om verder te gaan")

def print_completed(completed):
    counter = 0
    print(f"Aantal afgeronde orders: {len(completed)}")
    for po in completed:
        print(po)
        counter += 1
        if counter % 24 == 0:
            input("klik op een toets om verder te gaan")

    input("klik op een toets om verder te gaan")

def print_erp(erp):
    counter = 0
    print(f"Aantal orders in ERP: {len(erp)}")
    for po in erp:
        print(po)
        counter += 1
        if counter % 24 == 0:
            input("klik op een toets om verder te gaan")
    input("klik op een toets om verder te gaan")


def main():
    user_input = '1'
    erp = []
    mes = []
    started = []
    completed = []
    keep_day = STARTDATE
    while user_input != 'q' and user_input != 'Q':
        global number_of_production_days
        menu(keep_day)
        user_input = input("Maak keuze: ")
        if user_input == '1':
            keep_day += datetime.timedelta(days=1)
            if datetime.date.weekday(keep_day) == 5:
                keep_day += datetime.timedelta(days=2)
            elif datetime.date.weekday(keep_day) == 6:
                keep_day += datetime.timedelta(days=1)
            erp, mes, started, completed = simulate_day(erp, mes, started, completed, keep_day)
            number_of_production_days += 1
        elif user_input == '2':
            print_mes_queue(mes, 'all')
        elif user_input == '3':
            print_mes_queue(mes, 'changed')
        elif user_input == '4':
            print_started(started)
        elif user_input == '5':
            print_completed(completed)
        elif user_input == '6':
            print_erp(erp)







if __name__ == '__main__':
    main()