**This program has been written by Rémi Khatib.
Its role is to select all the jobs which could interest me among a list of websites**

# Work in progress
# Plan :
1. Check for the API of the websites. => OK for BPCE

2. Make one module per website => OK for BPCE

3. Store everything in a database. The table should contain : 
  - website : website where the offer wwas found
  - id ; Id of the job
  - title : title of the job
  - date_creation : date creation of the offer
  - company : company proposing the job
  - link : link
  - description : description
  - city : Name of the city
  - zipcode : zip code of the city
  - address : Street
  - date_found : date when the script ran

4. Define the list of websites. Create the rules to respect during the search. At each run, it should avoid duplicates.

5. Create a database

6. Make the python requierements.txt "pip freeze > requirements.txt"