from Orders import ProductionOrder
from config import PRODUCTIONORDERS_PER_DAY, MES_QUEUE_FIXED, STARTDATE, WINDOW, DELTA
import datetime


def create_day(so_nr, po_nr, date):
    day = []
    po_nr = po_nr
    so_nr = so_nr
    for i in range(PRODUCTIONORDERS_PER_DAY):
        po_nr += 1
        po = ProductionOrder(po_nr, so_nr, date)
        if po_nr % 3 == 0:
            so_nr += 1
        day.append(po)

    return day


def send_to_mes(erp, mes, date):
    to_mes = []
    check_date = date + datetime.timedelta(days=WINDOW)
    for po in erp:
        if po.finish_date <= check_date and not po.sent_to_MES:
            po.sent_to_MES = True
            to_mes.append(po)
    for po in to_mes:
        mes.append(po)
    print("wait")
    return mes






def simulate_day(erp, mes, nr, date):
    po_number = len(erp)
    print(po_number)
    if len(erp) == 0:
        so_number = 1
    else:
        so_number = erp[-1].so_nr
    po_day = create_day(so_number, po_number, date)
    for po in po_day:
        erp.append(po)
    if nr % 3 == 0:
        mes = send_to_mes(erp, mes, date)
    else:
        pass
    return erp, mes