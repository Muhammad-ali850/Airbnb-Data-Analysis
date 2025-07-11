import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:root@localhost/data")
df = pd.read_sql("SELECT * FROM all_cities", engine)

#print(df.head())
#print("Size of dataset:\n  rows  columns\n" , df.shape)
#print("We can guess the demands:\n",df["city_name"].value_counts())
#print("Name of columns:\n", df.columns)
#print("Data Types:\n", df.dtypes)
#print("Missing Values:\n", df.isnull().sum())

#with pd.option_context('display.max_columns', None, 'display.width', None):
    #print("Summary:\n\n", df.describe())

def avg_price_analys():
    avg_price = df.groupby("city_name")["price"].mean().round(2).sort_values(ascending=False)
    print("\nAverage price in $ according to", avg_price)

    #visualization
    plt.bar(avg_price.index, avg_price.values)
    plt.title("Price Analysis")
    plt.ylabel('Average $')
    plt.xlabel("City")
    plt.tight_layout()
    plt.show()

def Avail_per_RoomType_per_City():
    room_counts = df.groupby(["city_name", "room_type"]).size().unstack()
    print("\nAvailability per Room Type per City:")
    print(room_counts)

    #visualization
    room_counts.plot(kind='bar', figsize=(10, 6))
    plt.title('Availability per Room Type per City')
    plt.xlabel('City')
    plt.ylabel('Number of Listings')
    plt.grid(axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def Room_type_avg_price():
    avg_price_room = df.groupby('room_type')['price'].mean().sort_values(ascending=False)
    print("Room type average price:")
    print(avg_price_room)

    #visualization
    plt.bar(avg_price_room.index, avg_price_room.values)
    plt.title("Room_type price analysis")
    plt.ylabel('Average $')
    plt.xlabel("Room_type")
    plt.tight_layout()
    plt.show()

def Room_type_avg_price_per_city():
    avg_price_room_city = df.groupby(['city_name', 'room_type'])['price'].mean().unstack().round(2)
    print("Room type average price per city:")
    print(avg_price_room_city)

    #visualization
    avg_price_room_city.plot(kind='bar', figsize=(10, 6))
    plt.title('Room type average price per city')
    plt.xlabel('City')
    plt.ylabel('Average Price $')
    plt.grid(axis='y')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

def avg_cleanliness_analys():
    avg_cleanliness = df.groupby('city_name')['cleanliness_rating'].mean().sort_values(ascending=False)
    print("Average cleanliness rating out of 10 per city")
    print(avg_cleanliness)

    #visualization
    plt.barh(avg_cleanliness.index, avg_cleanliness.values)
    plt.title("Cleanliness analysis")
    plt.ylabel('City')
    plt.xlabel("Average Cleanliness Rating")
    plt.tight_layout()
    plt.show()

def avg_Guest_Satisfaction_analys():
    avg_guest_sat = df.groupby('city_name')['guest_satisfaction_overall'].mean().sort_values(ascending=False)
    print("Average Guest Satisfaction out of 100 per city")
    print(avg_guest_sat)

    #visualization
    plt.barh(avg_guest_sat.index, avg_guest_sat.values)
    plt.title("Guest Satisfaction analysis")
    plt.ylabel('City')
    plt.xlabel("Average Guest Satisfaction")
    plt.tight_layout()
    plt.show()

def check_correlations_with_guestSat():
    correlation = df[['price', 'guest_satisfaction_overall']].corr()
    correlation2 = df[['cleanliness_rating', 'guest_satisfaction_overall']].corr()
    correlation3 = df[['city_center_distance', 'guest_satisfaction_overall']].corr()
    correlation4 = df[['metro_distance', 'guest_satisfaction_overall']].corr()
    print(correlation, "\n", correlation2, "\n", correlation3, "\n", correlation4)

def premium_cheapest_per_city():
    print('To see the premium and cheapest according to price per city:')
    dict = df.groupby('city_name')['price']
    for city, prices in dict:
        prices_array = np.sort(prices.values)
        print("\nCity:" , city)
        print("Top 3 most expensive prices:", np.round(prices_array[-3:], 2))
        print("Bottom 3 cheapest prices:", np.round(prices_array[:3], 2))

def check_outliers_in_price():
    dict = df.groupby('city_name')['price']
    for city, prices in dict:
        prices_array = prices.values
        mean = np.mean(prices_array)
        std = np.std(prices_array)
        z_scores = (prices_array - mean) / std
        outliers = prices_array[np.abs(z_scores) > 3]
        print("\nCity:" , city)
        print("Number of price outliers:" ,len(outliers))
        if len(outliers) > 0:
            print("Outlier prices:" , outliers)

    #Calling Functions
#avg_price_analys()
#Avail_per_RoomType_per_City()
#Room_type_avg_price()
#Room_type_avg_price_per_city()
#avg_cleanliness_analys()
#avg_Guest_Satisfaction_analys()
#check_correlations_with_guestSat()
#premium_cheapest_per_city()
check_outliers_in_price()