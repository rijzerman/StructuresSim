from os import system
from day_sim import simulate_day
import datetime
from config import STARTDATE, PRODUCTION_ORDERS_PER_DAY, BUCKET, BUFFER
from print_order import menu_print_order

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
    print(f"{day}, 07:30")
    print(f"Aantal productiedagen: {number_of_production_days}                                                   PRODUCTION_ORDERS_PER_DAY: {PRODUCTION_ORDERS_PER_DAY}")
    print(F"MENU                                                                       BATCH: 3, PLANNING_AANPASSING: {BUCKET}, BUFFER: {BUFFER}")
    print("==================================                                         =======================================================")
    print("1. simuleer 1 dag                                                          C = Creation datum")
    print("2. Bekijk huidige MES queue                                                S_ERP = Start datum in ERP")
    print("3. Bekijk wijzigingen in MES queue                                         F_ERP = Finish datum in ERP")
    print("4. Bekijk gestarte orders                                                  S_MES = Start datum in MES (mogelijk wijziging tov ERP)")
    print("5. Bekijk orders op Tasveld                                                F_MES = Finish datum in MES (mogelijk wijziging tov ERP)")
    print("6. Bekijk orders op transport                                              F_REQ = Vereiste einddatum tbv Tasveld uitharding")
    print("7. Bekijk afgeleverde orders                                               T = Transport datum")
    print("8. Bekijk alle orders in ERP                                               D = Delivery datum")
    print("9. Bekijk de gegevens van één productieorder.")
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
            nr = mes.index(po) + 1
            nr = str(nr).zfill(3)
            print(f"{nr}. {po}")
            counter += 1
            if counter % 40 == 0:
                input("klik op een toets om verder te gaan")
        input("klik op een toets om verder te gaan")
    elif select == 'changed':
        for po in mes:
            if po.changed_by_arjen:
                print(po)
                counter += 1
                if counter % 40 == 0:
                    input("klik op een toets om verder te gaan")
        input("klik op een toets om verder te gaan")


def print_started(started):
    counter = 0
    print(f"Aantal orders in productie: {len(started)}")
    for po in started:
        print(po)
        counter += 1
        if counter % 40 == 0:
            input("klik op een toets om verder te gaan")

    input("klik op een toets om verder te gaan")


def print_completed(completed):
    counter = 0
    print(f"Aantal afgeronde orders: {len(completed)}")
    for po in completed:
        print(po)
        counter += 1
        if counter % 40 == 0:
            input("klik op een toets om verder te gaan")

    input("klik op een toets om verder te gaan")

def print_transport(on_transport):
    counter = 0
    print(f"Aantal orders op transport: {len(on_transport)}")
    for po in on_transport:
        print(po)
        counter += 1
        if counter % 40 == 0:
            input("klik op een toets om verder te gaan")

    input("klik op een toets om verder te gaan")


def print_delivered(delivered):
    counter = 0
    print(f"Aantal orders afgeleverd: {len(delivered)}")
    for po in delivered:
        print(po)
        counter += 1
        if counter % 40 == 0:
            input("klik op een toets om verder te gaan")

    input("klik op een toets om verder te gaan")


def print_erp(erp):
    counter = 0
    print(f"Aantal orders in ERP: {len(erp)}")
    for po in erp:
        print(po)
        counter += 1
        if counter % 40 == 0:
            input("klik op een toets om verder te gaan")
    input("klik op een toets om verder te gaan")



def main():
    user_input = '1'
    erp = []
    mes = []
    started = []
    completed = []
    on_transport = []
    delivered = []
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
            erp, mes, started, completed, on_transport, delivered = simulate_day(erp, mes, started, completed, on_transport, delivered, keep_day)
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
            print_transport(on_transport)
        elif user_input == '7':
            print_delivered(delivered)
        elif user_input == '8':
            print_erp(erp)
        elif user_input == '9':
            menu_print_order(erp, mes)


if __name__ == '__main__':
    main()