import requests, bs4

az_page_url = "https://library.calvin.edu/content/resource_abstract/c_54/"
page_ids = ['?startnum=51','?startnum=101','?startnum=151','?startnum=201','?startnum=251']
db_name_to_url_dict = {}
final_description_lists = []

def retrieveDescription(url, url_id=""):
    # get the information from the webpage and all the descriptions from page 1
        res = requests.get(url + url_id)
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        all_description = soup.select('.rr_summaryrow td')

        # get the description summary and add to your final list
        for summaryDescription in all_description:
            
            #remove any paragraph formation in the string and remove link text
            aSummary = " ".join(summaryDescription.getText().split())
            final_description_lists.append(aSummary.replace("Read the full annotation", ""))
            

def getDescriptions():
    #for firstpage only
    retrieveDescription(az_page_url) 
    
    #for subsequent pages
    for page_id in page_ids:
        retrieveDescription(az_page_url, page_id)


def retrieveDatabaseNamesAndLinks(url, url_id=""):
    res = requests.get(url + url_id)
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    all_db_names = soup.select('td h4')

    for db_name_tag in all_db_names:
        
        # get and format the database name
        unformatted_db_name = db_name_tag.getText()
        formatted_db_name = " ".join(unformatted_db_name.split())
        
        # outliers with no links
        if (len(db_name_tag.select('a')) == 0):
            continue
        
        # get the database actual link and pair it to the database name
        db_link = db_name_tag.select('a')[0]['href']
        db_name_to_url_dict[formatted_db_name] = db_link
        
       
def getDbNamesAndLinks():
    retrieveDatabaseNamesAndLinks(az_page_url)
    for page_id in page_ids:
        retrieveDatabaseNamesAndLinks(az_page_url, page_id)
        

def saveDescriptionsToFile(summaryDescriptions):
    with open ("descriptions.txt", "w") as file:
        for descr in summaryDescriptions:
            file.write(descr + "\n")


def saveDbNameAndLinksToFile(name_link_map):
    with open ("dbNamesAndLinks.txt", "w") as file:
        for dbName, dbLink in name_link_map.items():
            file.write("{}:{}\n".format(dbName, dbLink))



if __name__ == "__main__":
   getDbNamesAndLinks()
   saveDbNameAndLinksToFile(db_name_to_url_dict) 
    
