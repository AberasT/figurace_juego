from random import shuffle, choices
import PySimpleGUI as sg
import datetime
from . import manejar_datos
from . import menu_principal as menu

def generar_opciones(dataset):
    '''Genera las opciones a seleccionar en el juego, devolviendo 5 botones, 4 falsos, 1 como opcion correcta.
    Tambien devuelve los datos de la opcion verdadera para mostrar en la pantalla a la hora de encontrar la verdadera'''
    lineas = choices(dataset, k=5)    #Guarda 5 lineas aleatorias del dataset, (se trae como lista de listas)
    opcion_correcta = [sg.Button(lineas[0][5].title(), size=(60, 1), font=("Helvetica", 10),key="-OPCION CORRECTA-")]
    linea_correcta = lineas[0] #Me guardo los datos de la linea correcta
    dataset.remove(linea_correcta)
    opciones = [opcion_correcta] #Creo lista de elemento botones con la primera opcion V
    for i in range(1,5):
        boton_incorrecto = [sg.Button(lineas[i][5].title(), size=(60, 1), font=("Helvetica", 10),key="-OPCION INCORRECTA "+str(i)+"-")]
        opciones.append(boton_incorrecto)   #Agrego botones falsos(4)
    shuffle(opciones) #Mezclo los botones
    return opciones, linea_correcta

def obtener_caracteristicas(config,encabezado,linea_correcta):
    ''' Este modulo busca los datos de linea correcta y los nombres de las caracteristicas
    para mostrar ordenadamente cada CARACTERISTICA = DATO '''
    caracteristicas = [[sg.Text('CARACTERISTICAS',font=("overstrike", 14))]] #Creo lista de elementos texto, para mostrar todas las caracteristicas
    for i in range(int(config["valores"]["cant_carac"])):
        nueva_carac = [sg.Text(encabezado[i].title() + ": " + linea_correcta[i].title(),font=("Helvetica", 12),text_color='#C0C0C0')]
        caracteristicas.append(nueva_carac) # Agrego nuevo elemento de texto a mi lista de caracteristicas
    return caracteristicas #Devuelvo lista de elementos

def generar_layout(config,dataset,encabezado):
    '''Genero lista de elementos para iniciar la pantalla'''

    cant_tiempo = config["valores"]["tiempo_ronda"] #Busca cantidad de tiempo a utilizar en config  

    #Se define contador con la cantidad de tiempo establecida por la dificultad'''
    
    elemento_contador = [sg.Frame(title="TIEMPO", title_location="n", border_width = 2,
                                 layout=[[sg.Text(cant_tiempo,font = ("bold", 15), text_color = "white",key="-CONTADOR-")]])]
    
    elemento_puntaje = [sg.Frame(title="PUNTAJE", title_location="n", border_width = 2,
                                 layout=[[sg.Text(0 ,font = ("bold", 15), text_color = "white",key="-PUNTOS-")]])]
                              
    #Genero opciones y caracteristicas a traves de los modulos definidos anteriormente'''
    opciones, linea_correcta = generar_opciones(dataset)
    caracteristicas = obtener_caracteristicas(config,encabezado,linea_correcta)
   
    #Se crea la lista de elementos
    layout = [
        #Caracteristicas
        caracteristicas,

        #Opciones a elegir para pasar (son 5)
        opciones,

        #En esta linea se va a implementar los puntajes por rondas
        #puntajes,
    
        #Boton pasar (se pierde la ronda)
        [sg.Button("Pasar", size=(60, 1), font=("Helvetica", 10),button_color=('black','gray'),key="-PASAR-")],

        #Volver menu (Se pierde actual y restantes)
        [sg.Button("Volver al Menu", size=(60, 1), font=("Helvetica", 10),button_color=('black','gray'), key="-ABANDONO-")],
 
        #Cuenta Regresiva
        elemento_puntaje,
        elemento_contador
    ]
    return layout

def pasar_ronda(cant_puntos,config,ronda_actual,cant_rondas,eventos,estado = "finalizado"):
    if ronda_actual == cant_rondas:
        generar_evento(config,eventos,"fin",estado,"-","-")
        
        id = manejar_datos.obtener_id_ultima_partida()
        manejar_datos.guardar_partidas(eventos, id)
        
        if (estado == "finalizado"): 
            puntajes = manejar_datos.obtener_puntajes()
            manejar_datos.guardar_puntajes(puntajes, config["dificultad"], config["nick"], cant_puntos)

            #Al finalizar guardo ultima partida
            manejar_datos.guardar_ultima_partida({"nick": config["nick"],"dificultad": config["dificultad"],
            "fecha": datetime.datetime.now().strftime('%d/%m/%Y'),"puntaje": cant_puntos})

            sg.Popup("Fin de partida","Puntaje logrado: "+str(cant_puntos))
        elif (estado == "cancelada"):
            sg.Popup("Partida abandonada... ", "Puntaje logrado: "+str(cant_puntos))
        return True
    else:
        return False

