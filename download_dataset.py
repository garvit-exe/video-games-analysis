import requests
import os

def download_dataset():
    url = "https://raw.githubusercontent.com/GregorUT/vgchartzScrape/master/Video_Games_Sales_as_at_22_Dec_2016.csv"
    response = requests.get(url)
    
    if response.status_code == 200:
        with open("vgsales.csv", "wb") as f:
            f.write(response.content)
        print("Dataset downloaded successfully!")
    else:
        print("Failed to download dataset")

if __name__ == "__main__":
    download_dataset()
