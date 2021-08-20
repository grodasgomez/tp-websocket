import json
from tkinter.constants import CENTER
import PySimpleGUI as sg
import websockets
import asyncio

async def main():
    windows = {
        "main": crear_ventana_principal()
    }

    while True: #Event Loop
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Salir':
            window.close()
            windows.pop(window.name)
            if len(windows) == 0:
                break
        
        #Eventos de seleccionar
        elif event == 'Conectar':
            if not values["-NOMBRE_HOSPITAL-"]:
                sg.popup("Debe especificar el nombre del hospital")
            elif not values["-NOMBRE_HOSPITAL-"] in windows:
                windows[values["-NOMBRE_HOSPITAL-"]] = conectar_hostpital(values["-NOMBRE_HOSPITAL-"])
            else:
                sg.popup(
                    "Ya existe una conexión abierta con este hospital!",
                    auto_close = True,
                    auto_close_duration = 3)

        #Eventos de hospital
        elif event == 'Ver Estado':
            ver_estado()
        elif event == 'Agregar Cama':  
            agregar_cama()
        elif event == 'Eliminar Cama': 
            eliminar_cama(values["-ID-"])
        elif event == 'Ocupar Cama': 
            ocupar_cama(values["-ID-"])
        elif event == 'Desocupar Cama':
            desocupar_cama(values["-ID-"])


def crear_ventana_principal():
    layout = [
        [sg.Text('Por favor ingresar ID del hospital a conectar:')],
        [sg.Input(key='-NOMBRE_HOSPITAL-')],
        [sg.Button('Conectar'), sg.Button('Salir')]]
    window = sg.Window('Window Title', layout, location=(800,600), finalize=True)
    window.name = 'main'

def conectar_hostpital(nombre_hospital):
    #TODO conectar

    layout = [
        [sg.Button('Ver Estado', size=(30,1))],
        [sg.Button('Agregar Cama', size=(30,1))],
        [sg.Text('Modificar cama con ID: ', justification=CENTER, size=(20,1)), sg.Input(key='-ID-', size=(11,1))],
        [sg.Button('Eliminar Cama', size=(30,1))],
        [sg.Button('Ocupar Cama', size=(30,1))],
        [sg.Button('Desocupar Cama', size=(30,1))],
        [sg.Text()],
        [sg.Button('Salir', size=(30,1))]]
    window = sg.Window(nombre_hospital, layout, finalize=True)
    window.name = nombre_hospital

def ver_estado():
    print("Ver estado")

def agregar_cama():
    print("Agregar cama")

def eliminar_cama(id):
    print("Eliminar Cama", id)

def ocupar_cama(id):
    print("Ocupar cama", id)

def desocupar_cama(id):
    print("Desocupar cama", id)

async def hello():
    uri = "ws://127.0.0.1:6789/"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"operation": 1}, separators=(',', ':')))
        response = await websocket.recv()
        print(response)
        response = await websocket.recv()
        print(response)
        response = await websocket.recv()
        print(response)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())