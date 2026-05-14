#Module to look into the "mobilite" website of BPCE
#There is an API
#   https://mobilite.groupebpce.fr/nos-offres-demploi?tax_sector=digital,informatique&tax_contract=cdi&tax_place=ile-de-france&tax_brands=bpce-payment-services,bpce-sa,bpce-solutions-informatiques&external=false

##########
#Libraries
##########
import requests
import general_tools as gt


###########################################
#Read the page associate with mobilite BPCE
###########################################
def bpce_read():
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
        "size": 9
    }
#XXX To uncomment : The goal is to use a test file instead of callin the website BPCE
#    response = requests.post(url, json=data)
    response=gt.MockResponse("bpce_test.json",200)

    #Generation of the response
    if response.status_code == 200:
        jobs = response.json()
        for job in jobs:
            print(f"{job} : {jobs[job]}")


        #XXX Travail work Arbeit : Get the list of jobs
        for job in jobs:
            print(job)
    else:
        gt.err_management()
        print(f"API status code: {response.status_code}.")
    

########################################
#Extraction of the important information
########################################
def bpce_extract():
    pass