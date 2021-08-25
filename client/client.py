import json
import PySimpleGUI as GUI
import websockets
import asyncio

hospitales = ["Hospital 1", "Hospital 2", "Hospital 3", "Hospital 4", "Hospital 5"]


async def main():
    # Loop principal del programa
    while True:
        ipPort = connectMenu()
        if ipPort == "":
            return
        # Se establecion conexion con el servidor
        window = conectarHostpital([])
        await listener(ipPort, window)


async def guiProducer():
    window, event, values = GUI.read_all_windows(timeout=100)
    if event == GUI.WIN_CLOSED or event == "Salir":
        window.close()
        return "close"
    # Eventos de hospital
    elif event == "_BTN-VER-ESTADO_":
        return json.dumps({"operation": 1})
    elif event == "Agregar Cama":
        try:
            id = hospitales.index(values["_HOSPITAL-ID_"])
            return json.dumps({"operation": 2, "data": {"hospitalId": id + 1}})
        except ValueError:
            pass
    elif event != "__TIMEOUT__":
        operations = {"_ELIM-": 3, "_OCUP-": 4, "_VCTE-": 5}
        return json.dumps({"operation": operations[event[:6]], "data": {"bedId": event[6:]}})


def conectarHostpital(data):
    layout = [[GUI.Button("Actualizar manualmente (ver estado)", key="_BTN-VER-ESTADO_", size=(30, 1))]]
    listaCamas = []
    lastHospitalId = ""
    # Se preparan los datos a mostrar en pantalla
    if data:
        for bed in data:
            if lastHospitalId != bed["hospitalId"]:
                lastHospitalId = bed["hospitalId"]
                bedCounter = 1
            else:
                bedCounter += 1

            txt = f'Hospital {bed["hospitalId"]}: Cama {bedCounter} - {"ocupada" if bed["state"] else "no ocupada"}'
            aux = []
            aux.append(GUI.Text(txt))
            aux.append(GUI.Button("Eliminar cama", k=f'_ELIM-{bed["id"]}'))
            if bed["state"]:
                aux.append(GUI.Button("Desocupar", k=f'_VCTE-{bed["id"]}'))
            else:
                aux.append(GUI.Button("Ocupar", k=f'_OCUP-{bed["id"]}'))
            listaCamas.append(aux)
        layout.append([GUI.Column(listaCamas, scrollable=True, vertical_scroll_only=True, s=(380, 100))])
    # Se termina y retorna la interfaz
    text = GUI.Text("Hospital Id")
    combo = GUI.Combo(hospitales, k="_HOSPITAL-ID_", readonly=True)
    boton = GUI.Button("Agregar Cama")
    layout.extend([[text], [combo], [boton]])
    layout.append([GUI.Button("Salir", size=(30, 1))])
    return GUI.Window("TCP Hostpital Cliente", layout, finalize=True)


def connectMenu():
    layout = [
        [GUI.Text("Conectar a:")],
        [GUI.InputText("127.0.0.1:6789", k="-IP_PORT-")],
        [GUI.Button("Conectar", size=(30, 1))],
    ]
    window = GUI.Window("TCP Hostpital Cliente", layout, finalize=True)
    # Loop de eventos de la pantalla menu
    while True:
        window, event, values = GUI.read_all_windows()
        if event == GUI.WIN_CLOSED:
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
        producer_task = asyncio.ensure_future(guiProducer())

        # Esperar que uno de los dos termine
        done, pending = await asyncio.wait([listener_task, producer_task], return_when=asyncio.FIRST_COMPLETED)

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
                window = conectarHostpital(bedList)
        else:
            listener_task.cancel()
        # Si completamos un ciclo del event loop del gui
        if producer_task in done:
            message = producer_task.result()
            if message == "close":  # Si se quiere terminar la aplicación
                break
            elif message:  # Solo hacer algo si hubo input del usuario
                await websocket.send(message)
        else:
            producer_task.cancel()
    # Cerrar conexión
    await websocket.close()


async def conectar(ipPort):
    try:
        uri = f"ws://{ipPort}/"
        websocket = await websockets.connect(uri, ping_interval=None)
        return websocket
    except ConnectionRefusedError:
        print("Connection error")


def showError(message):
    GUI.popup_error(message)


if __name__ == "__main__":
    asyncio.run(main())
