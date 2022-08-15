from ntpath import join
import PySimpleGUI as sg
import os
from . import manejar_datos
from . import menu_perfiles
from . import menu_config
from . import menu_puntajes
from . import menu_juego


sg.theme('DarkBlue')

def crear_ventana_nuevo_jugador():
    """Por si por primera vez, no hay perfiles creados, crea y retorna la ventana de creación de perfiles"""

    layout = [[[sg.Text(text='Ingrese los datos del nuevo perfil: ', size=50)], [sg.Text(text='Nickname '), sg.Input()],
               [sg.Text(text='Ya existe un perfil con ese Nickname. Pruebe ingresando otro distinto.',
                        key='-TEXTO NICKNAME EXISTENTE-', visible=False, text_color='red')],
               [sg.Text(text='No puede registrar un perfil con un Nickname vacio.', key='-TEXTO NICKNAME VACIO-', visible=False, text_color='red')]],
              [sg.Text(text='Edad '), sg.Slider(range=(1, 120), orientation="h", border_width=8, default_value=20, font="Helvetica 13", s=(30, 5))],
              [sg.Text(text='Genero autopercibido '), sg.Input()],
              [sg.Text(text='Por favor, especifique un genero', key='-TEXTO GENERO VACIO-', visible=False, text_color='red')],
              [sg.Button(button_text='Crear', key='-CONFIRMAR CREAR PRIMER JUGADOR-')],
              ]

    return sg.Window('Nuevo Perfil', layout, finalize=True)


def crear_ventana_principal():
    carpeta_datos = (os.path.join(os.getcwd(),"src", "datos"))
    if not(os.path.isdir(carpeta_datos)):
        os.mkdir(carpeta_datos)
    '''Crea y retona la ventana principal, con los perfiles ya creados para seleccionar y las dificultades '''
    menu = [
        [sg.Text("FIGURACE", justification="center",
                 font="Helvetica 15 bold", pad=((0, 0), (0, 10)))],
        [sg.Button("Jugar", key="-JUGAR-", font="Helvetica 13")],
        [sg.Button("Configuracion", key="-CONFIG-", font="Helvetica 13")],
        [sg.Button("Puntajes", key="-PUNTAJES-", font="Helvetica 13")],
        [sg.Button("Perfil", key="-PERFIL-", font="Helvetica 13")],
        [sg.Button("Salir", key="-EXIT-", font="Helvetica 13")],
    ]

    #Obtiene la ultima sesion abierta
    ultima_partida = manejar_datos.obtener_ultima_partida()
    config = manejar_datos.obtener_config()

    #Consigo los jugadores y los guardo en el menu
    jugadores = manejar_datos.obtener_perfiles()
    if(len(jugadores)) == 0:
        return crear_ventana_nuevo_jugador()

    perfiles = []
    for jugador in jugadores:
        perfiles.append(jugador["nick"])

    #Usuario, configuracion y ultima sesion con su puntaje(a resolver)
    layout_configs = [
        

        [sg.Frame(title="Usuario", element_justification="center", title_location="n", pad=((50, 0), (0, 150)), border_width=0,
                  layout=[[sg.Combo(perfiles, key="-USER-", font="Helvetica 11", size=(20, 1), enable_events=True, readonly=True, default_value=config["nick"])]])],

        [sg.Frame(title="Dificultad", element_justification="center", title_location="n", pad=((50, 0), (0, 150)), border_width=0,
                  layout=[[sg.Combo(["Facil", "Normal", "Dificil", "Einstein"], size=(20, 1), font="Helvetica 11", key="-DIFICULTAD-", enable_events=True, readonly=True, default_value=config["dificultad"])]])],
        
    ]

    layout = [
        [sg.Frame(title="Última partida", title_location="n", border_width=1,
                                 layout=[[sg.Text(ultima_partida["nick"], font="Helvetica 11")]])],
        [sg.Col(menu, element_justification='center',  pad=(
            (190, 0), (100, 100))), sg.Col(layout_configs)]
    ]

    return sg.Window("Figurace", layout, size=(500, 500), finalize=True)


def iniciar_menu_principal():
    """Función principal del menu principal"""
    window = crear_ventana_principal()
    while True:
        event, values = window.read()

        if(event == sg.WIN_CLOSED) or (event == "-EXIT-"):
            break
        elif event == "-JUGAR-":
            window.close()
            window = menu_juego.iniciar_pantalla_juego()
            window = crear_ventana_principal()
        elif event == "-PUNTAJES-":
            window.close()
            window = menu_puntajes.iniciar_pantalla_puntajes()
            window = crear_ventana_principal()
        elif event == "-CONFIG-":
            window.close()
            window = menu_config.iniciar_pantalla_config()
            window = crear_ventana_principal()
        elif event == "-PERFIL-":
            window.close()
            window = menu_perfiles.iniciar_menu_perfiles()
            window = crear_ventana_principal()
        elif event == "-USER-":
            config = manejar_datos.obtener_config()
            config["nick"] = values["-USER-"]
            manejar_datos.guardar_config(config) #Para guardar que jugador quedo seleccionado
        elif event == "-DIFICULTAD-":
            config = manejar_datos.obtener_config()
            config["dificultad"] = values["-DIFICULTAD-"]
            manejar_datos.seleccionar_dificultad(values["-DIFICULTAD-"])
        elif event == "-CONFIRMAR CREAR PRIMER JUGADOR-":
            config = manejar_datos.obtener_config()
            if(menu_perfiles.crear_perfil(values, window)):
                window.close()
                config["nick"] = values[0]
                manejar_datos.guardar_config(config)
                window = crear_ventana_principal()
    window.close()
