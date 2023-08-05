# Webservice Stash

A PyPI packages that supports all the necessary error codes, validation exception, common exceptions of a webservice. This PyPI package includes a method that establishes the connection to your firebase account.

## Installation

Run the following to install:

```cmd
pip install stash-service
```

## Usage

#### Connect to Firestore with key

A connection can be established easily with your Firestore account. This method receives two mandatory parameters. The first string parameters receives your collection name of the Firestore database and the second string or dictionary parameter will receive your firestore account's secret key.

```python
from stash_service import connect_firestore_with_key

db_reference = connect_firestore_with_key(collection_name, firestore_secret_key)
```

## Response codes description
##### HTTP response status codes indicate whether a specific HTTP request has been successfully completed.
All HTTP response status codes are separated into five classes or categories. The first digit of the status code defines the class of response,
while the last two digits do not have any classifying or categorization role.
> ###### 1xx informational response – the request was received, continuing process.
       An informational response indicates that the request was received and understood. 
> ###### 2xx successful – the request was successfully received, understood, and accepted.
       This class of status codes indicates the action requested by the client was received, understood, and accepted.
> ###### 3xx redirection – further action needs to be taken in order to complete the request.
       This class of status code indicates the client must take additional action to complete the request. 
> ###### 4xx client error – the request contains bad syntax or cannot be fulfilled.
       This class of status code is intended for situations in which the error seems to have been caused by the client.
> ###### 5xx server error – the server failed to fulfil an apparently valid request.
       Response status codes beginning with the digit "5" indicate cases in which the server is aware that it has encountered an error or is otherwise incapable of performing the request.

## App_Exception code description

The App_Exception is a class which will inherit the properties of Class Exception.
The method __init__  will check your program with the conditions and check whether it contains error or not.
If the condition satisfies then the method "response" will be called which will give the required exception(error description). 
##### The function "get_env" will retrieve values of your environment variables of your program.

---

MIT Licensed - 2021 : Britsa - britsa.tech@gmail.com

Contributors:
Maria Irudaya Regilan J, Pavithra K, Venkateshwar S, D Vidhyalakshmi

---
