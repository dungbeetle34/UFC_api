**UFC API**

An API that returns information about current fighters across all weight divisions. 
The only supported format is JSON
The data is scraped from 'https://www.itnwwe.com/mma/ufc-fighters-roster/' and put into a SQLITE3 database

(Currently creating a frontend interface)

**Getting Started**

Make sure you have Flask installed. 
If not, no worries... paste in the code below
```
pip install flask
```
Download the requirements.txt using the command below
```
pip install -r requirements.txt
```
Run [api.py] and head to the localhost it is running on.

**Using the API**

Protocol and server name is the localhost the Flask application is running on
I am only including the URL paths and parameters in the following examples.

The entire list of fighters:
    /api/v1/resources/fighters/all

The only supported parameter thus far is the name of fighters (case-sensitive):
    /api/v1/resources/fighters?name=[]
    
    Replace the '[]' with the fighter name. If the fighter has a first and last name, append them with a '+'
    i.e. /api/v1/resources/fighters?name=Conor+McGregor
