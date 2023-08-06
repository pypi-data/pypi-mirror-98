import pandas as pd
import hbshare as hbs
from datetime import datetime
from sqlalchemy import create_engine
from hbshare.rm_associated.config import engine_params, style_names

hbs.set_token("qwertyuisdfghjkxcvbn1000")


class NavAttributionLoader:
    def __init__(self, fund_id, fund_type, start_date, end_date, factor_type):
        self.fund_id = fund_id
        self.fund_type = fund_type
        self.start_date = start_date
        self.end_date = end_date
        self.factor_type = factor_type

    def _load_calendar(self):
        sql_script = "SELECT JYRQ, SFJJ, SFZM, SFYM FROM funddb.JYRL WHERE JYRQ >= {} and JYRQ <= {}".format(
            self.start_date, self.end_date)
        res = hbs.db_data_query('readonly', sql_script)
        df = pd.DataFrame(res['data']).rename(
            columns={"JYRQ": 'calendarDate', "SFJJ": 'isOpen',
                     "SFZM": "isWeekEnd", "SFYM": "isMonthEnd"}).sort_values(by='calendarDate')
        df['isOpen'] = df['isOpen'].astype(int).replace({0: 1, 1: 0})
        df['isWeekEnd'] = df['isWeekEnd'].fillna(0).astype(int)
        df['isMonthEnd'] = df['isMonthEnd'].fillna(0).astype(int)

        return df[['calendarDate', 'isOpen', 'isWeekEnd', 'isMonthEnd']]

    def _load_fund_data(self):
        if self.fund_type == 'mutual':
            sql_script = "SELECT a.jjdm fund_id, b.jzrq tradeDate, b.hbcl accumulate_return from " \
                         "funddb.jjxx1 a, funddb.jjhb b where a.cpfl = '2' and a.jjdm = b.jjdm " \
                         "and a.jjzt not in ('3', 'c') " \
                         "and a.m_opt_type <> '03' and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                         "order by b.jzrq".format(self.fund_id, self.start_date, self.end_date)
            res = hbs.db_data_query('readonly', sql_script)
            data = pd.DataFrame(res['data'])
            data['ADJ_NAV'] = 0.01 * data['ACCUMULATE_RETURN'] + 1
        else:
            sql_script = "SELECT a.jjdm fund_id, b.jzrq tradeDate, b.fqdwjz as adj_nav from " \
                         "fundapp.jjxx1 a, fundapp.smlj b where a.cpfl = '4' and a.jjdm = b.jjdm " \
                         "and a.jjzt not in ('3') " \
                         "and a.jjdm = '{}' and b.jzrq >= {} and b.jzrq <= {} " \
                         "order by b.jzrq".format(self.fund_id, self.start_date, self.end_date)
            res = hbs.db_data_query('readonly', sql_script)
            data = pd.DataFrame(res['data'])

        data.rename(columns={"FUND_ID": "fund_id", "TRADEDATE": "tradeDate", "ADJ_NAV": "adj_nav"}, inplace=True)

        return data.set_index('tradeDate')['adj_nav']

    def _load_factor_data(self):
        factor_type = self.factor_type
        if factor_type == "style_allocation":
            factor_data = pd.DataFrame()
        elif factor_type == "industry":
            factor_data = pd.DataFrame()
        else:
            sql_script = "SELECT * FROM factor_return where TRADE_DATE >= {} and TRADE_DATE <= {}".format(
                self.start_date, self.end_date)
            engine = create_engine(engine_params)
            factor_return = pd.read_sql(sql_script, engine)
            factor_return['trade_date'] = factor_return['trade_date'].apply(lambda x: datetime.strftime(x, '%Y%m%d'))
            factor_return = pd.pivot_table(
                factor_return, index='trade_date', columns='factor_name', values='factor_ret').sort_index()[style_names]
            factor_data = (1 + factor_return).cumprod()

        return factor_data

    def load(self):
        calendar_df = self._load_calendar()
        fund_adj_nav = self._load_fund_data()
        factor_data = self._load_factor_data()

        data = {"calendar_df": calendar_df, "fund_adj_nav": fund_adj_nav, "factor_data": factor_data}

        return data
