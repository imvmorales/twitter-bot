import tweepy
import requests
from JogoDaVelha.infos import c_id, secret, consumer_key, consumer_secret, consumer_access_token, access_token_secret


# conseguir um token de acesso
def access_token(id, secret):
    import pybase64
    client_creds = f"{id}:{secret}"
    client_creds_b64 = pybase64.b64encode(client_creds.encode())

    token_url = "https://accounts.spotify.com/api/token"
    method = "POST"
    token_data = {
        "grant_type": "client_credentials"
    }
    token_headers = {
        "Authorization": f"Basic {client_creds_b64.decode()}"
    }

    r = requests.post(token_url, data=token_data, headers=token_headers)
    token_response_data = r.json()
    return token_response_data['access_token']


# usar o token de acesso para conseguir o id do artista
def artist_id():
    headers = {
        "Authorization": f"Bearer {access_token(client_id, client_secret)}"
    }
    endpoint = "https://api.spotify.com/v1/search"
    data = "q=ArianaGrande&type=artist"

    lookup_url = f"{endpoint}?{data}"
    r = requests.get(lookup_url, headers=headers)
    artist_id_aux = r.json()['artists']['items']
    return artist_id_aux[0]['id']


# usar o token de acesso para conseguir os albuns do artista
def last_album():
    headers = {
        "Authorization": f"Bearer {access_token(client_id, client_secret)}"
    }
    endpoint = f"https://api.spotify.com/v1/artists/{artist_id()}/albums"
    data = "include_groups=album"

    lookup_url = f"{endpoint}?{data}"
    r = requests.get(lookup_url, headers=headers)
    aux = r.json()

    del aux['href']
    return aux['items']


# nome do último álbum
def name():
    return last_album()[2]['name']


# data de lançamento do último álbum
def release_date():
    return last_album()[2]['release_date']


def dias():
    import datetime
    hoje = datetime.date.today()
    album = datetime.datetime.strptime(release_date(), '%Y-%m-%d').date()
    d = hoje - album
    return d.days


def _main_():
    if name() == 'Positions':
        try:
            tweet = api.create_tweet(text=f'{dias()} days')
            print('Tweet enviado com sucesso!')
        except:
            print("Algo deu errado!")
    else:
        print('Ariana released an album')


client_id = c_id()
client_secret = secret()

# informar as chaves para acessar a conta
api = tweepy.Client(
    consumer_key=f'{consumer_key()}',
    consumer_secret=f'{consumer_secret()}',
    access_token=f'{consumer_access_token()}',
    access_token_secret=f'{access_token_secret()}'
)

_main_()
