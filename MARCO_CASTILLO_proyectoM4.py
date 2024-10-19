# Biblioteca request para hacer peticiones a la PokeAPI
import requests
# Para mejorar archivos y directorios
import os
# Importamos para guardar los datos del pokémon en formato JSON
import json
# Importamos para crear la interfaz gráfica
from tkinter import Tk, Label, Frame
#Importamos pillow para manejar imagenes
from PIL import Image, ImageTk
# Importamos BytesIO para manipular los datos de imagen recibidos
from io import BytesIO

# Funcion para buscar los datos del Pokémon en la PokeAPI
def pokemon(nombre):
    # Se crea la URL con el nombre del Pokémon
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    #Se hace la solicitud a la API para obtener los datos
    response = requests.get(url)
    
    # Si la respuesta es exitosa se otorga el código 200 y se devuelven los datos en formato JSON
    if response.status_code == 200:
        return response.json()
    # En caso contrario se manda el mensaje de que nose encontro y se devuelve none
    else:
        print(f"{nombre.capitalize()} no encontrado")
        return None

# La definicion estrae la información importante del pokémon
def pokeinf(datoPokemon):
    # Se guarda el nombre del pokémon
    nombre = datoPokemon['name']
    # Se guarda el peso del pokémon
    peso = datoPokemon['weight']
    # Se Guarda la altura del pokémon
    altura = datoPokemon['height']
    # Se guardan una lista con las habilidades del pokémon
    habilidades = [habilidad['ability']['name'] for habilidad in datoPokemon['abilities']]
    # Se guarda el tipo al que pertenece el pokémon
    tipos = [tipo['type']['name'] for tipo in datoPokemon['types']]
    # Se guarda la URL de la imagen del pokémon
    img = datoPokemon['sprites']['front_default']
    
    # Se devuelve un diccionario con los datos recabados
    return {
        "nombre": nombre,
        "peso": peso,
        "altura": altura,
        "habilidades": habilidades,
        "tipos": tipos,
        "imagen_url": img
    }

# Esta función guarda los datos obtenidos en un archivo JSON
def guardardato(pokemoninfo):
    # si no existe una carpeta llamada pokedex, la crea
    if not os.path.exists('pokedex'):
        os.makedirs('pokedex')
    # Se abre un archivo JSON en modo escritura para guardar los datos
    with open(f"pokedex/{pokemoninfo['nombre']}.json", "w") as archivo:
        # Guarda el diccionadrio de la informacion obtenida con formato JSON
        json.dump(pokemoninfo, archivo, indent=4)
    # Imprimimos que se ha guardado correctamnte la información
    print(f"Información de {pokemoninfo['nombre']} guardada en pokedex/{pokemoninfo['nombre']}.json")

# La función para crear la interfaz gráfica donde se mostrarán los datos del pokémon
def visualizar(pokemoninfo):
    # Inicializacion de la ventana de tkinter
    root = Tk()
    # El nombre que aparecera en la barra de titulo
    root.title(f"{pokemoninfo['nombre'].capitalize()} - Pokédex")

    # Se crea un marco para organizar los widgets en la ventana
    frame = Frame(root)
    # Se configuran los margenes de la ventana
    frame.pack(pady=20, padx=20)

    # Se envia petición para obtener la imagen del pokémon
    response = requests.get(pokemoninfo['imagen_url'])
    # Se guarda los datos de la imagen
    img_data = response.content
    # Se abre la imagen con  Pillow
    img = Image.open(BytesIO(img_data))

    # Se convierte la imagen en formato tkinter para la visualización
    img_tk = ImageTk.PhotoImage(img)
    # Se crea la etiqueta label, para mostrar la imagen dentro del marco
    img_label = Label(frame, image=img_tk)
    # Se coloca el posicionamiento de la imagen dentro del marco
    img_label.grid(row=0, column=0, padx=10)

    # Se crea el texto con la información del pokémon
    info_text = f"""
    Nombre: {pokemoninfo['nombre'].capitalize()}
    Peso: {pokemoninfo['peso']} hectogramos
    Altura: {pokemoninfo['altura']} decímetros
    Tipos: {', '.join(pokemoninfo['tipos'])}
    Habilidades: {', '.join(pokemoninfo['habilidades'])}
    """

    # Se crea el label para mostrar la información
    label_info = Label(frame, text=info_text, justify="left", font=("arial", 12), padx=10)
    # Se posiuciona el texto en la cuadricula de la fila 0 columna 1
    label_info.grid(row=0, column=1)

    # Se ejecuta un bucle principal de la ventana para que se mantenga abierta
    root.mainloop()

# Es la definición principal del programa
def main():
    # Se pide al usuario ingrese el nombre de un pokémon
    n_pokemon= input("Introduce el Pokémon: ")
    # Se llama a la funcion que busca los datos del pokémon
    dato_pokemon = pokemon(n_pokemon)
    
    # Si se encuentran los datos del pokémon se realiza el proceso para mostrarlos
    if dato_pokemon:
        pokemoninfo = pokeinf(dato_pokemon)
        guardardato(pokemoninfo)
        visualizar(pokemoninfo)
# Si estamos ejecutando este archivo directamente (y no lo estamos importando en otro),
# entonces llamamos a la función main() para que empiece el programa.
if __name__ == "__main__":
    main()