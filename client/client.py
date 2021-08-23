import json
from tkinter.constants import CENTER
import PySimpleGUI as sg
import websockets
import asyncio
import threading

global hospitales_disponibles
hospitales_disponibles = ["Hospital 1", "Hospital 2", "Hospital 3", "Hospital 4", "Hospital 5"]

async def main():
    while True: # Volver a mostrar menu de conectar al salir
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
        try:
            id = hospitales_disponibles.index(values["_HOSPITAL-ID_"])
            return json.dumps({"operation": 2, "data": {"hospitalId": id+1}})
        except ValueError:
            pass
    elif event != "__TIMEOUT__":
        operations = {"_ELIM-": 3, "_OCUP-": 4, "_VCTE-": 5}
        return json.dumps({"operation": operations[event[:6]], "data": {
            "bedId": event[6:]
        }})

def conectar_hostpital(data):
    layout = [[sg.Button('Actualizar manualmente (ver estado)', key="_BTN-VER-ESTADO_", size=(30,1))]]
    col = []

    lastHospitalId = ""
    for bed in data:
        if lastHospitalId != bed["hospitalId"]:
            lastHospitalId = bed["hospitalId"]
            bedCounter = 1
        else:
            bedCounter += 1
        
        txt = f'Hospital {bed["hospitalId"]}: Cama {bedCounter} - {"ocupada" if bed["state"] else "no ocupada"}'
        col.append([sg.Text(txt),
            sg.Button("Eliminar cama", k=f'_ELIM-{bed["id"]}'),
            sg.Button("Descupar", k=f'_VCTE-{bed["id"]}') if bed["state"] else
            sg.Button("Ocupar", k=f'_OCUP-{bed["id"]}')])
    if len(col) > 0:
        layout.append([sg.Column(col, scrollable=True, vertical_scroll_only=True)])
    layout.extend([
        [sg.Text("Hospital Id")],
        [sg.Combo(hospitales_disponibles, k="_HOSPITAL-ID_", readonly=True)],
        [sg.Button("Agregar Cama")]])
    layout.append([sg.Button('Salir', size=(30,1))])

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
    bedList = []
    websocket = await conectar(ip_port)
    await websocket.send(json.dumps({"operation": 1}))
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
            
            if message["state"] != 0:
                showError(message)
            else:
                operation = message["operation"]

                if operation == 1:
                    bedList = message["data"]
                elif operation == 2:
                    bedList.append(message["data"])
                elif operation == 3:
                    bedList = [bed for bed in bedList if bed["id"] != message["data"]]
                elif operation == 4:
                    for bed in bedList:
                        if bed["id"] == message["data"]:
                            bed["state"] = True
                elif operation == 5:
                    for bed in bedList:
                        if bed["id"] == message["data"]:
                            bed["state"] = False
                
                bedList.sort(key=lambda bed: bed["hospitalId"])
                window.close()
                window = conectar_hostpital(bedList)

        else:
            listener_task.cancel()

        # Si completamos un ciclo del event loop del gui
        if producer_task in done:
            message = producer_task.result()
            if message == "close": # Si se quiere terminar la aplicación
                break
            elif message: # Solo hacer algo si hubo input del usuario
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

def showError(message):
    sg.popup_error(message)


if __name__ == "__main__":
    asyncio.run(main())