import os,json, datetime,re 

import pandas as pd
import bar_chart_race as bcr


class Config_data():
    
    def __init__(self, dict_data) -> None:
        
        # 体重、血圧を管理するJson
        self.blood_pressure_info = os.path.join(os.getcwd(),'settings', f'blood_pressure_info.json')

        self.dt = dict_data.get('dt', '2024-01-01') 
        self.high_value = dict_data.get('high', 130) 
        self.low_value = dict_data.get('low', 80) 
        self.pulsation = dict_data.get('pulse', 75)
        self.weight_value = dict_data.get('weight', 60)
       
    def get_json_info(self):
        with open(self.blood_pressure_info, mode='r', encoding='utf-8') as json_file:
            return json.load(json_file)
    
    def add_new_data(self):
        exist_data = self.get_json_info()
        new_data = {
            'date': self.dt,
            'high': self.high_value,
            'low': self.low_value,
            'pulse': self.pulsation,
            'weight': self.weight_value
        }

        # 既存のデータのdateフィールドを抽出してリストに格納
        existing_dates = [item['date'] for item in exist_data]

        # 新しいデータのdateフィールドが既存のdateフィールドリストに含まれていない場合のみ、追加
        if new_data['date'] not in existing_dates:
            exist_data.append(new_data)

        # 更新されたデータをJSONファイルに書き込み
        with open(self.blood_pressure_info, 'w', encoding='cp932') as json_file:
                json.dump(exist_data, json_file, indent=4)

def create_data():
    start_date = datetime.date(2024, 2, 25)
    end_date = datetime.date.today()  
    blood_pressure_data_set1 = [165, 168, 162, 170, 161, 153, 162, 153, 158, 153]
    blood_pressure_data_set2 = [121, 119, 119, 120, 120, 112, 110, 112, 114, 112]
    dates = [start_date + datetime.timedelta(days=i) for i in range((end_date - start_date).days + 1)]

    dict_data = {}
    for dt, high, low in zip(dates, blood_pressure_data_set1, blood_pressure_data_set2):
        dict_data['dt'] = dt
        dict_data['high'] = high
        dict_data['low'] = low
        ins = Config(dict_data)
        ins.add_new_data()

class CsvReader():
    def __init__(self) -> None:
        self.file_path = 'merged_data.csv'
        self.pattern = r'(\d{4}年)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)\s+(\d+\.\d+)'

    def get_text_data(self):

        gdp_x = []
        gdp_japan = []
        with open(self.file_path, 'r', encoding='utf-8') as file:
            for line in file:
                print(line)
                matches = re.findall(self.pattern, line)
                for match in matches:
                    gdp_x.append(match[0])
                    gdp_japan.append(match[1])
        return gdp_x, gdp_japan
    
    def get_gdp_df(self):
        df = pd.read_csv(self.file_path, encoding='utf-8',index_col=0)
        return df
        
if __name__ == '__main__':
    # 単体テスト
    # create_data()
    # ins = Config({})
    # print(ins.get_json_info())

    ins = CsvReader()
    # x, y = ins.get_text_data()
    df = ins.get_gdp_df()
    bcr.bar_chart_race(df=df, n_bars=len(df.columns),
                       title='GDP',
                        filename='output.mp4')


