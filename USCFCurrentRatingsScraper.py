#SS 07/18/2020
#USCFCurrentRatingsScraper
#Scrapes current ratings page and dumps to pd.dataframe

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

#function to fetch current ratings 
def fetchCurrentRatings(idNum):
    # Create Base URL Pointing to member mainpage
    baseURL = 'https://www.uschess.org/msa/MbrDtlMain.php?'
    #idNum = '12687356' 
    URLtoFetch = baseURL + idNum
    # print(URLtoFetch) Insert validation here
    
    # Fetch Soup
    reqHTML = requests.get(URLtoFetch)
    soup = BeautifulSoup(reqHTML.text, 'lxml')
    
    # Tables are too nested for soup to find one containing just the ratings
    #ratingTable = soup.find_all('table')[2]
    
    # Extract rows of the webpage that contain the Rating Data. Can find directly from the soup
    ratingRows  = soup.find_all('tr')
    
    current_df = pd.DataFrame(columns=["Rating"], index=["Regular", 
                                                         "Quick", 
                                                         "Blitz",
                                                         "Online-Regular",
                                                         "Online-Quick",
                                                         "Online-Blitz",
                                                         "Correspondence"]) #FIDE ?

    #X#X#X#X#X#X#X Find the column with the relevant rating info
    #Fill a pandas dataFrame with the interesting ratings
    for rrow in ratingRows:
        rcolumns = rrow.find_all('td')  #Many rows found are bizarre but eventually the ratings are found
        #    for column in rcolumns:
        #       print (column.get_text())
        print ("*************************")
        print (rcolumns[0].get_text())
        if (len(rcolumns) > 1):
            print (rcolumns[1].get_text())
            for ind in current_df.index:
                #Identify Rows with the desired ratings by matching name of rating
                if (rcolumns[0].get_text(strip=True) == ind + " Rating"): 
                    #print ("W00t")
                    current_df.at[ind, "Rating"] = rcolumns[1].get_text(strip=True) #Store the rating in it's matching df row

    print (current_df)


if __name__ == "__main__":
    fetchCurrentRatings(sys.argv[1])
