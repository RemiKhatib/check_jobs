**This program has been written by Rémi Khatib.
Its role is to select all the jobs which could interest me among a list of websites**

# Work in progress
# Plan :
1. [] Store every offer in database. The table should contain : 
  - website : website where the offer wwas found
  - id ; Id of the job
  - company : company proposing the job
  - title : title of the job
  - link : link
  - city : Name of the city
  - zipcode : zip code of the city
  - address : Street
  - date_creation : date creation of the offer
  - date_found : date when the script ran
  - check : Do I have checked this offer ?
  - to_apply : job to apply
  - date_applied : application date

2. [] Define the list of websites. Check all the API
  - BPCE OK
  - BdF OK
  - VISA Nothing in France
  - CB : ???
  - BNPP : output Javascript. To analyse nicely.
  - CA : Nothing now
  - Crédit mutuel : ?????
  - APEC : https://www.apec.fr/cms/webservices/rechercheOffre
  - EPI : ???
  - LCL : ???

3. [] Create a database => OK

4. [] Delete the jobs which do not appear anymore in the extraction.

5. [] Make the python requierements.txt "pip freeze > requirements.txt"