def generar_evento(config,eventos,evento,estado,texto_ingresado, respuesta):
    log = { "timestamp": int(datetime.datetime.timestamp(datetime.datetime.now())),
            "id": "",
            "evento": evento,
            "usuarie": config["nick"],
            "estado": estado,
            "texto_ingresado": texto_ingresado,
            "respuesta": respuesta,
            "nivel": config["dificultad"],
            }
    eventos.append(log)

def iniciar_pantalla_juego():
    ''' Este modulo inicia una partida en su primera caratula y con los valores traidos de config 
    luego, a traves de pasar ronda, actualizando el puntaje y reiniciando el tiempo se va pasando cada nivel hasta terminar'''
   
    #A traves mis manejadores de datos, obtengo las configuraciones y el dataset de los archivos correspondientes para generar mi ventana
    config = manejar_datos.obtener_config()
    dataset = manejar_datos.obtener_dataset(config["dataset"])
    encabezado = dataset[0]
    dataset.pop(0)

    #En esta variable guardo el tiempo disponible actual para actualizarlo cada seg
    cant_tiempo = config["valores"]["tiempo_ronda"]

    # Inicio cantidad de rondas de la partida y puntos en 0
    ronda_actual = 1
    cant_rondas = config["valores"]["cant_rondas"]
    cant_puntos = 0

    # Creo mi lista de eventos y el primer evento inicio_partida
    eventos = list()
    generar_evento(config,eventos,"inicio_partida","nueva","-","-")

    #Creo mi primera ventana con generar_layout con los parametros correspondientes
    window = sg.Window("Menu de juego", layout = generar_layout(config,dataset,encabezado), size=(500, 550), finalize=True)

    while True:
        event, values = window.read(timeout=1000)
        if event == "-ABANDONO-" or event == sg.WIN_CLOSED:
            ronda_actual = cant_rondas
            pasar_ronda(cant_puntos,config,ronda_actual,cant_rondas,eventos,"cancelada")
            menu.crear_ventana_principal
            break

        elif event == "__TIMEOUT__":
            # Incrementamos el cantidad tiempo
            if cant_tiempo > 0: 
                cant_tiempo -= 1
            else:
                generar_evento(config,eventos,"intento","timeout","-","-")
                if pasar_ronda(cant_puntos,config,ronda_actual,cant_rondas,eventos): break
                else: 
                    ronda_actual += 1
                    window.close()
                    cant_tiempo = config["valores"]["tiempo_ronda"]
                    window = sg.Window("Menu de juego", layout = generar_layout(config,dataset,encabezado), size=(500, 550), finalize=True)
                    window["-PUNTOS-"].update(cant_puntos)

            elem = window["-CONTADOR-"]   
            elem.update(cant_tiempo)

        elif event == "-OPCION CORRECTA-":
            generar_evento(config,eventos,"intento","ok",window[event].get_text(),window["-OPCION CORRECTA-"].get_text())

            cant_puntos = cant_puntos + config["valores"]["puntos_bien"]

            if pasar_ronda(cant_puntos,config,ronda_actual,cant_rondas,eventos): break
            else: 
                ronda_actual += 1
                window.close()
                window = sg.Window("Menu de juego", layout = generar_layout(config,dataset,encabezado), size=(500, 550), finalize=True)
                window["-PUNTOS-"].update(cant_puntos)
            cant_tiempo = config["valores"]["tiempo_ronda"]

        elif 'INCORRECTA' in event:
            cant_puntos = cant_puntos + config["valores"]["puntos_mal"]
            window["-PUNTOS-"].update(cant_puntos)
            generar_evento(config,eventos,"intento","error",window[event].get_text(),window["-OPCION CORRECTA-"].get_text())

            if pasar_ronda(cant_puntos,config,ronda_actual,cant_rondas,eventos): 
                break
            else: 
                ronda_actual += 1
                window.close()
                window = sg.Window("Menu de juego", layout = generar_layout(config,dataset,encabezado), size=(500, 550), finalize=True)
                window["-PUNTOS-"].update(cant_puntos)
            cant_tiempo = config["valores"]["tiempo_ronda"]

        elif event == "-PASAR-":
            generar_evento(config,eventos,"intento","pasar","-",window["-OPCION CORRECTA-"].get_text())

            if pasar_ronda(cant_puntos,config,ronda_actual,cant_rondas,eventos): break
            else: 
                ronda_actual += 1
                window.close()
                window = sg.Window("Menu de juego", layout = generar_layout(config,dataset,encabezado), size=(500, 550), finalize=True)
                window["-PUNTOS-"].update(cant_puntos)
            cant_tiempo = config["valores"]["tiempo_ronda"]

    window.close()  
