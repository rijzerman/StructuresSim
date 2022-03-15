from config import DELTA, STARTDATE, stockyard_times, BUCKET, BUFFER
import datetime


# class Salesorder:
#     def __init__(self):
#         pass

class ProductionOrder:
    def __init__(self, nr, so_nr, date, element_type):
        self._nr = nr
        self.po_nr = self.prod_nr()
        self.create_date = date
        self.element_type = element_type
        self.status = 'Gepland'
        self.finish_date_req = self.calc_fin_date_req()
        self.finish_date_erp = self.calc_fin_date_erp()
        self.finish_date_mes = self.finish_date_erp
        self.start_date_mes = self._calc_start_date_mes()
        self.start_date_erp = self._calc_start_date_mes()
        self.transport_date = self.calc_transport_date()
        self.delivery_date = self.calc_delivery_date()
        self._so_nr = so_nr
        self.s_id = self.sales_id()
        self.sent_to_MES = False
        self.changed_by_arjen = False

    def prod_nr(self):
        pn_str = 'P' + str(self._nr).zfill(5)
        return pn_str

    def sales_id(self):
        sn_str = "V" + str(self._so_nr).zfill(5)
        return sn_str

    def calc_fin_date_req(self):
        # Delta bepaald de required finished date
        calc_date = self.create_date + datetime.timedelta(days=DELTA)
        return calc_date

    def calc_fin_date_erp(self):
        # finished date ERP ligt grootte van bucket
        calc_date = self.create_date + datetime.timedelta(days=DELTA)
        check = datetime.date.weekday(calc_date)
        delta = BUCKET + BUFFER
        if check < delta:
            use_bucket = BUCKET + BUFFER + 2
        else:
            use_bucket = BUCKET + BUFFER
        calc_date -= datetime.timedelta(days=use_bucket)
        return calc_date

    def _calc_start_date_mes(self):
        check = datetime.date.weekday(self.finish_date_mes)
        delta_start = 1
        if check == 0:
            delta_start = 3
        calc_date = self.finish_date_mes - datetime.timedelta(days=delta_start)
        return calc_date

    def calc_start_date_mes(self):
        check = datetime.date.weekday(self.finish_date_mes)
        delta_start = 1
        if check == 0:
            delta_start = 3
        calc_date = self.finish_date_mes - datetime.timedelta(days=delta_start)
        self.start_date_mes = calc_date

    def calc_transport_date(self):
        calc_date = self.finish_date_req + datetime.timedelta(days=stockyard_times[self.element_type])
        check = datetime.date.weekday(calc_date)
        delta = 0
        if check == 5:
            delta = 2
        elif check == 6:
            delta = 1
        calc_date += datetime.timedelta(days=delta)
        return calc_date

    def calc_delivery_date(self):
        delta = 1
        if datetime.date.weekday(self.transport_date) == 4:
            delta = 3
        calc_date = self.transport_date + datetime.timedelta(days=delta)
        return calc_date

    def __str__(self):
        return f"SO: {self.s_id}, PO: {self.po_nr}, Elem_type: {self.element_type}, Status: {self.status}, To_MES: {self.sent_to_MES}, Changed: {self.changed_by_arjen}, C: {self.create_date}, " \
               f"S_ERP: {self.start_date_erp}, F_ERP: {self.finish_date_erp}, S_MES: {self.start_date_mes}, F_MES: {self.finish_date_mes}, F_REQ: {self.finish_date_req}," \
               f"T: {self.transport_date}, D: {self.delivery_date}".format(self=self)

