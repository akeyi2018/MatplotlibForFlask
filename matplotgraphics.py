import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
from matplotlib.dates import date2num

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Hiragino Sans', 'Hiragino Kaku Gothic Pro', 'Meiryo', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

from data_config import Config_data

class MatGrapics:
    def __init__(self):
        pass

    def get_json_data(self):
        ins = Config_data({})
        data = ins.get_json_info()
        # リストの最初の要素を使用して、すべてのキーを抽出します。
        keys = data[0].keys()

        # 各キーに対して、リストを作成し、そのキーの値をリストに追加します。
        data_by_key = {key: [item[key] for item in data] for key in keys}
        return data_by_key
    
    def create_blood(self):
      
        data = self.get_json_data()

        # Example blood pressure data sets
        blood_pressure_data_set1 = data['high']
        blood_pressure_data_set2 = data['low']
        weight_data = data['weight']
        pulse_data = data['pulse']

        # Create a list of dates from the start_date to the end_date
        # dates = [datetime.datetime.strptime(date_string, "%Y-%m-%d").date() for date_string in data['date']]
        dates = [date2num(datetime.datetime.strptime(date_string, "%Y-%m-%d").date()) for date_string in data['date']]

        # 体重データに2次多項式をフィットさせる
        # coefficients = np.polyfit(dates, blood_pressure_data_set1 , 2)
        # polynomial = np.poly1d(coefficients)

        # Plot the first set of blood pressure data
        plt.plot_date(dates, blood_pressure_data_set1, marker='o', linestyle='--', label='最高血圧', color='crimson')

        # 近似曲線を描く
        # plt.plot_date(dates, polynomial(dates), marker='o', linestyle='--', label='High Blood Pressure Approximation', color='g', linewidth=10)

        # Annotate the plotted values
        for date, value in zip(dates, blood_pressure_data_set1):
            plt.annotate(str(value), (date, value), textcoords="offset points", xytext=(-10,10), ha='center', color='crimson')

        # Plot the second set of blood pressure data
        plt.plot_date(dates, blood_pressure_data_set2, marker='o', linestyle='--', label='最低血圧', color='tomato')

        #   # Annotate the plotted values
        for date, value in zip(dates, blood_pressure_data_set2):
            plt.annotate(str(value), (date, value), textcoords="offset points", xytext=(-10,10), ha='center', color='tomato')

        plt.plot_date(dates, pulse_data, marker='o', linestyle='--', label='心拍数', color='deeppink')

        for date, value in zip(dates, pulse_data):
            plt.annotate(str(value), (date, value), textcoords="offset points", xytext=(-10,10), ha='center', color='deeppink')

        #   # Add annotations for normal values
        plt.axhline(y=135, color='crimson', linestyle='-', linewidth=20, alpha=0.3)
        plt.axhline(y=80, color='tomato', linestyle='-', linewidth=20, alpha=0.3)
        # plt.fill_between(dates, 135, 180, color='tomato', alpha=0.2)
        # plt.fill_between(dates, 80, 135, color='lightskyblue', alpha=0.2)
        
        plt.legend(loc='upper left')

        # Set labels and title
        plt.title('(血圧/体重)管理')
        plt.xlabel('日付')
        plt.ylabel('血圧(mmHg)')
        
        plt.ylim(60, 180)

        ax2 = plt.gca().twinx()

        ax2.plot_date(dates, weight_data, marker='o', linestyle='--', label='体重', color='g')
        

        for date, value in zip(dates, weight_data):
            ax2.annotate(str(value), (date, value), textcoords="offset points", xytext=(15,-10), ha='center')

        ax2.axhline(y=72, color='g', linestyle='-', linewidth=20, alpha=0.3)

        ax2.legend(loc='upper right')

        ax2.set_ylabel('体重(kg)', rotation=90, labelpad=15)
        ax2.yaxis.set_label_position('right')
        ax2.set_ylim(71,80)

        # Format the x-axis to display dates
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator())
        plt.gcf().autofmt_xdate()

        return plt
        # plt.show()
    

if __name__ == '__main__':
    ins = MatGrapics()
    # print(ins.get_json_data())
    ins.create_blood()
