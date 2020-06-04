# Example showing how to plot a single state using a downloaded csv
# Matplotlib is a plotting library for the Python programming language and its numerical mathematics extension NumPy
# In computer programming, pandas is a software library written for the Python programming language for data manipulation and analysis
from matplotlib import pyplot as plt
import pandas as pd
from matplotlib.pyplot import figure

# https://www.kaggle.com/fireballbyedimyrnmom/us-counties-covid-19-dataset
# https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv
df = pd.read_csv(
    'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
    )
while True:
    
    ch1 = raw_input("1- Plot State\n2- All State\ne- Exit\n")
    
    if ch1 == "1":
        city = raw_input("Please, enter a city (Colorado, New York, Kansas etc..) in USA: ")
        status = raw_input("Please, select status to see deaths/cases: ")
        # Create a new data frame of a single state.
        df_city = df[ df['state'] == str(city) ].copy()
        # Make sure pandas realizes our date column is a date.
        df_city['date'] = pd.to_datetime(df_city['date'])
        # Sum up all the cases for city by date.
        # Use diff method to compair to previous day to get new cases.
        series_city_sum = df_city.groupby('date')[str(status)].sum()
        series_city_diff = series_city_sum.diff()
        
        plt.plot(series_city_diff.index, series_city_diff.values, label=city)
        # x ve y eksenine neye ait olduklarını yazdırmak için
        plt.xlabel("Date")
        plt.ylabel(str(status))
        # Grafik title
        plt.title(str(city)+" "+str(status)+" per day.")
        
        plt.legend()
        plt.show()
        
    elif ch1 == "2":
        
        ch2 = raw_input("1- Line Plot\n2- Pie Chart\n")
        
        if ch2 == "1":
            # Increase default chart size.
            figure(num=None, figsize=(16, 12))
            
            # THIS PULLS IN LIVE DATA.
            url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
            df = pd.read_csv(url)
            unique_states = df['state'].unique()
            status = raw_input("Please, select status to see deaths/cases: ")
            
            # Add base style and print out style choices.
            plt.style.use('seaborn-colorblind')
            print(plt.style.available)
            
            # Get last date to see which states have the most cases currently
            last_date = df['date'].max()
            df_last_date = df[ df['date'] == last_date]
            series_last_date = df_last_date.groupby('state')[str(status)].sum()
            # kaç tane eyaletin grafikte gözükmesini istiyorsam burasaya default bir değer giriyorum.
            series_last_date = series_last_date.nlargest(10)
            
            # Remove left and right plot lines.
            ax = plt.subplot()       
            ax.spines["right"].set_visible(False)    
            ax.spines["left"].set_visible(False)    
            # Bir başlangıç tarihi belirledim grafikte daha net gözükmeleri için
            # The chat is flat before 3/15/2020 so lets limit it to after that date.
            date_after = pd.Timestamp("03/15/2020")
            
            for state in series_last_date.index:
                df_state = df[ df['state'] == state].copy()
                df_state['date'] = pd.to_datetime(df_state['date'])
                df_state = df_state[ df_state['date'] > date_after]
            
                series_state = df_state.groupby('date')[str(status)].sum()
                series_state = series_state.diff()
                series_state.index = series_state.index.strftime('%b %d')
                plt.plot(series_state.index, series_state.values, label=state)
            
            plt.xlabel("Date")
            plt.ylabel(str(status))
            plt.title('Top 10 Covid-19 States')
            plt.grid(True)
            
            # Plot custom range for our Y axis
            plt.yticks(range(0, 12001, 1000))
            # rotate our dates.
            plt.xticks(rotation=60)
            plt.legend()
            plt.show()
        
        if ch2 == "2":
            status = raw_input("Please, select status to see deaths/cases: ")
            df = pd.read_csv(
                'https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv'
                )
            
            unique_states = df['state'].unique()
            plt.style.use("seaborn-talk")
            
            # Get last date to see which states have the most cases currently
            last_date = df['date'].max()
            df_last_date = df[ df['date'] == last_date]
            series_last_date = df_last_date.groupby('state')[str(status)].sum().sort_values(ascending=False)
            print(series_last_date)
            
            labels = []
            values = []
            # kaç tane ülkenin pie chartta olmasını istiyorsak o kadar count var,
            state_count = 6
            other_total = 0
            for state in series_last_date.index:
                if state_count > 0:
                    labels.append(state)
                    values.append(series_last_date[state])
                    state_count -= 1
                else:
                    other_total += series_last_date[state]
            #  bir de geri kalanlar için other kısmı
            labels.append("Other")
            values.append(other_total)
            
            wedge_dict = {
                'edgecolor': 'white',
                'linewidth': 2        
            }
            # pie chartımız da max değerlere sahip 6 ülke var, ülke sayısını artırıp azalarak düzenlenmeli.
            # 0.1 şekilde ayrık dilimi elde etmemizi sağladı.
            explode = (0, 0.1, 0, 0, 0, 0, 0)
            plt.pie(values, labels=labels, explode=explode, autopct='%1.1f%%', wedgeprops=wedge_dict)
            plt.show()
    elif ch1 == "e":
        print("Exiting...")
        break
    else:
        print("Invalid command")
        continue