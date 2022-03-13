from config import DELTA, STARTDATE
import datetime

# class Salesorder:
#     def __init__(self):
#         pass

class ProductionOrder:
    def __init__(self, nr, so_nr, date):
        self.nr = nr
        self.po_nr = self.prod_nr()
        self.create_date = date
        self.finish_date = self.calc_fin_date()
        self.so_nr = so_nr
        self.s_id = self.sales_id()
        self.sent_to_MES = False

    def prod_nr(self):
        pn_str = 'P' + str(self.nr).zfill(5)
        return pn_str

    def sales_id(self):
        sn_str = "S" + str(self.so_nr).zfill(5)
        return sn_str

    def calc_fin_date(self):
        calc_date = self.create_date + datetime.timedelta(days=DELTA)
        return calc_date

    def __str__(self):
        return f"PO: {self.po_nr}, SO: {self.s_id}, Finish_date: {self.finish_date}".format(self=self)

