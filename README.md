**Its role is to select all the jobs which could interest me among a list of websites**

I do not like to reveive e-mails by different websites proposing some job offers. There is nothing like RRS to manage the jobs so I have created mine.


# Usage
Run it when you want to download the last job offers. Now there is only BPCE, Banque de France and APEC (maybe more later).
It creates :
  - a database accessible with sqlite (table job_offers).
    With other tools (using SQL), you can use it to check the offers you have read, check the offers to apply and when you send an application.
  - a html file where you will see 2 tables :
    - The jobs you should shoukd check and the jobs you should apply
    - The jobs you applied


# How to install and use it ?
On linux, use makefile :
#### Virtual environment creation
```make venv```
#### Installation
```make install```
#### Run the programm
```make run```

or

```.venv/bin/python3 -m src.check_jobs ```
#### Clean the virtual environment and the compiled files
```make clean```
#### List all the targets of the makefile
```make help```


# List of modules
#### ./src/check_jobs.py
Main script which calls all the others. As mentionned, it allows you to get all the jobs you want to check.
#### ./src/{apec.py,bdf.py,bpce.py}
Modules associated with the scrapping of the websites.
#### ./src/general_tools.py
Module which contains general tools which can be reused anytime.
#### ./src/table.py
Module with everything about database.
#### ./config.py
Configuration file. The main parameters are :
  - MONTHS_NOT_APPLIED : Delete time in month before a purge if I did not applied to a job.
  - YEARS_APPLIED : Delete time in year before a purge if I applied to a job


# Future developments
  - Add extra websites to check :
    - [ ] BNPP : javascript output. A new type of module has to be created.
    - [ ] SG : php output. A new type of module has to be created.
    - [ ] CB : only 1 offer
    - [ ] VISA Nothing in France
    - [ ] EPI : HTML output. No offer for me right now.
    - [ ] CA : Nothing now
    - [ ] Crédit mutuel : No
    - [ ] LCL : No

**This program has been created by Remi Khatib**
