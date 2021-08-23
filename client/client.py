import json
from tkinter.constants import CENTER
import PySimpleGUI as sg
import websockets
import asyncio
import threading

async def main():
    ip_port = connect_menu()
    if ip_port == "":
        return

    window = conectar_hostpital([])

    await listener(ip_port, window)

async def gui_producer():
    window, event, values = sg.read_all_windows(timeout=100)
    if event == sg.WIN_CLOSED or event == 'Salir':
        window.close()
        return "close"

    #Eventos de hospital
    elif event == '_BTN-VER-ESTADO_':
        return json.dumps({"operation": 1})
    elif event == 'Agregar Cama':  
        agregar_cama()
    elif event == 'Eliminar Cama': 
        eliminar_cama(values["-ID-"])
    elif event == 'Ocupar Cama': 
        ocupar_cama(values["-ID-"])
    elif event == 'Desocupar Cama':
        desocupar_cama(values["-ID-"])

def conectar_hostpital(data):
    layout = [
        [sg.Button('Actualizar manualmente (ver estado)', key="_BTN-VER-ESTADO_", size=(30,1))]]
    layout.append([[sg.Button('Salir', size=(30,1))]])

    return sg.Window("TCP Hostpital Cliente", layout, finalize=True)

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
        

async def listener(ip_port, window):
    websocket = await conectar(ip_port)
    while True:
        # Crear dos tasks que en el mismo thread se encargan de esperar nuevos mensajes y leer gui
        listener_task = asyncio.ensure_future(websocket.recv())
        producer_task = asyncio.ensure_future(gui_producer())

        # Esperar que uno de los dos termine
        done, pending = await asyncio.wait(
            [listener_task, producer_task],
            return_when = asyncio.FIRST_COMPLETED)

        # Si fue un mensaje del servido que llegó
        if listener_task in done:
            message = json.loads(listener_task.result())
            
            window.close()
            window = conectar_hostpital(message["data"])
        else:
            listener_task.cancel()

        # Si completamos un ciclo del event loop del gui
        if producer_task in done:
            message = producer_task.result()
            if message == "close": # Si se quiere terminar la aplicación
                break
            elif message: # Solo hacerr algo si hubo input del usuario
                await websocket.send(message)
        else:
            producer_task.cancel()

    # Cerrar conexión
    await websocket.close()

async def conectar(ip_port):
    try:
        uri = f"ws://{ip_port}/"
        websocket = await websockets.connect(uri, ping_interval=None)
        return websocket
    except ConnectionRefusedError:
        print("Connection error")

if __name__ == "__main__":
    asyncio.run(main())