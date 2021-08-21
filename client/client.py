import json
from tkinter.constants import CENTER
import PySimpleGUI as sg
import websockets
import asyncio

async def main():
    ip_port = connect_menu()
    if ip_port == "":
        return

    websocket = await conectar(ip_port)
    window = conectar_hostpital()

    #conectar
    while True: #Event Loop
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED or event == 'Salir':
            await websocket.close()
            window.close()
            break

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

def conectar_hostpital():
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
    window = sg.Window("TCP Hostpital Cliente", layout, finalize=True)

def connect_menu():
    layout = [
        [sg.Text("Conectar a:")],
        [sg.InputText("127.0.0.1:6789", k="-IP_PORT-")],
        [sg.Button('Conectar', size=(30,1))]        ]
    window = sg.Window("TCP Hostpital Cliente", layout, finalize=True)
    while True: #Event Loop
        window, event, values = sg.read_all_windows()
        if event == sg.WIN_CLOSED:
            window.close()
            return ""
        elif event == "Conectar":
            window.close()
            return values["-IP_PORT-"]


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

async def conectar(ip_port):
    try:
        uri = f"ws://{ip_port}/"
        websocket = await websockets.connect(uri)
        return websocket
    except ConnectionRefusedError:
        print("Connection error")

if __name__ == "__main__":
    asyncio.run(main())