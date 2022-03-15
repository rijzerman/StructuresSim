import datetime

from Orders import ProductionOrder
from config import stockyard_times

def print_order(order, mes_nr):
    tasveldtijd = order.transport_date - order.finish_date_mes
    tasveldtijd = tasveldtijd.days
    minimale_tasveldtijd = stockyard_times[order.element_type]
    to_mes = 'Ja' if order.sent_to_MES else 'Nee'
    gewijzigd = 'Ja' if order.changed_by_arjen else 'Nee'
    print("")
    print("   =============================================================")
    print(f"   | Verkooporder:   {order.s_id}                                    |")
    print(f"   | Productieorder: {order.po_nr}                                    |")
    print(f"   | Element_type:   {order.element_type}                                        |")
    print(f"   | Aanmaakdatum:   {order.create_date}                                |")
    print(f"   |                                                           |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | STATUS DATA                                               |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | Orderstatus:            {order.status: <16}                  |")
    print(f"   | Verstuurd naar MES:     {to_mes: <4}                              |")
    print(f"   | MES Planning aangepast: {gewijzigd: <4}                              |")
    print(f"   |                                                           |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | ERP DATA                                                  |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | ERP Startdatum planning:  {order.start_date_erp}                      |")
    print(f"   | ERP Einddatum planning:   {order.finish_date_erp}                      |")
    print(f"   | ERP Uiterlijke einddatum: {order.finish_date_req}                      |")
    print(f"   |                                                           |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | MES DATA                                                  |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | MES Startdatum:      {order.start_date_mes}                           |")
    print(f"   | MES Einddatum:       {order.finish_date_mes}                           |")
    print(f"   | Huidige MES positie: {mes_nr: <3}                                  |")
    print(f"   |                                                           |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | TASVELD, TRANSPORT EN LEVERING                            |")
    print(f"   | -----------------------------------------------------------")
    print(f"   | Minimum Tasveldtijd:       {minimale_tasveldtijd: <2} dagen                       |")
    print(f"   | Gerealiseerde Tasveldtijd: {tasveldtijd: <2} dagen                       |")
    print(f"   | Transportdatum:            {order.transport_date}                     |")
    print(f"   | Leverdatum:                {order.delivery_date}                     |")
    print("   =============================================================")
    print("")

def menu_print_order(erp, mes):
    user_input = input("Geef volledige Productieordercode of volgnummer: ")
    if user_input[0] == 'P':
        order_nr = user_input
    else:
        order_nr = 'P' + str(user_input).zfill(5)
    try:
        order_to_print = next(order for order in erp if order.po_nr == order_nr)
        mes_nr = '000'
        if order_to_print in mes:
            mes_nr = mes.index(order_to_print) + 1
            mes_nr = str(mes_nr).zfill(3)
        print_order(order_to_print, mes_nr)
    except StopIteration:
        print("Geen af te drukken orders aanwezig")
    except:
        print("IETS ANDERS GING FOUT")
    finally:
        input("klik op een toets om verder te gaan")

