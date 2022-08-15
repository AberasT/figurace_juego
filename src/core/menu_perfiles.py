import PySimpleGUI as sg
from . import manejar_datos


def crear_ventana_nuevo_jugador():
    '''Crea y retona la ventana que tomara la información para crear el nuevo perfil. Este incluye texto para advertir, de ser necesario, 
    por que no puede ser creado el perfil con los datos ingresados'''
    layout = [[[sg.Text(text='Ingrese los datos del nuevo perfil: ', size=50)], [sg.Text(text='Nickname '), sg.Input()],
        [sg.Text(text='Ya existe un perfil con ese Nickname. Pruebe ingresando otro distinto.',key='-TEXTO NICKNAME EXISTENTE-', visible=False, text_color='red')],
        [sg.Text(text='No puede registrar un perfil con un Nickname vacio.', key='-TEXTO NICKNAME VACIO-', visible=False, text_color='red')]],
        [sg.Text(text='Edad '), sg.Slider(range=(1, 120), orientation="h", border_width=8, default_value = 20, font="Helvetica 13", s=(30, 5))],
        [sg.Text(text='Genero autopercibido '), sg.Input()],
        [sg.Text(text='Por favor, especifique un genero', key='-TEXTO GENERO VACIO-', visible=False, text_color='red')],
        [sg.Button(button_text='Crear', key='-CONFIRMAR CREAR JUGADOR-')],
        [sg.Button(button_text='Cancelar', key='-CANCELAR CREAR JUGADOR-')],
    ]
    return sg.Window('Nuevo Perfil', layout, finalize=True)


def crear_ventana_editar_jugador(jugador_seleccionado):
    '''Recibe la información del perfil seleccionado para la edición del mismo y 
    crea y retona la ventana para editar un jugador. Esta es creada con la información ya escrita del jugador seleccionado para la edición'''
    layout = [[sg.Text(text='Ingrese los datos del nuevo perfil: ', size=50)], [sg.Text(text='Nickname '), sg.Input(default_text=jugador_seleccionado[0][0], readonly=True)],
              [sg.Text(text='Edad '), sg.Slider(range=(1, 120), orientation="h", border_width=8, default_value=20, font="Helvetica 13", s=(30, 5))],
              [sg.Text(text='Genero autopercibido '), sg.Input(default_text=jugador_seleccionado[0][2])],
              [sg.Text(text='Por favor, especifique un genero', key='-TEXTO GENERO VACIO EDICION-', visible=False, text_color='red')],
              [sg.Button(button_text='Confirmar edición',key='-CONFIRMAR EDICION JUGADOR-')],
              [sg.Button(button_text='Cancelar edición', key='-CANCELAR EDICION JUGADOR-')]
              ]
    return sg.Window('Editar Perfil', layout, finalize=True)


def crear_ventana_perfiles():
    '''Crea y retorna la ventana de perfiles. Esta incluye una tabla con perfiles seleccionables para su edición, y dos botones, tanto para volver
    como para crear un nuevo perfil'''
    cabecera = ['Nickname', 'Edad', 'Genero Autopercibido']
    lista_jugadores = crear_listado_jugadores()

    layout = [[sg.Table(values=lista_jugadores, headings=cabecera,
                        auto_size_columns=True,
                        row_height=25,
                        enable_events=True,
                        num_rows=min(10, len(lista_jugadores)), key='-EDITAR JUGADOR-')],
              [sg.Button('Crear Jugador', key='-CREAR JUGADOR-')],
              [sg.Button('Volver', key='-VOLVER-')],
              ]
    return sg.Window("Perfil", layout, margins=(200, 150), finalize=True)


