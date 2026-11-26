from unittest.mock import MagicMock 

# --- Importar Funciones Criticas Del Servidor ---
from server import (add_client, delete_client, relay_message)   


# ==============================
# PRUEBAS UNITARIAS
# ==============================


# ----------------------------
# AGREGAR CLIENTE
# ----------------------------
def test_Add_Client():

    # Lista De CLientes
    clientes = []

    # Creamos Un Cliente Falso 
    cliente = MagicMock()

    # Agregamos EL Cliente
    add_client(clientes, cliente)

    # Nos aseguramos De Que Se Agrego El Cliente
    assert cliente  in clientes



# ----------------------------
# ELIMINAR CLIENTE
# ----------------------------
def test_Delete_Client():

    cliente = MagicMock()

    clientes = [cliente]

    delete_client(clientes, cliente)


    # --- Verificar Que Se Elmino Y Que Esta Cerrado ---
    assert cliente not in clientes
    cliente.close.assert_called_once()



# ----------------------------
# RETRANSMITIR MENSAJE
# ----------------------------
def test_Relay_Message():

    servidor = MagicMock()

    emisor = MagicMock()

    cliente_2 = MagicMock()
    cliente_3 = MagicMock()

    clientes = [servidor, emisor, cliente_2, cliente_3]

    relay_message(clientes, servidor, emisor, "Hola")


    # --- Verificar Que Se Transmitio El Mensaje ---
    cliente_2.send.assert_called_once_with(b"Hola")

    cliente_3.send.assert_called_once_with(b"Hola")



# ------------------------------
# EMISOR NO RECIBE SU MENSAJE
# ------------------------------
def test_Sender_Not_Message():

    servidor = MagicMock()

    emisor = MagicMock()

    cliente_2 = MagicMock()
    cliente_3 = MagicMock()

    clientes = [servidor, emisor, cliente_2, cliente_3]

    relay_message(clientes, servidor, emisor, "Hola")

    # --- Verifico Mensaje Al Emisor ---
    emisor.send.assert_not_called()



# ----------------------------
# SERVIDOR NO RECIBE MENSAJE
# ----------------------------
def test_Server_Not_Message():

    servidor = MagicMock()

    emisor = MagicMock()

    cliente_2 = MagicMock()
    cliente_3 = MagicMock()

    clientes = [servidor, emisor, cliente_2, cliente_3]

    relay_message(clientes, servidor, emisor, "Hola")

    # --- Verifico Mensaje Al Servidor ---
    servidor.send.assert_not_called()