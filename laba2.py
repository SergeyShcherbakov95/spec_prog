from spyre import server

import pandas as pd
from datetime import datetime

class StockExample(server.App):
    title = "VHI - lab2"

    inputs = [{    "input_type": 'dropdown',
                   "label": 'Setting',
                   "options": [{"label": "VHI", "value": "VHI"},
                               {"label": "TCI", "value": "TCI"},
                               {"label": "VCI", "value": "VCI"}],
                   "variable_name": 'setting',
                   "action_id": "update_data" },

              {    "input_type": 'dropdown',
                   "label": 'Province',
                   "options": [{"label": "Vinnickaya", "value": "01"},
                               {"label": "Volinskaya", "value": "02"},
                               {"label": "Dnepropetrovskaya", "value": "03"},
                               {"label": "Doneckaya", "value": "04"},
                               {"label": "Zhytomirskaya", "value": "05"},
                               {"label": "Zakarpatskaya", "value": "06"},
                               {"label": "Zaporojskaya", "value": "07"},
                               {"label": "Ivano-Frankovskaya", "value": "08"},
                               {"label": "Kievskaya", "value": "09"},
                               {"label": "Kirovogradskaya", "value": "10"},
                               {"label": "Luganskaya", "value": "11"},
                               {"label": "Lvovskaya", "value": "12"},
                               {"label": "Nikolaevskaya", "value": "13"},
                               {"label": "Odeskaya", "value": "14"},
                               {"label": "Poltavskaya", "value": "15"},
                               {"label": "Rovenskaya", "value": "16"},
                               {"label": "Summskaya", "value": "17"},
                               {"label": "Ternopol'skaya", "value": "18"},
                               {"label": "Khar'kovskaya", "value": "19"},
                               {"label": "Khersonskaya", "value": "20"},
                               {"label": "Hmel'nickaya", "value": "21"},
                               {"label": "Cherkasskaya", "value": "22"},
                               {"label": "Chernivec'ka", "value": "23"},
                               {"label": "Chernigovskaya", "value": "24"},
                               {"label": "Krim", "value": "25"},],
                   "variable_name": 'province',
                   "action_id": "update_data"},

              {    "input_type": 'text',
                   "label": 'Year',
                   "value": '1995',
                   "variable_name": 'year',
                   "action_id": "update_data" },

              {    "input_type": 'text',
                   "label": 'Week from',
                   "value": '1',
                   "variable_name": 'week_start',
                   "action_id": "update_data" },

              {    "input_type": 'text',
                   "label": 'Week to',
                   "value": '52',
                   "variable_name": 'week_end',
                   "action_id": "update_data" },

              {    "input_type": 'dropdown',
                   "label": 'Summer',
                   "options": [{"label": "No", "value": "no"},
                               {"label": "Yes", "value": "yes"},],
                   "variable_name": 'summer',
                   "action_id": "update_data" },]

    controls = [{   "control_type": "hidden",
                    "label": "get historical value of VCI/TCI/VHI",
                    "control_id": "update_data"}]

    tabs = ["Plot", "Table"]

    outputs = [{    "output_type": "plot",
                    "output_id": "plot",
                    "control_id": "update_data",
                    "tab": "Plot",
                    "on_page_load": True },

                {   "output_type": "table",
                    "output_id": "table_id",
                    "control_id": "update_data",
                    "tab": "Table",
                    "on_page_load": True }]

    def getData(self, params):
        setting = params['setting']
        province = params['province']
        year = int(params['year'])
        week_start = int(params['week_start'])
        week_end = int(params['week_end'])
        summer = params['summer']
        df = pd.read_csv('vhi-' + province + '-' + datetime.strftime(datetime.now(), "--%m-%Y") + '.csv' , index_col = False, header = 1)
        df = df[(df['VHI'] != -1.00)]
        df = df[(df['VCI'] != -1.00)]
        df = df[(df['TCI'] != -1.00)]

        if(summer == "yes"):
            df = df[(df['VHI'] > 60) & (df['week'] > 22) & (df['week'] < 27)]
            list = df.year.tolist()
            for i in list:
                index =  list.count(i)
                if index != 4:
                    df = df[df['year'] != i]
            df = df[['year', 'VHI']]
            return df

        if (year > 2015) and (week_end > 5) or (year < 1982):
            year = 2008
        if (week_start < 1) or (week_start > week_end) or (week_start > 52):
            week_start = 1
        if (week_end > 52) or (week_end < 1):
            week_end = 52

        df = df[df['year'] == int(year)]
        df = df[df['week'] >= int(week_start)]
        df = df[df['week'] <= int(week_end)]
        df = df[['week', setting]]

        return df

    def getPlot(self, params):
        df = self.getData(params)
        plt_obj = df.set_index('week').plot()
        plt_obj.set_ylabel(list(df[:0])[1])
        plt_obj.set_title('VHI-TCI-VCI')
        fig = plt_obj.get_figure()
        return fig

app = StockExample()
app.launch(port=9093)