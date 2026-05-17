#Module to look into the "mobilite" website of the APEC
#There is an API
#   https://www.apec.fr/cms/webservices/rechercheOffre

##########
#Libraries
##########
import requests
import general_tools as gt
import datetime


###########################################
#Read the page associate with mobilite APEC
###########################################
def read():

    nb_offers_max=500 #Number of offers displayed by the API

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
            "pagination":{"range":nb_offers_max,"startIndex":0},
            "activeFiltre":True,
            "pointGeolocDeReference":{"distance":0},
            "salaireMinimum":"60",
            "salaireMaximum":"200",
            "motsCles":"banque"
        }
    #The goal is to use a test file instead of calling the website BPCE
    if not gt.DEV :
        response = requests.post(url, json=data)
    else :
        response=gt.MockResponse("APEC_test.json",200)

    #Extraction of the main information
    if response.status_code == 200:
        ljobs=[]
        jobs = response.json()
        if(jobs["totalCount"]<=nb_offers_max):
            for job in jobs["resultats"]:
                ljobs.append({
                    "website" : "APEC",
                    "id" : job["numeroOffre"],
                    "company" : job.get("nomCommercial",""), #Sometimes does not exist
                    "title" : job["intitule"],
                    "link" : "https://www.apec.fr/candidat/recherche-emploi.html/emploi/detail-offre/"+job["numeroOffre"],
                    "city" : "",
                    "zipcode" : "",
                    "address" : "",
                    "date_creation" : datetime.date.fromisoformat(job["datePublication"][:10]),
                    "date_found" : datetime.date.today()
                })
            return ljobs

        #Too many answers
        else:
            print(f"Too many offers available on APEC ({jobs["totalCount"]}). Max limit reached ({nb_offers_max}).")
            return []

    #API problem
    else:
        gt.err_management()
        print(f"API status code: {response.status_code}.")
        return []
    
