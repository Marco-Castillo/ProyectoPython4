import requests
import os
import json
from tkinter import Tk, Label, Frame
from PIL import Image, ImageTk
from io import BytesIO


def pokemon(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"{nombre.capitalize()} no encontrado")
        return None


def pokeinf(datoPokemon):
    nombre = datoPokemon['name']
    peso = datoPokemon['weight']
    altura = datoPokemon['height']
    habilidades = [habilidad['ability']['name'] for habilidad in datoPokemon['abilities']]
    tipos = [tipo['type']['name'] for tipo in datoPokemon['types']]
    img = datoPokemon['sprites']['front_default']
    
    return {
        "nombre": nombre,
        "peso": peso,
        "altura": altura,
        "habilidades": habilidades,
        "tipos": tipos,
        "imagen_url": img
    }


def guardardato(pokemoninfo):
    if not os.path.exists('pokedex'):
        os.makedirs('pokedex')

    with open(f"pokedex/{pokemoninfo['nombre']}.json", "w") as archivo:
        json.dump(pokemoninfo, archivo, indent=4)
    print(f"Información de {pokemoninfo['nombre']} guardada en pokedex/{pokemoninfo['nombre']}.json")


def visualizar(pokemoninfo):
    
    root = Tk()
    root.title(f"{pokemoninfo['nombre'].capitalize()} - Pokédex")

    
    frame = Frame(root)
    frame.pack(pady=20, padx=20)

    
    response = requests.get(pokemoninfo['imagen_url'])
    img_data = response.content
    img = Image.open(BytesIO(img_data))

    img_tk = ImageTk.PhotoImage(img)
    img_label = Label(frame, image=img_tk)
    img_label.grid(row=0, column=0, padx=10)

    
    info_text = f"""
    Nombre: {pokemoninfo['nombre'].capitalize()}
    Peso: {pokemoninfo['peso']} hectogramos
    Altura: {pokemoninfo['altura']} decímetros
    Tipos: {', '.join(pokemoninfo['tipos'])}
    Habilidades: {', '.join(pokemoninfo['habilidades'])}
    """

    
    label_info = Label(frame, text=info_text, justify="left", font=("arial", 12), padx=10)
    label_info.grid(row=0, column=1)

    
    root.mainloop()


def main():
    n_pokemon= input("Introduce el Pokémon: ")
    dato_pokemon = pokemon(n_pokemon)
    
    if dato_pokemon:
        pokemoninfo = pokeinf(dato_pokemon)
        guardardato(pokemoninfo)
        visualizar(pokemoninfo)

if __name__ == "__main__":
    main()