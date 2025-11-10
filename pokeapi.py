import requests
import time

# Función auxiliar para manejar peticiones HTTP con control de errores
def get_data(url):
    try:
        res = requests.get(url)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return None

print("=== CLASIFICACIÓN POR TIPOS ===")

# a) ¿Cuántos Pokémon de tipo fuego existen en la región de Kanto?
fire_type = get_data("https://pokeapi.co/api/v2/type/fire")
fire_pokemon = fire_type["pokemon"]
fire_kanto = [p["pokemon"]["name"] for p in fire_pokemon if int(p["pokemon"]["url"].split("/")[-2]) <= 151]
print(f"Pokémon tipo fuego en Kanto: {len(fire_kanto)} → {fire_kanto}\n")

# b) Pokémon tipo agua con altura > 10
water_type = get_data("https://pokeapi.co/api/v2/type/water")
water_pokemon = water_type["pokemon"]
water_tall = []
for p in water_pokemon:
    data = get_data(p["pokemon"]["url"])
    if data and data["height"] > 10:
        water_tall.append(data["name"])
print(f"Pokémon tipo agua con altura > 10: {water_tall}\n")

print("=== EVOLUCIONES ===")

# a) Cadena evolutiva completa de un Pokémon inicial (ejemplo: Bulbasaur)
bulbasaur_species = get_data("https://pokeapi.co/api/v2/pokemon-species/1/")
evo_chain_url = bulbasaur_species["evolution_chain"]["url"]
evo_chain = get_data(evo_chain_url)

def get_evolution_chain(chain):
    evo_list = [chain["species"]["name"]]
    while chain["evolves_to"]:
        chain = chain["evolves_to"][0]
        evo_list.append(chain["species"]["name"])
    return evo_list

bulbasaur_chain = get_evolution_chain(evo_chain["chain"])
print(f"Cadena evolutiva de Bulbasaur: {' → '.join(bulbasaur_chain)}\n")

# b) Pokémon eléctricos sin evolución
electric_type = get_data("https://pokeapi.co/api/v2/type/electric")
electric_pokemon = electric_type["pokemon"]
no_evo_electric = []
for p in electric_pokemon:
    species = get_data(f"https://pokeapi.co/api/v2/pokemon-species/{p['pokemon']['name']}")
    if species and not species["evolves_from_species"]:
        evo_chain = get_data(species["evolution_chain"]["url"])
        if evo_chain and evo_chain["chain"]["species"]["name"] == species["name"] and not evo_chain["chain"]["evolves_to"]:
            no_evo_electric.append(species["name"])
print(f"Pokémon eléctricos sin evolución: {no_evo_electric}\n")

print("=== ESTADÍSTICAS DE BATALLA ===")

# a) Pokémon con mayor ataque base en la región de Johto (Pokémon #152–251)
max_attack = 0
best_pokemon = None
for i in range(152, 252):
    data = get_data(f"https://pokeapi.co/api/v2/pokemon/{i}/")
    if not data:
        continue
    attack = next(stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] == "attack")
    if attack > max_attack:
        max_attack = attack
        best_pokemon = data["name"]
print(f"Pokémon con mayor ataque en Johto: {best_pokemon} ({max_attack})\n")

# b) Pokémon con la mayor velocidad que no sea legendario
max_speed = 0
fastest = None
for i in range(1, 899):
    data = get_data(f"https://pokeapi.co/api/v2/pokemon/{i}/")
    if not data:
        continue
    species = get_data(f"https://pokeapi.co/api/v2/pokemon-species/{i}/")
    if not species or species["is_legendary"]:
        continue
    speed = next(stat["base_stat"] for stat in data["stats"] if stat["stat"]["name"] ==_]()
