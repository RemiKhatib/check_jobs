#Module to look into the "mobilite" website of the APEC
#There is an API
#   https://www.apec.fr/cms/webservices/rechercheOffre

##########
#Libraries
##########
import config
from . import general_tools as gt

import requests
import datetime


###########################################
#Read the page associate with mobilite APEC
###########################################
def read():

    today=datetime.date.today()
    #API call
    url = 'https://www.apec.fr/cms/webservices/rechercheOffre'
    data = {
            "lieux":["711"],
            "fonctions":["101833"],
            "statutPoste":[],
            "typesContrat":["101888"],
            "typesConvention":["143684"],
            "niveauxExperience":[],
            "idsEtablissement":[],
            "secteursActivite":[],
            "typesTeletravail":[],
            "idNomZonesDeplacement":[],
            "positionNumbersExcluded":[],
            "typeClient":"CADRE",
            "sorts":[{"type":"DATE","direction":"DESCENDING"}],
            "pagination":{"range":config.NB_OFFERS_MAX,"startIndex":0},
            "activeFiltre":True,
            "pointGeolocDeReference":{"distance":0},
            "salaireMinimum":"60",
            "salaireMaximum":"200",
            "motsCles":"banque"
        }
    #The goal is to use a test file instead of calling the website APEC
    if not config.DEV :
        response = requests.post(url, json=data)
    else :
        response=gt.MockResponse("tests/apec_test.json",200)

    #Extraction of the main information
    if response.status_code == 200:
        ljobs=[]
        jobs = response.json()
        if(jobs["totalCount"]<=config.NB_OFFERS_MAX):
            for job in jobs["resultats"]:
                ljobs.append({
                    "website"       : "APEC",
                    "id"            : job["numeroOffre"],
                    "company"       : job.get("nomCommercial",""), #Sometimes does not exist
                    "title"         : job["intitule"],
                    "link"          : "https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/"+job["numeroOffre"],
                    "city"          : "",
                    "zipcode"       : "",
                    "address"       : "",
                    "date_creation" : datetime.date.fromisoformat(job["datePublication"][:10]),
                    "date_found"    : today,
                    "last_update"   : today
                })
            return ljobs

        #Too many answers
        else:
            print(f"Too many offers available on APEC ({jobs["totalCount"]}). Max limit reached ({config.NB_OFFERS_MAX}).")
            return []

    #API problem
    else:
        gt.err_management()
        print(f"API status code: {response.status_code}.")
        return []
    
if __name__=="__main__":
    jobs=read()
    for job in jobs:
        print(job)