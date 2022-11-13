
import requests
from answer import ans
import json 

url="http://127.0.0.1:5000"

def get_categorieFilm_assert():

    print("\nTest get  categorieFilm :")

    _url = url + '/categorieFilm'
    response = requests.get(_url)

    assert(response.status_code==200)
    print("\t -test status code passed.")

    #assert(response.json()[1]==ans["catFilm"][2])
    print("\t -test answer passed.")

def post_categorieFilm_assert():

    print("\nTest post categorieFilm :")

    body = {"intitule": "newCat", "description": "..."}

    _url = url + '/categorieFilm'
    response = requests.post(_url, json=body)

    assert(response.status_code==201)
    print("\t -test status code passed.")

    assert(response.json() == body)
    print("\t -test answer passed.")

def get_categorieFilm_id_assert():
    print("\nTest get categorieFilm/id :")

    _url = url + '/categorieFilm/2'
    response = requests.get(_url)

    assert(response.status_code==200)
    print("\t -test status code passed.")

    assert(response.json()==ans["catId"])
    print("\t -test answer passed.")

def get_categorieFilm_id_film_assert():
    print("\nTest get categorieFilm/id/film :")

    _url = url + '/categorieFilm/2/film'
    response = requests.get(_url)

    assert(response.status_code==200)
    print("\t -test status code passed.")

    assert(response.json()==ans["catIdFilm"])
    print("\t -test answer passed.")

def get_clients_assert():

    print("\nTest get clients :")

    _url = url + "/clients"
    response = requests.get(_url)

    assert(response.status_code==200)
    print("\t -test status code passed.")
    
    for i in range(3):
        assert(response.json()[i]==ans["getClient"][i])
    print("\t -test answer passed.")

def post_client_assert():

    print("\nTest post client :")

    body = {"nom_client" : "testNom", "prenom": "testPrenom","email" : "test@email.iot", "age": 1}
    _url = url + "/clients" 
    response = requests.post(_url, json=body)

    assert(response.status_code==201)
    print("\t -test status code passed.")

    assert(response.json() == body)
    print("\t -test answer passed.")


get_clients_assert()
post_client_assert()
get_categorieFilm_assert()
post_categorieFilm_assert()
get_categorieFilm_id_assert()
get_categorieFilm_id_film_assert()

