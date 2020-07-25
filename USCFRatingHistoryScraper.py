#SS 07/24/2020
#USCFRatingsHistoryScraper
#Scrapes ratings history and dumps to pd.dataframe

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

#function to fetch current ratings 
def fetchRatingHistory(idNum):
    # Create Base URL Pointing to member rating history
    baseURL = 'https://www.uschess.org/msa/MbrDtlTnmtHst.php?'
    #idNum = '12687356' 
    URLtoFetch = baseURL + idNum
    # print(URLtoFetch) Insert validation here
    
    # Fetch Soup
    reqHTML = requests.get(URLtoFetch)
    bigsoup = BeautifulSoup(reqHTML.text, 'lxml')
    
    # Find all the pages in Tournament History, by counting them
    # Typical page: 'MbrDtlTnmtHst.php?12687356.1' = URLtoFetch.pagenumber
    # Note that 'MbrDtlTnmtHst.php?12687356' exists but is identical to 'MbrDtlTnmtHst.php?12687356.1'
    # Filter it out by requiring two "."
    linksList = bigsoup.find_all('a')
    nPgHst = 0
    for link in linksList:
        linkhref = link.get('href')
        if (linkhref.find('MbrDtlTnmtHst') > -1 and linkhref.count(".") == 2):
            nPgHst += 1 
            
    souplist = []
    for page in range(1, nPgHst+1): # integers from 1 to nPgHst
        littleURL = URLtoFetch + "." + str(page)
        littleHTML = requests.get(littleURL)
        souplist.append(BeautifulSoup(littleHTML.text, 'lxml'))
    

    ######### Everything below here needs to be replaced



    # Extract rows of the webpage that contain the Rating Data. Can find directly from the soup
    ratingRows  = soup.find_all('tr')
    
    current_df = pd.DataFrame(columns=["Rating"], index=["Regular", 
                                                         "Quick", 
                                                         "Blitz",
                                                         "Online-Regular",
                                                         "Online-Quick",
                                                         "Online-Blitz",
                                                         "Correspondence"]) #FIDE ?

        #Fill a pandas dataFrame with the interesting ratings
    for rrow in ratingRows:
        rcolumns = rrow.find_all('td')  #Many rows found are bizarre but eventually the ratings are found
        #    for column in rcolumns:
        #       print (column.get_text())
        #print ("*************************")
        #print (rcolumns[0].get_text())
        if (len(rcolumns) > 1):
            print (rcolumns[1].get_text())
            for ind in current_df.index:
                if (rcolumns[0].get_text(strip=True) == ind + " Rating"):
                    print ("W00t")
                    current_df.at[ind, "Rating"] = rcolumns[1].get_text(strip=True)

    print (current_df)


if __name__ == "__main__":
    fetchRatingHistory(sys.argv[1])
