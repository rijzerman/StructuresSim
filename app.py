from os import system
from day_sim import simulate_day
import datetime
from config import STARTDATE
from time import sleep

counter = 0

def clear():
    # define our clear function
    _ = system('cls')

def menu(day):
    clear()
    print(day)
    print("MENU")
    print("======================")
    print("1. simuleer 1 dag")
    print("2. Bekijk huidige MES queue")
    print("q. Stoppen")


def main():
    user_input = 1
    erp = []
    mes = []
    keep_day = STARTDATE
    while user_input != 'q' and user_input != 'Q':
        global counter
        counter += 1
        menu(keep_day)
        user_input = input("Maak keuze: ")
        if user_input == '1':
            keep_day += datetime.timedelta(days=1)
            if datetime.date.weekday(keep_day) == 5:
                keep_day += datetime.timedelta(days=2)
            elif datetime.date.weekday(keep_day) == 6:
                keep_day += datetime.timedelta(days=1)
            erp, mes = simulate_day(erp, mes, counter, keep_day)
            for order in mes:
                print(order)
            sleep(10)






if __name__ == '__main__':
    main()