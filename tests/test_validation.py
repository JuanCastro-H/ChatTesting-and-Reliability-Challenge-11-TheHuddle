# --- Importar La Funcion De Validar Mensaje ---
from chat.validation import validateMessage


# ==============================
# PRUEBAS UNITARIAS
# ==============================


# ----------------------
# CASOS POSITIVOS
# ----------------------


# --- Mensaje Valido ---
def test_ValidMessage():
    assert validateMessage("Hola mundo") is True # Si la funcion devuelve un resultado Inesperado
                                                #  Como False, deten el programa y avisame del fallo. 


# --- Mensaje Con Maximo De Caracteres ---
def test_Message1024Caracher():
    message = "a" * 1024

    assert validateMessage(message) is True


# --- Mensaje Corto ---
def test_MessageShort():
    assert validateMessage("A") is True



# -----------------------------
# CASOS NEGATIVOS
# -----------------------------

# --- Mensaje Vacio ---
def test_EmptyMessage():
    assert validateMessage("") is False


# ===== Mesaje Con Puros Espacios =====
def test_MessageSpacesOnly():
    assert validateMessage("    ") is False


# --- Mensaje Demasiado Largo ---
def test_MessageTooLong():
    message = "a" * 1025

    assert validateMessage(message) is False


# --- Mensaje None ---
def test_MessageNone():
    assert validateMessage(None) is False


# --- Mensaje No Es String --
def test_MessageNotString():
    assert validateMessage(12345) is False