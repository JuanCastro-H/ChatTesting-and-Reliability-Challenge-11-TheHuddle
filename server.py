#=====================================================
# BLOQUE 1: LIBRERIAS
#=====================================================
import socket # Libreria que proporciona las funciones y clases necesarias para crear y manipular sockets
import select # Función que permite vigilar múltiples sockets simultaneamente para realizar alguna operación (leer, escribir o detectar errores), sin necesidad de usar hilos.


#=====================================
# BLOQUE 2: CONFIGURACION INICIAL
#=====================================
HOST = 'localhost' # 127.0.0.1
PUERTO = 8000 # para desarrollo local 




# =====================================
# FUNCIONES CRITICAS REFACTORIZADAS 
# =====================================


# --- Obtener Funcion Para Validar Mensaje --
from chat.validation import validateMessage

# --- Agregar Cliente ---
def add_client(clientes, cliente):
    clientes.append(cliente)



# --- Eliminar Cliente ---
def delete_client(clientes, cliente):

    # Buscar Sokect Y Removerlo De la Lista
    if cliente in clientes:
        clientes.remove(cliente) 

    # Elimina El Sokect De Ese Cliente
    cliente.close()



# --- Retransmitir Mensaje ---
def relay_message(clientes, servidor, emisor, mensaje):

    # --- Recorrer Sokects De Clientes ---
    for cliente in clientes: 

        # --- Enviar Mensaje A Todos Menos Servidor Y Emisor ---
        if cliente != servidor and cliente != emisor:
            cliente.send(mensaje.encode()) # En bytes.



# --- SERVIDOR ---
def iniciar_servidor(host=HOST, puerto=PUERTO, stop_event=None, ready_event=None, puerto_real=None):


    # ------------------------------------------------------
    # BLOQUE 3: CREACION Y CONFIGURACION DEL SOCKET SERVIDOR
    # ------------------------------------------------------


    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # Crear sokect, conexionIPV4, tipo TCP 


    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # configurar las opcion internsa del socket. sol socket nivel donde se aplica la opcion a nivel de socket no del protoclo, en el servidor para reutilizar el host y puerto 

    servidor.bind((HOST, PUERTO))                                   # Asocia el socket a una direccion IP y Puerto (con .bind)

    servidor.listen()                                               # basicamente le dice al sistema, estoy listo para recibir conexiones, empieza a escuchar modo servidor pasivo, pero aun no acepta ninguna conexion


    # --- Lista De Sokect Manejados ---
    clientes = [servidor] 

    # --- Obtiene El Puerto Real ---
    puerto_asignado = servidor.getsockname()[1]

    
    if puerto_real is not None:
        puerto_real.append(puerto_asignado)

    # Imprime datos del puerto y anfritrion
    print(f"[🎧] Servidor escuchando en {HOST}:{PUERTO}")


    # --- Avisamos Al Test Que EL Servidor Esta Preparado ---
    if ready_event is not None:
        ready_event.set()




    # ------------------------------------------------------------
    # BLOQUE 4: BUCLE PRINCIPAL DEL SERVIDOR
    # SELECT Y MANEJO DE EVENTOS
    # ------------------------------------------------------------

    try: 

        # --- Bucle que mantiene vivo el servidor ---
        while stop_event is None or not stop_event.is_set():  

                
                #---------------------------------
                # El corazon del servidor
                #---------------------------------

                sockets_listos, _, excepciones = select.select(clientes, [], clientes, 0.1) # select.select basicamente le pregunta al sistema cuando un socket este listo para hacer algo
#                ↑               ↑               ↑                                      └──   Espera Como Maximo 0.1 segundos entre cada analisis, por si se detiene el servidor.                    
#                |               |               └── Lista de sockets con errores o estados excepcionales.
#                |               └────────────────── Lista de sockets "listos para escribir" (DESCARTADA).
#                └────────────────────────────────── Lista de sockets "listos para leer" (incluye servidor y clientes).

                #------------------------------------------------
                # Manejo de conexiones nuevas y sockets listos
                #------------------------------------------------

                for sock in sockets_listos:

                    # --------------------------
                    # NUEVA CONEXIÓN
                    # --------------------------
                    if sock == servidor:                               # Hay una nueva conexcion entrante
                        cliente_socket, direccion = servidor.accept()  # acepts acepta la conexion y se crea un nuevo socket exclusivo para este cliente (cliente socket) y se guarda su direccion IP en la variable direccion

                        # --- Agregar Sokect Del Cliente ---
                        add_client(clientes, cliente_socket)

                        print(f"[+] Nuevo cliente conectado desde {direccion}")



                    #----------------------------------
                    # Manejo de mensajes de clientes
                    #---------------------------------

                    else: # Si el socket no es el Servidor entonces es un cliente

                        try:
                            mensaje = sock.recv(1024).decode() # Recibe hasta 1024 bytes de infromacion que transforma a texto
                            
                            if not mensaje: # Detecta si el cliente se desconecto
                                raise Exception("Cliente desconectado")


                            # --- Mensaje Invalido ---
                            if not validateMessage(mensaje):
                                print("[⚠️] Mensaje inválido.")
                                continue


                            # --- Imprime EL Mensaje Recibido ---
                            print(f"[SMS] Mensaje recibido: {mensaje}")

                            # --- Retrasmitir Mensaje ---
                            relay_message(clientes, servidor, sock, mensaje)



                        # ---------------------------
                        # Manejo de desconexiones
                        # ---------------------------
                        except Exception: 

                            print("[!] Cliente desconectado")
                            delete_client(clientes, sock)      # Eliminar y cerrar Socket 


                #--------------------------------
                # SOCKETS CON ERROR
                #--------------------------------
                for sock in excepciones:           # Toma al socket de la lista
                    delete_client(clientes, sock)  # Elimina y cierra el Socket 



    finally:

        # --- Cerrar Todos Los Clientes ---
        for sock in clientes[:]:

            try:
                sock.close()

            except  OSError:
                pass


        print("[🔚] Servidor detenido.")




if __name__ == "__main__":
    iniciar_servidor()