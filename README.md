**This program has been written by Rémi Khatib.
Its role is to select all the jobs which could interest me among a list of websites**

# How to use it ?
Run it when you want to download the last job offers (now only BPCE, Banque de France and APEC).
It will create :
  - a database accessible with sqlite (table job_offers)
  - a html file where you will see 2 tables (the jobs you should check or recheck ; the jobs you applied)
The basic information about the jobs are displayed on the html page. Then you can tell if any offer interst you and when you candidated (using SQL).


# Work in progress
# Plan :
[] Define the list of websites. Check all the API
  - BPCE OK
  - BdF OK
  - APEC : OK
  - VISA Nothing in France
  - CB : Only 1 offer.
  - EPI : output HTML. No offer right now. To analyse nicely.
  - BNPP : output Javascript. To analyse nicely.
  - SG : php. To analyse nicely.
  - CA : Nothing now
  - Crédit mutuel : No
  - LCL : No
 
[] Make the python requierements.txt "pip freeze > requirements.txt"

[] Make the documentation

[] Control the number of records returned by apec.py