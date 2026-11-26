import socket
import threading

import pytest

from server import iniciar_servidor

# ==========================================
# FIXTURE DEL SERVIDOR
# ==========================================


@pytest.fixture
def servidor_chat():

    stop_event  = threading.Event()
    ready_event = threading.Event()

    puerto_real = []

    hilo = threading.Thread(
        target=iniciar_servidor,

        kwargs={
            "host":"localhost",
            "puerto": 0,
            "stop_event": stop_event,
            "ready_event": ready_event,
            "puerto_real": puerto_real
        },
        daemon=True
    )

    hilo.start()


    # --- Esperar Hasta Que El Servidor Este Listo/Escuchando ---
    assert ready_event.wait(timeout=2)

    puerto = puerto_real[0]

    yield puerto

    # --- Apagamos El Servidor Al Terminar El Test ---
    stop_event.set()

    hilo.join(timeout=2)


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

# ------------------------------
# FUNCION PARA CREAR CLIENTE
# ------------------------------

def Creat_client(puerto):

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    cliente.settimeout(1) # Obtener excepcion despues de esperar 1 segundo

    cliente.connect( ("localhost", puerto) )

    return cliente



# ------------------------------
# FUNCION PARA ENVIAR MENSAJES
# ------------------------------

def enviar_mensaje(cliente, mensaje):
    cliente.sendall(mensaje.encode()) # Convertimos el texto del mensaje a bytes y lo enviamos al servidor.



# ------------------------------
# FUNCION PARA RECIBIR MENSAJES
# ------------------------------
def recibir_mensajes(cliente, mensajes_esperados):
    datos_recibidos = ""                       # Almacen De Mensajes.

    # --- Recibir Hasta Obtener Todos Los Mensajes ---
    while True: 

        datos = cliente.recv(1024).decode()    # Recibir y Decodificar bytes.
        datos_recibidos += datos               # Acomular los datos recibidos.

        # --- Verificamos Si Ya Obtuvimos Todos Los Mensajes ---
        if all(
            mensaje in datos_recibidos
            for mensaje in mensajes_esperados
        ):
            return datos_recibidos # Retornar Los Mensajes Recibidos.



# ==========================================
# PRUEBAS DE INTEGRACIÓN
# ==========================================


# -----------------------------------
# MULTIPLES CONEXINES SIMULTANEAS 
# -----------------------------------
def test_Multipes_Clientes( servidor_chat):

    # --- Crear Clientes ---
    cliente_1 = Creat_client(servidor_chat)
    cliente_2 = Creat_client(servidor_chat)
    cliente_3 = Creat_client(servidor_chat)

    # --- Cerrar Coenxiones ---
    cliente_1.close()
    cliente_2.close()
    cliente_3.close()



# -----------------------------------
# VERIFICAR LLEGADA DE MENSAJE 
# -----------------------------------
def test_mensaje_llegan_clientes( servidor_chat ):

    # --- Crear Clientes ---
    cliente_1 = Creat_client(servidor_chat)
    cliente_2 = Creat_client(servidor_chat)
    cliente_3 = Creat_client(servidor_chat)


    try:

        # --- Enviar Mensaje ---
        cliente_1.sendall(
            b"Hola pinguinos"
        )

        # --- Recibir Mensaje ---
        mensaje_2 = cliente_2.recv(1024)
        mensaje_3 = cliente_3.recv(1024)

        # --- Verificar Mensaje Obtenido ---
        assert mensaje_2 == b"Hola pinguinos"
        assert mensaje_3 == b"Hola pinguinos"

    
    finally:

        # --- Cerrar Conexiones ---
        cliente_1.close()
        cliente_2.close()
        cliente_3.close()


# ------------------------------
# EMISOR NO RECIBA SU MENSAJE
# ------------------------------
def test_emisor_no_recibe_mensaje(servidor_chat):

    # --- Crear Clientes ---
    cliente_1 = Creat_client(servidor_chat)
    cliente_2 = Creat_client(servidor_chat)


    try:
        # --- Mandar Mensaje ---
        cliente_1.sendall(
            b"Hola"
        )

        # --- Recibir Mensaje ---
        recibido = cliente_2.recv(1024)

        # --- Verificar Mensaje Recibido ---
        assert recibido == b"Hola"

        # --- Verificar Que Emisor No Obtuvo Su Mensaje ---
        with pytest.raises(socket.timeout): # Esperemos que ocurra un socket timeoutn
            cliente_1.recv(1024)

    finally:

        # --- Cerrar Conexiones
        cliente_1.close()
        cliente_2.close()


# --------------------------------------
# MULTTIPLS MENSAJES POR VARIOS CLIENTES
# --------------------------------------

