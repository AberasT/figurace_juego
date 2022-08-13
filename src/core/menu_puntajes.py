from multiprocessing import set_executable
from tkinter import NONE
import PySimpleGUI as sg
from . import manejar_datos

def iniciar_pantalla_puntajes():
    ''' Crea la ventana de la pantalla de puntajes para visualizar los mejores 20 puntajes por cada dificultad '''
    puntajes, promedios = manejar_datos.obtener_mejores_puntajes()

    for linea in puntajes: 
        if len(linea) == 0: linea.append(("Sin datos","-"))

    for linea in promedios: 
        if len(linea) == 0: linea.append(("Sin datos","-"))

    # Varias tablas para las distintas dificultades
    elem_tabla_1 = sg.Frame(title='Fácil', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=puntajes[0], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tabla_2 = sg.Frame(title='Normal', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=puntajes[1], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tabla_3 = sg.Frame(title='Difícil', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=puntajes[2], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tabla_4 = sg.Frame(title='Einstein', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=puntajes[3], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tablas = [elem_tabla_1, elem_tabla_2, elem_tabla_3, elem_tabla_4]
    
    elem_volver = sg.Button("Volver",key="-PUNTAJES_VOLVER-", font="Helvetica 13",s=(10, 1))

    elem_tabla_prom1 = sg.Frame(title='Fácil', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=promedios[0], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tabla_prom2 = sg.Frame(title='Normal', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=promedios[1], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tabla_prom3 = sg.Frame(title='Difícil', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=promedios[2], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tabla_prom4 = sg.Frame(title='Einstein', title_location='n', border_width=0, layout=[[sg.Table(headings=["Usuario","Puntos"], values=promedios[3], auto_size_columns=True, font="Helvetica 13", num_rows=10, justification="center")]])

    elem_tablas_prom = [elem_tabla_prom1, elem_tabla_prom2, elem_tabla_prom3, elem_tabla_prom4]

    contenedor_puntajes = sg.Frame(title="Top 20 puntajes", title_location="n", vertical_alignment="center", border_width=0, element_justification="center", expand_x=True, expand_y=True, layout=[elem_tablas])

    contenedor_promedios = sg.Frame(title="Top 20 promedios", title_location="n", vertical_alignment="center", border_width=0, element_justification="center", expand_x=True, expand_y=True, layout=[elem_tablas_prom])

    contenedor = [[sg.Col(vertical_alignment="center", element_justification="center", expand_x=True, expand_y=True, layout=[[contenedor_puntajes], [sg.HorizontalSeparator()], [contenedor_promedios], [elem_volver]])]]
    window = sg.Window("Puntajes",contenedor,size=(1000, 600))

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        elif event == "-PUNTAJES_VOLVER-":
            break
    window.close()
