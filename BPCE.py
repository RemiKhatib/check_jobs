#Module to look into the "mobilite" website of BPCE
#There is an API
#   https://mobilite.groupebpce.fr/nos-offres-demploi?tax_sector=digital,informatique&tax_contract=cdi&tax_place=ile-de-france&tax_brands=bpce-payment-services,bpce-sa,bpce-solutions-informatiques&external=false

##########
#Libraries
##########
import requests
import general_tools as gt
import datetime


###########################################
#Read the page associate with mobilite BPCE
###########################################
def bpce_read():

    nb_offers_max=500 #Number of offers displayed by the API

    #API call
    url = 'https://mobilite.groupebpce.fr/app/wp-json/bpce/v1/search/jobs'
    data = {
        "lang": "fr",
        "keyword": "",
        "tax_sector": "digital,informatique",
        "tax_contract": "cdi",
        "tax_place": "ile-de-france",
        "tax_job": "",
        "tax_experience": "",
        "tax_degree": "",
        "tax_brands": "bpce-payment-services,bpce-sa,bpce-solutions-informatiques",
        "tax_department": "",
        "tax_city": "",
        "tax_country": "",
        "tax_channel": "",
        "jobcode": "",
        "tax_community_job": "",
        "external": False,
        "userID": "",
        "from": 0,
        "size": nb_offers_max
    }
    #The goal is to use a test file instead of callin the website BPCE
    if not gt.DEV :
        response = requests.post(url, json=data)
    else :
        response=gt.MockResponse("bpce_test.json",200)

    #Extraction of the main information
    if response.status_code == 200:
        ljobs=[]
        jobs = response.json()
        if(jobs["data"]["total"]<=nb_offers_max):
            for job in jobs["data"]["items"]:
                ljobs.append({
                    "website" : "BPCE",
                    "id" : job["job_number"],
                    "title" : job["title"],
                    "company" : job["brand"][0],
                    "link" : "https://mobilite.groupebpce.fr"+job["link"]["url"],
                    "description" : job["description"],
                    "city" : job["localisations"][0]["city"],
                    "zipcode" : job["localisations"][0]["zipcode"],
                    "address" : job["localisations"][0]["address"],
                    "date_creation" : datetime.date.fromisoformat(job["datetime"][:10]),
                    "date_found" : datetime.date.today()
                })
            return ljobs

        #Too many answers
        else:
            print(f"Too many offers available on BPCE ({jobs["data"]["total"]}). Max limit reached ({nb_offers_max}).")
            return []

    #API problem
    else:
        gt.err_management()
        print(f"API status code: {response.status_code}.")
        return []
    
