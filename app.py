from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# retornar 200
@app.route('/')
def hello_world():
    return '''
    <a href="/color">Color</a><br>
    <a href="/generation">Generation</a><br>
    <a href="/name">Name</a>
    '''

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
@app.route('/color', methods=['GET', 'POST'])
def getPokemonColor():
    # handle the POST request
    if request.method == 'POST':
        POKEMON_ID = request.form.get('POKEMON_ID')
        POKEMON_ID = POKEMON_ID.lower()
        # pokemon-species
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{POKEMON_ID}/"
        species_response = requests.get(species_url)
        species_pokemon_data = species_response.json()
        return {
            "name": species_pokemon_data['name'],
            "id": species_pokemon_data['id'],
            "base_happiness": species_pokemon_data['base_happiness'],
            "color": species_pokemon_data['color']['name']
        }
    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Pokemon-ID: <input type="text" name="POKEMON_ID"></label></div>
               <input type="submit" value="Submit">
           </form>'''

# geração
@app.route('/generation', methods=['GET', 'POST'])
def getPokemonGeneration():
    # handle the POST request
    if request.method == 'POST':
        POKEMON_ID = request.form.get('POKEMON_ID')
        POKEMON_ID = POKEMON_ID.lower()
        # pokemon-species
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{POKEMON_ID}/"
        species_response = requests.get(species_url)
        species_pokemon_data = species_response.json()
        return {
            "name": species_pokemon_data['name'],
            "id": species_pokemon_data['id'],
            "base_happiness": species_pokemon_data['base_happiness'],
            "generation": species_pokemon_data['generation']['name']
        }
    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Pokemon-ID: <input type="text" name="POKEMON_ID"></label></div>
               <input type="submit" value="Submit">
           </form>'''

@app.route('/name', methods=['GET', 'POST'])
def getPokemonJAName():
    # handle the POST request
    if request.method == 'POST':
        POKEMON_ID = request.form.get('POKEMON_ID')
        POKEMON_ID = POKEMON_ID.lower()
        # pokemon-species
        species_url = f"https://pokeapi.co/api/v2/pokemon-species/{POKEMON_ID}/"
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
    # otherwise handle the GET request
    return '''
           <form method="POST">
               <div><label>Pokemon-ID: <input type="text" name="POKEMON_ID"></label></div>
               <input type="submit" value="Submit">
           </form>'''

if __name__ == '__main__':
    app.run(debug=True)