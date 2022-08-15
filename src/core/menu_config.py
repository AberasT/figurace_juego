from multiprocessing import set_executable
import PySimpleGUI as sg
from . import manejar_datos

def iniciar_pantalla_config():
    ''' Crea la ventana de la pantalla de configuración con sus respectivas opciones y funcionalidades '''
    config_previa = manejar_datos.obtener_config()

    nombres_datasets = ["Aleatorio", "Erupciones volcanicas", "Lagos de Argentina", "Peliculas", "Jugadores FIFA 2021"]
    
    elem_datasets = [sg.Text("Dataset ", font="Helvetica 13", s=(30)),
                sg.Combo(nombres_datasets, key="-CONFIG_DATASET-", default_value=config_previa["dataset"], font="Helvetica 13", s = (18, 1), readonly=True)]

    elem_tiempo = [sg.Text("Tiempo límite por ronda (seg)", s=(30), font="Helvetica 13"),
                sg.Slider(range=(1,60), key="-CONFIG_TIEMPO-", orientation="h",border_width= 10, default_value=config_previa["valores"]["tiempo_ronda"], font="Helvetica 13", s = (18, 1), enable_events= True)]

    elem_rondas = [sg.Text("Cantidad de rondas por partida", s=(30), font="Helvetica 13"),
                   sg.Slider(range=(1, 50), key="-CONFIG_RONDAS-", orientation="h", border_width=10, default_value=config_previa["valores"]["cant_rondas"], font="Helvetica 13", s=(18, 1), enable_events=True)]

    elem_puntos_bien = [sg.Text("Puntos por correcta", font="Helvetica 13", s=(30)),
                        sg.Slider(range=(1, 100), key="-CONFIG_PUNTOS_BIEN-", orientation="h", border_width=10, default_value=config_previa["valores"]["puntos_bien"], font="Helvetica 13", s=(18, 1), enable_events=True)]

    elem_puntos_mal = [sg.Text("Puntos restados por incorrecta", font="Helvetica 13", s=(30)),
                       sg.Slider(range=(-1, -100), key="-CONFIG_PUNTOS_MAL-", orientation="h", border_width=10, default_value=config_previa["valores"]["puntos_mal"], font="Helvetica 13", s=(18, 1), enable_events=True)]

    elem_carac_tarjeta = [sg.Text("Características a mostrar por tarjeta", font="Helvetica 13", s=(30)),
                          sg.Slider(range=(1, 5), key="-CONFIG_CANT_CARAC-", orientation="h", border_width=10, default_value=config_previa["valores"]["cant_carac"], font="Helvetica 13", s=(18, 1), enable_events=True)]

    elem_botones = [sg.Button("Guardar",key="-CONFIG_GUARDAR-", font="Helvetica 13",s=(10, 1)), 
                sg.Button("Volver",key="-CONFIG_VOLVER-", font="Helvetica 13",s=(10, 1))]

    contenedor = [[sg.Frame(border_width=0, title="Opciones de configuración",title_location="n", vertical_alignment="center", element_justification="center", expand_x=True, expand_y=True, layout=[elem_datasets, elem_tiempo, elem_rondas, elem_puntos_bien, elem_puntos_mal, elem_carac_tarjeta, [sg.HorizontalSeparator()], elem_botones])]]

    window = sg.Window("Configuración",contenedor,size=(1000, 600))
    flag_sliders = False

    while True:
        event, values = window.read()
        sliders = "-CONFIG_TIEMPO- -CONFIG_RONDAS- -CONFIG_PUNTOS_BIEN- -CONFIG_PUNTOS_MAL- -CONFIG_CANT_CARAC-".split()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-CONFIG_GUARDAR-":
            seleccionados = {"valores": {
                                "tiempo_ronda": values["-CONFIG_TIEMPO-"],
                                "cant_rondas" : values["-CONFIG_RONDAS-"],
                                "puntos_bien" : values["-CONFIG_PUNTOS_BIEN-"],
                                "puntos_mal" : values["-CONFIG_PUNTOS_MAL-"],
                                "cant_carac" : values["-CONFIG_CANT_CARAC-"],
                            }, 
                            "dataset": values["-CONFIG_DATASET-"],
                            "dificultad": config_previa["dificultad"],
                            "nick": config_previa["nick"]}
            if (flag_sliders):
                seleccionados["dificultad"] = "Personalizada"
            manejar_datos.guardar_config(seleccionados)
        elif event in sliders:
            flag_sliders = True
        elif event == "-CONFIG_VOLVER-":
            break
    window.close()