# Metodos de creacion/modificacion de perfiles
def crear_perfil(datos, window):
    '''Recibe la información ingresada en la ventana de creacion de perfiles y verifica si el nickname ya existe o esta vacío. Modifica la visibilidad de textos de la ventana de creacion de perfiles para advertir al usuario si el nickname ya existe o es vacío. 
    De ser correcta la información, agrega el perfil al listado de jugadores y llama al metodo guardar_perfiles para almacenar la nueva lista en el archivo json de perfiles'''
    jugador = {'nick': datos[0].strip(" "), 'edad': int(datos[1]), 'genero': (datos[2].strip(" ")).title() }
    if (len(jugador['nick']) != 0):
        window['-TEXTO NICKNAME VACIO-'].Update(visible=False)
        window['-TEXTO GENERO VACIO-'].Update(visible = False)
        jugadores = manejar_datos.obtener_perfiles()
        #Busco en la lista de jugadores el nick del jugador que modifique
        for i in range(len(jugadores)):
            if jugadores[i]['nick'] == jugador['nick']:
                window['-TEXTO NICKNAME EXISTENTE-'].Update(visible= True)
                return False
            else: 
                window['-TEXTO NICKNAME EXISTENTE-'].Update(visible=False)
        if len(datos[2]) != 0:
            window['-TEXTO GENERO VACIO-'].Update(visible = False)
            jugadores.append(jugador)
            manejar_datos.guardar_perfiles(jugadores)
            return True
        else:
            window['-TEXTO GENERO VACIO-'].Update(visible = True)
            return False
    else:
        window['-TEXTO NICKNAME VACIO-'].Update(visible=True)
        if len(datos[2]) != 0:
            window['-TEXTO GENERO VACIO-'].Update(visible=False)
        return False


def modificar_perfil(datos):
    '''Recibe la informacion nueva del perfil editado, obtiene el listado de perfiles y busca la información del nickname del perfil editado para sobreescribirlo con la nueva información'''
    jugador_editado = {'nick': datos[0], 'edad': int(datos[1]), 'genero': datos[2]}
    jugadores = manejar_datos.obtener_perfiles()
    #Busco en la lista de jugadores el nick del jugador que modifique
    for i in range(len(jugadores)):
        #Cuando lo encuentro, le actualizo la informacion
        if jugadores[i]['nick'] == jugador_editado['nick']:
            jugadores[i] = jugador_editado
            break
    manejar_datos.guardar_perfiles(jugadores)

def crear_listado_jugadores():
    '''Trae el diccionario de jugadores del archivo json de perfiles, y crea una lista de listas con los perfiles para mostrarlo 
    en la tabla de perfiles de la ventana'''
    jugadores = manejar_datos.obtener_perfiles()
    lista_jugadores = list()
    for jugador in jugadores:
        datos = [jugador['nick'], jugador['edad'], jugador['genero']]
        lista_jugadores.append(datos)
    return lista_jugadores

def iniciar_menu_perfiles():
    '''Funcion que representa el cuerpo principal del modulo de la ventana de menu de perfiles'''
    window = crear_ventana_perfiles()
    while True:
        current_window, event, values = sg.read_all_windows()
        if (event == sg.WIN_CLOSED) or (event == '-VOLVER-'):
            break
        elif event == '-EDITAR JUGADOR-':
            lista_jugadores = crear_listado_jugadores()
            jugador_seleccionado = [lista_jugadores[row] for row in values[event]]
            window = crear_ventana_editar_jugador(jugador_seleccionado)
            current_window.close()

        elif event == '-CONFIRMAR EDICION JUGADOR-':
            if(len(values[2].strip(" ")) != 0):
                modificar_perfil(values)
                window = crear_ventana_perfiles()
                current_window.close()
            else:
                window['-TEXTO GENERO VACIO EDICION-'].Update(visible = True)

        elif event == '-CANCELAR EDICION JUGADOR-':
            window = crear_ventana_perfiles()
            current_window.close()

        elif event == '-CREAR JUGADOR-':
            window = crear_ventana_nuevo_jugador()
            current_window.close()

        elif event == '-CONFIRMAR CREAR JUGADOR-':
            if (crear_perfil(values, window)):
                current_window.close()
                window = crear_ventana_perfiles()

        elif event == '-CANCELAR CREAR JUGADOR-':
            current_window.close()
            window = crear_ventana_perfiles()

        elif event == '-VOLVER-':
            current_window.close()
    window.close()
