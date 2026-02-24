# This is a simple little data visualization script that I made as practice to learn more about data analytics/engieering.
# It downloads a dataset from the Kaggle API, does simple processing on it to get some averages, then plots them.
# The dataset itself seems quite flawed, as I noticed mismatches between the "country" and "region" attributes in many rows.
# Therefore, the resulting plot is not very accurate, but this was just practice and a learning experience.
# The dataset and its description can be found here: https://www.kaggle.com/datasets/hassanjameelahmed/price-of-healthy-diet-clean
import pandas as pd
import matplotlib.pyplot as plt
import kagglehub
from kagglehub import KaggleDatasetAdapter

# takes a df and a continent name, and returns a new df with
# the average cost of a healthy diet for each year in the continent
def create_continent_df(df, continent):
    #create a smaller df so we don't have query the entire thing every time
    continent_data = df.query("region == @continent", inplace=False)
    year = 2017
    data_dict = {"year": [], "avg": []}
    while year <= 2024:
        # filter for the specific year, and then count the average price for the year
        # by dividing the sum of the column values with the number of non-null values in the column
        year_data = continent_data.query("year == @year", inplace=False)
        sum = year_data['cost_healthy_diet_ppp_usd'].sum()
        value_count = year_data['cost_healthy_diet_ppp_usd'].count()
        if value_count > 0:
            average = sum / value_count
            data_dict["avg"].append(average)
            data_dict["year"].append(year)
        year = year + 1
    
    return pd.DataFrame.from_dict(data_dict)

def main():
    # Download the dataset from Kaggle API
    path = kagglehub.dataset_download("hassanjameelahmed/price-of-healthy-diet-clean")
    print("Path to dataset files:", path)

    #load a pandas dataframe from the dataset
    base_df = kagglehub.dataset_load(KaggleDatasetAdapter.PANDAS, 
                                "hassanjameelahmed/price-of-healthy-diet-clean", 
                                 "price_of_healthy_diet_clean.csv"
    )
    # create the data for each continent
    africa_data = create_continent_df(base_df, "Africa")
    europe_data = create_continent_df(base_df, "Europe")
    asia_data = create_continent_df(base_df, "Asia")
    americas_data = create_continent_df(base_df, "Americas")

    # plot the data 
    fig, ax = plt.subplots()
    ax.plot(africa_data["year"], africa_data["avg"], label="Africa")
    ax.plot(europe_data["year"], europe_data["avg"], label="Europe")
    ax.plot(asia_data["year"], asia_data["avg"], label="Asia")
    ax.plot(americas_data["year"], americas_data["avg"], label="Americas")

    ax.set_xlabel("Year")
    ax.set_ylabel("Average Cost of Healthy Diet (USD PPP)")
    ax.set_title("Average Cost of Healthy Diet by region")
    ax.legend()
    plt.show()

if __name__=="__main__":
    main()