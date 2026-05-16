#Module to look into the "mobilite" website of the Banque de France
#There is an API
#   https://bdf.wd103.myworkdayjobs.com/wday/cxs/bdf/recrutement-banque-de-France/jobs

##########
#Libraries
##########
import requests
import general_tools as gt
import datetime


##########################################
#Read the page associate with mobilite BDF
##########################################
def bdf_read():

    nb_offers_max=total=500 #Number maximal of offers displayed by the API
    offset=0 #Offset to check all the pages
    limit=20 #Maximal number of jobs displayed per page

    #It is not possible to have more than 20 resultats per page
    ljobs=[]
    while offset<total :
        #API call
        url = 'https://bdf.wd103.myworkdayjobs.com/wday/cxs/bdf/recrutement-banque-de-France/jobs'
        data = {
            "appliedFacets":{
                "locations":["f4195605335b100201863e0a2a950000","d1f36ec1bc921000cf220a60387b0000"],
                "jobFamilyGroup":["58643cc75552100108ae9c11fadc0000","58643cc75552100108ae8bdbe9810000","58643cc75552100108ae94ddf7250000","58643cc75552100108ae810b7be90000","58643cc75552100108ae991176d70000","58643cc75552100108ae931086500000"],
                "workerSubType":["f4195605335b1001a416b00be4f80000"]
                },
            "limit":limit,
            "offset":offset,
            "searchText":""
        }
        #The goal is to use a test file instead of calling the website BDF
        if not gt.DEV :
            response = requests.post(url, json=data)
        else :
            response=gt.MockResponse("bdf_test.json",200)
        
        #Extraction of the main information
        if response.status_code == 200:
            jobs = response.json()
            total=jobs["total"]
            offset+=limit

            if(jobs["total"]<=nb_offers_max):
                for job in jobs["jobPostings"]:
                    resp_detail=requests.get("https://bdf.wd103.myworkdayjobs.com/wday/cxs/bdf/recrutement-banque-de-France"+job["externalPath"])
                    detail=resp_detail.json()

                    if resp_detail.status_code == 200:
                        ljobs.append({
                            "website"       : "BdF",
                            "id"            : detail["jobPostingInfo"]["jobReqId"],
                            "company"       : detail["hiringOrganization"]["name"],
                            "title"         : detail["jobPostingInfo"]["title"],
                            "link"          : detail["jobPostingInfo"]["externalUrl"],
                            "city"          : detail["jobPostingInfo"]["location"],
                            "zipcode"       : "",
                            "address"       : detail["jobPostingInfo"]["jobRequisitionLocation"]["descriptor"],
                            "date_creation" : datetime.date.fromisoformat(detail["jobPostingInfo"]["startDate"]),
                            "date_found"    : datetime.date.today()
                        })

                    #API problem
                    else:
                        gt.err_management()
                        print(f"API status code: {response.status_code}.")
                        return []

            #Too many answers
            else:
                print(f"Too many offers available on BPCE ({jobs["data"]["total"]}). Max limit reached ({nb_offers_max}).")
                return []

        #API problem
        else:
            gt.err_management()
            print(f"API status code: {response.status_code}.")
            return []

    return ljobs

    