def test_varios_clientes_envian_mensajes(
    servidor_chat
):
    # ---- Crear Clientes ---
    cliente_1 = Creat_client(servidor_chat)
    cliente_2 = Creat_client(servidor_chat)
    cliente_3 = Creat_client(servidor_chat)


    try:    
        # --- Enviar Primer Mensaje ---
        cliente_1.sendall(
            b"Mensaje-A"
        )
        # --- Recibir Mensaje ---
        datos_a = cliente_3.recv(1024)

        # --- Comprobar
        assert datos_a == b"Mensaje-A"

        # --- Enviar Segundo Mensje ---
        cliente_2.sendall(
            b"Mensaje-B"
        )

        # --- Recibir ---
        datos_b = cliente_3.recv(1024)

        # --- Comprobar
        assert datos_b == b"Mensaje-B"

    finally:
        # --- Cerrar Conexiones ---
        cliente_1.close()
        cliente_2.close()
        cliente_3.close()



# -------------------------------------
# MULTIPLES MENSAJES AL MISMO TIEMPO
# -------------------------------------

def test_varios_clientes_envian_simultaneamente(servidor_chat):

    # --- Crear Clientes ---
    clientes = [
        Creat_client(servidor_chat),
        Creat_client(servidor_chat),
        Creat_client(servidor_chat)
    ]

    # ---- Lista De Mensajes  ---
    mensajes = [
        "Mensaje del cliente 1",
        "Mensaje del cliente 2",
        "Mensaje del cliente 3"
    ]

    # --- Lista De Hilos ---
    hilos = []

    # --- ENVIAR LOS 3 MENSAJES AL MISMO TIEMPO ---

    for cliente, mensaje in zip(clientes, mensajes):

        # --- Crear Hilo Con La Mision De Enviar Mensaje ---
        hilo = threading.Thread(
            target=enviar_mensaje,
            args=(cliente, mensaje)
        )
        hilos.append(hilo)  # Guardar hilo.
        hilo.start()        # Iniciarlo.


    # --- Esperar A Que Terminen Todos Los Hilos ---
    for hilo in hilos:
        hilo.join()         # Espera a que termine la ejecucion del hilo.



    # --- COMPROBAR LOS MENSAJES RECIBIDOS ---

    for i, cliente in enumerate(clientes):


        # --- Recibir Mensajes Menos El Propio ---
        mensajes_esperados = [
            mensaje
            for j, mensaje in enumerate(mensajes)
            if i != j
        ]

        # --- Recibir Mensajes De Los Demas ---
        datos_recibidos = recibir_mensajes(
            cliente,
            mensajes_esperados
        )

        # Todos los mensajes esperados llegaron
        for mensaje in mensajes_esperados:
            assert mensaje in datos_recibidos

        # El cliente no recibió su propio mensaje
        assert mensajes[i] not in datos_recibidos

    # ----------------------------------------
    # CERRAR CLIENTES
    # ----------------------------------------

    for cliente in clientes:
        cliente.close()

    # El cliente 1 recibe los mensajes de 2 y 3
    # El cliente 2 recibe los mensajes de 1 y 3
    # El cliente 3 recibe los mensajes de 1 y 2




# ==========================================
# DESCONEXIONES
# ==========================================


# -------------------------------
#  UN CLIENTE SE DESCONECTA
# -------------------------------

def test_servidor_sigue_funcionando_si_cliente_se_desconecta(
    servidor_chat
):

    cliente_1 = Creat_client(servidor_chat)
    cliente_2 = Creat_client(servidor_chat)
    cliente_3 = Creat_client(servidor_chat)

    try:

        # El cliente 2 desaparece.
        cliente_2.close()

        # Cliente 1 sigue enviando.
        cliente_1.sendall(
            b"Sigues ahi?"
        )

        # Cliente 3 debería seguir recibiendo.
        mensaje = cliente_3.recv(1024)

        assert mensaje == b"Sigues ahi?"

    finally:

        cliente_1.close()
        cliente_3.close()


# --------------------------------
#  VARIOS CLIENTES SE DESCONECTAN
# --------------------------------

def test_varias_desconexiones_no_detienen_servidor(
    servidor_chat
):

    cliente_1 = Creat_client(servidor_chat)
    cliente_2 = Creat_client(servidor_chat)
    cliente_3 = Creat_client(servidor_chat)
    cliente_4 = Creat_client(servidor_chat)

    try:

        cliente_2.close()
        cliente_3.close()

        cliente_1.sendall(
            b"Servidor vivo"
        )

        mensaje = cliente_4.recv(1024)

        assert mensaje == b"Servidor vivo"

    finally:

        cliente_1.close()
        cliente_4.close()


# -------------------------------------------------------------
# SE CONECTA UN NUEVO CLIENTE LUEGO DE QUE OTRO SE DESCONECTO
# -------------------------------------------------------------
def test_nuevo_cliente_puede_conectarse_tras_desconexion(
    servidor_chat
):

    cliente_1 = Creat_client(servidor_chat)
    cliente_2 = Creat_client(servidor_chat)

    # Uno desaparece.
    cliente_2.close()

    # Nuevo cliente.
    cliente_3 = Creat_client(servidor_chat)

    try:

        cliente_1.sendall(
            b"Bienvenido"
        )

        mensaje = cliente_3.recv(1024)

        assert mensaje == b"Bienvenido"

    finally:

        cliente_1.close()
        cliente_3.close()