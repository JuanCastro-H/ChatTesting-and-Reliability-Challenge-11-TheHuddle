# --- Numero Maximo De Mensajes ---

MAX_MESSAGE_LENGTH = 1024

# -------------------------------------------
# --- Valida Un Mensaje Antes De Enviarlo ---
# -------------------------------------------

def validateMessage (message):

    # ===== Verifica Que El Contenido Del Mensaje Sea Str =====
    if not isinstance(message, str):
        return False # Lo rechaza si no es texto

    
    # --- Si No Hay Mensaje ---
    # ==========================================
    if  not message:
        return False
    # ==========================================
    


    """# ===== Si No Hay Mensaje O Esta Compuesto De Espacios =====
    if  not message or not message.strip():
        return False
    """


    # --- Si Es Mas Grande Que El Limite ---
    if len(message) > MAX_MESSAGE_LENGTH:
        return False

    # --- Todo Correcto ---
    return True


