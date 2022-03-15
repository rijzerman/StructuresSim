from Orders import ProductionOrder
from config import PRODUCTION_ORDERS_PER_DAY, WINDOW, stockyard_times, PERC_CHANGE, BUCKET
import datetime
import random


def create_day(so_nr, po_nr, date):
    day = []
    po_nr = po_nr
    so_nr = so_nr
    element_type = 50
    for i in range(PRODUCTION_ORDERS_PER_DAY):
        po_nr += 1
        po = ProductionOrder(po_nr, so_nr, date, element_type)
        if po_nr % 3 == 0:
            so_nr += 1
            element_type = random.choice(list(stockyard_times.keys()))
        day.append(po)

    return day

def change_production_orders(mes, sales_order, dates):

    # get current date for sales_order
    for po in mes:
        if po.s_id == sales_order:
            date_selected_so = po.finish_date_mes
            break

    change_to_date = date_selected_so

    # select random from dates, not equal to current date.
    while change_to_date == date_selected_so:
        change_to_date = random.choice(dates)

    # change all order mes dates
    for po in mes:
        if po.s_id == sales_order:
            po.finish_date_mes = change_to_date
            po.changed_by_arjen = True
            po.calc_start_date_mes()

    return mes


def arjen(mes):
    dates = []
    sales_orders = []
    for po in mes:
        dates.append(po.finish_date_erp)
        sales_orders.append(po.s_id)
    dates = list(set(dates))
    sales_orders = list(set(sales_orders))
    if len(dates) == 3:
        for so in sales_orders:
            chance = random.random()
            if chance < PERC_CHANGE:
                mes = change_production_orders(mes, so, dates)
        for po in mes:
            po.sent_to_MES = True
    else:
        # if only 1 or 2 dates, then no shuffle.
        mes = []
    return mes



def send_to_mes(erp, mes, date):
    to_mes = []
    check_date = date + datetime.timedelta(days=WINDOW)
    for po in erp:
        if po.finish_date_erp <= check_date and not po.sent_to_MES:
            to_mes.append(po)

    if len(to_mes) > 0:
        to_mes = arjen(to_mes)
        for po in to_mes:
            mes.append(po)
    return mes


def simulate_day(erp, mes, started, completed, on_transport, delivered, date):
    po_number = len(erp)
    print(po_number)
    if len(erp) == 0:
        so_number = 1
    else:
        so_number = erp[-1]._so_nr + 1
    # 1 day production to erp
    po_day = create_day(so_number, po_number, date)
    for po in po_day:
        erp.append(po)
    mes = send_to_mes(erp, mes, date)

    # check started
    for po in reversed(mes):

        # VRIJGAVE MES
        delta = 1
        if datetime.date.weekday(po.start_date_mes) == 0:
            delta = 3
        check_date_released = po.start_date_mes - datetime.timedelta(days=delta)
        if check_date_released == date:
            po.status = 'Vrijgegeven'

        # START MES
        check_date_started = po.start_date_mes

        if check_date_started == date:
            po.status = 'Begonnen'
            started.append(po)
            mes.remove(po)

    for po in reversed(started):
        if po.finish_date_mes <= date:   # verwijderd: + datetime.timedelta(days=1)
            po.status = 'Gereed gemeld'
            completed.append(po)
            started.remove(po)

    for po in reversed(completed):
        if po.transport_date == date:
            on_transport.append(po)
            completed.remove(po)

    for po in reversed(on_transport):
        if po.delivery_date == date:
            po.status = 'Gereed'
            delivered.append(po)
            on_transport.remove(po)


    mes.sort(key=lambda x: x.finish_date_mes, reverse=False)

    return erp, mes, started, completed, on_transport, delivered
