from flask import Flask, jsonify, request, json
import requests

app = Flask(__name__)

# retornar 200
@app.route('/')
def hello_world():
    return 'Hello world!'

# id do pokemon
@app.route('/<POKEMON>', methods=['GET'])
def getPokeId(POKEMON):
    poke = POKEMON.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{poke}"

    response = requests.get(url)
    pokemon_data = response.json()
    return {
        "id": pokemon_data['id']
    }

# tamanho do nome
@app.route('/name_length/<POKEMON>', methods=['GET'])
def getPokeNameLength(POKEMON):
    poke = POKEMON.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{poke}"

    response = requests.get(url)
    pokemon_data = response.json()
    return {
        "name_length": len(pokemon_data['name'])
    }

# contar vogais no nome
@app.route('/vowel_count/<POKEMON>', methods=['GET'])
def getPokeNameVowelCount(POKEMON):
    poke = POKEMON.lower()
    url = f"https://pokeapi.co/api/v2/pokemon/{poke}"

    response = requests.get(url)
    pokemon_data = response.json()
    vowelcount = 0
    for char in pokemon_data['name']:
        vowel = ['a','e','i','o','u']
        if char in vowel:
            vowelcount += 1
    return {
        "vowel_count": vowelcount
    }

# cor, teste de post & body request
@app.route('/color', methods=['POST'])
def getPokemonColor():
    # handle the POST request
    if request.method == 'POST':
        data = json.loads(request.data)
        poke_id = str(data['pokemon_id']).lower()
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}/"
        species_response = requests.get(species_url)
        species_pokemon_data = species_response.json()

        return {
            "name": species_pokemon_data['name'],
            "id": species_pokemon_data['id'],
            "base_happiness": species_pokemon_data['base_happiness'],
            "color": species_pokemon_data['color']['name']
        }

# geração
@app.route('/generation', methods=['POST'])
def getPokemonGeneration():
    # handle the POST request
    if request.method == 'POST':
        data = json.loads(request.data)
        poke_id = str(data['pokemon_id']).lower()
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}/"
        species_response = requests.get(species_url)
        species_pokemon_data = species_response.json()
        return {
            "name": species_pokemon_data['name'],
            "id": species_pokemon_data['id'],
            "base_happiness": species_pokemon_data['base_happiness'],
            "generation": species_pokemon_data['generation']['name']
        }

@app.route('/name', methods=['POST'])
def getPokemonJAName():
    # handle the POST request
    if request.method == 'POST':
        data = json.loads(request.data)
        poke_id = str(data['pokemon_id']).lower()
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{poke_id}/"
        species_response = requests.get(species_url)
        species_pokemon_data = species_response.json()
        # args - lingua de index 0 até 10
        args = request.args
        arglanguage = args.get('language', default="ja", type=str)
        arglanguage = arglanguage.lower()
        language = None
        match arglanguage:
            case "ja-hrkt":
                language = 0
            case "roomaji":
                language = 1
            case "ko":
                language = 2
            case "zh-hant":
                language = 3
            case "fr":
                language = 4
            case "de":
                language = 5
            case "es":
                language = 6
            case "it":
                language = 7
            case "en":
                language = 8
            case "ja":
                language = 9
            case "zh-hans":
                language = 10
            case _:
                arglanguage = "ja"
                language = 9
        return {
            "name": species_pokemon_data['name'],
            "id": species_pokemon_data['id'],
            "base_happiness": species_pokemon_data['base_happiness'],
            f"name_{arglanguage}": species_pokemon_data['names'][language]['name']
        }

if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=5000)