# 🐧 Testing Fest — "El Chat Indestructible" 🧪🛡️

> "If it isn't tested, it's broken. You just don't know it yet."

Multi-client TCP chat server built with Python sockets and `select`, backed by unit, integration and disconnection tests with Pytest.

---

## 🎬 Description

This project takes a real-time chat application and puts it through a full testing process.

The chat is a TCP server that accepts multiple clients and relays every message to everyone except the sender. The focus of the project is not the chat itself, but proving that it works: that messages arrive, that nothing is lost or duplicated, and that the server survives clients disappearing mid-conversation.

The system includes:

- A single-threaded chat server based on `select`
- A console client with automatic reconnection
- A message validation module
- A test suite with unit, integration and disconnection scenarios
- A code coverage report

---

## 🧠 Objective

Practice software testing on a networked application:

- Unit testing with Pytest and mocks
- Test-Driven Development (Red → Green → Refactor)
- Integration testing with real sockets and multiple clients
- Concurrency scenarios (simultaneous senders)
- Fault tolerance (abrupt client disconnections)
- Positive and negative test cases
- Code coverage measurement

---

## 🛠️ Technologies Used

### Application
- **Python**
- **socket** (TCP communication)
- **select** (multiplexing multiple connections without threads)
- **threading** (client send/receive)

### Testing
- **Pytest**
- **pytest-cov** (coverage)
- **unittest.mock** (`MagicMock` for isolated unit tests)

---

## 🧩 System Architecture

```text
 Client 1 ─┐
 Client 2 ─┼──►  Chat Server  ──►  Validation  ──►  Relay to the others
 Client 3 ─┘     (select loop)     (chat/validation.py)
```

| Component | Responsibility |
|---|---|
| `server.py` | Accepts connections, validates incoming messages, relays them and cleans up disconnected clients |
| `chat/validation.py` | Decides whether a message is acceptable |
| `client.py` | Interactive client: connects with retries, sends and receives concurrently |

The server logic is split into small, testable functions (`add_client`, `delete_client`, `relay_message`) so they can be verified in isolation with mocks.

---

## ⚙️ How It Works

### 🔹 General Flow

1. The server starts listening and waits for connections using `select`.
2. A new client connects and is added to the list of active sockets.
3. A client sends a message.
4. The server validates it. Invalid messages are discarded.
5. Valid messages are relayed to every other client (never to the sender).
6. If a client disconnects or its socket fails, it is removed and closed. The rest keep chatting.

### 🔹 Message Validation Rules

| Rule | Result |
|---|---|
| Not a string (`None`, number) | Rejected |
| Empty message | Rejected |
| Only whitespace | Rejected |
| Longer than 1024 characters | Rejected |
| 1 to 1024 characters | Accepted |

---

## 🧪 Testing Strategy

The suite has **21 tests** across three layers:

| Layer | File | Tests | What it verifies |
|---|---|---|---|
| Unit — validation | `tests/test_validation.py` | 8 | Valid, boundary (1 and 1024 chars), empty, whitespace-only, too long, `None` and non-string messages |
| Unit — server logic | `tests/test_server.py` | 5 | Add/remove client, relay to all others, sender and server excluded (using mocks) |
| Integration | `tests/test_integration.py` | 8 | Real server in a thread with real client sockets |

### 🔹 Integration Scenarios

- Multiple clients connect at the same time
- A message from one client reaches all the others
- The sender does not receive its own message
- Several clients send messages in sequence and simultaneously (threads)
- No message is lost or duplicated
- A client disconnects abruptly and the others keep working
- Several clients disconnect and the server stays alive
- A new client connects after a disconnection and chats normally

Each test starts its own server through a Pytest fixture and shuts it down afterwards, so tests are independent of each other.

### 🔴🟢🔵 TDD

Message validation was developed following the Red-Green-Refactor cycle:

1. **Red** — write a test for rejecting whitespace-only messages and watch it fail.
2. **Green** — add the minimum code to make it pass.
3. **Refactor** — clean the validation function without changing its behavior.

---

## 📊 Results & Coverage

| File | Coverage |
|---|---:|
| `chat/validation.py` | 100% |
| `server.py` | 89% |
| `client.py` | 0% |

- **Overall: ~80%** as reported by `pytest-cov` (test files included in the total).
- **Server + validation only: ~91%.**
- `client.py` is not covered: it depends on console `input()` and an endless loop, which makes it hard to test without refactoring.

Test progress and decisions are recorded in [`TESTING.md`](TESTING.md).

---

## 📂 Project Structure

```text
Reto 11 - Testing/

├── chat/
│   ├── __init__.py
│   └── validation.py
│
├── tests/
│   ├── __init__.py
│   ├── test_validation.py
│   ├── test_server.py
│   └── test_integration.py
│
├── client.py
├── server.py
├── TESTING.md
└── README.md
```

---

## 🚀 Installation

### 1. Clone repository

```bash
git clone <repository-url>
cd "Reto 11 - Testing"
```

### 2. Install test dependencies

The chat itself only uses the standard library. For the tests:

```bash
pip install pytest pytest-cov
```

---

## ▶️ Usage

### Run the chat

Start the server:

```bash
python server.py
```

Open one or more terminals and start a client in each:

```bash
python client.py
```

The server listens on `localhost:8000`. Type a message in any client and press Enter to broadcast it.

### Run the tests

From the project root:

```bash
pytest -v
```

### Run with coverage

```bash
pytest --cov=. --cov-report=term-missing
```

Generate an HTML report:

```bash
pytest --cov=. --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

---

## 📈 Key Features

✔ Multi-client TCP chat with `select`  
✔ Message validation module  
✔ Automatic client reconnection (10 attempts)  
✔ Unit tests with mocks  
✔ Integration tests with real sockets  
✔ Simultaneous sender scenarios  
✔ Abrupt disconnection scenarios  
✔ Positive and negative test cases  
✔ TDD applied to message validation  
✔ Independent tests with fixture-managed server lifecycle  
✔ Code coverage report  

---

## 🧃 Possible Improvements

- Cover `client.py` by separating the I/O from the logic and testing it with mocks
- Make `iniciar_servidor` honor its `host` and `puerto` parameters (the tests could then use a free port instead of `8000`)
- Handle failures while relaying to a dead client without dropping the sender
- Replace timing-based waits in integration tests with an explicit "server has registered the client" check
- Add a message framing protocol (TCP is a byte stream, so messages can merge)
- Enforce a coverage threshold with `--cov-fail-under=80`
- Add a single command or script to run lint, tests and coverage
- Add CI with GitHub Actions
- Add `.coverage` and `htmlcov/` to `.gitignore`

---

## 👨‍💻 Author

**Juan Castro**

---

# 🇪🇸 Resumen en Español

Este proyecto toma una aplicación de chat en tiempo real y la somete a un proceso completo de pruebas automatizadas.

El chat es un servidor TCP que acepta múltiples clientes y retransmite cada mensaje a todos menos al emisor. Lo importante no es el chat en sí, sino demostrar que funciona: que los mensajes llegan, que no se pierden ni se duplican y que el servidor sobrevive cuando un cliente se desconecta de golpe.

---

## 🎯 Objetivo

El proyecto fue desarrollado para practicar:

- pruebas unitarias con Pytest y mocks,
- desarrollo guiado por pruebas (TDD: Red, Green, Refactor),
- pruebas de integración con sockets reales y varios clientes,
- escenarios de concurrencia con varios clientes enviando a la vez,
- tolerancia a fallos ante desconexiones inesperadas,
- casos de prueba positivos y negativos,
- medición de cobertura de código.

---

## ⚙️ Funcionamiento

- El servidor escucha conexiones con `select` y mantiene una lista de clientes activos.
- Cada mensaje recibido se valida (no vacío, no solo espacios, máximo 1024 caracteres, tipo texto).
- Los mensajes válidos se retransmiten a todos los clientes excepto al emisor.
- Si un cliente se desconecta, el servidor lo elimina y sigue funcionando con los demás.
- Las pruebas levantan un servidor real en un hilo, conectan clientes reales y verifican el comportamiento extremo a extremo.

---

## 📊 Características destacadas

- 21 pruebas automatizadas en tres capas (validación, lógica del servidor e integración)
- Pruebas unitarias aisladas con mocks
- Pruebas de integración con varios clientes y envíos simultáneos
- Pruebas de desconexión abrupta de uno o varios clientes
- TDD aplicado a la validación de mensajes
- Informe de cobertura: ~80% global, 89% en el servidor y 100% en la validación

---

## 🧠 Conclusión

El proyecto demuestra cómo probar una aplicación de red de forma estructurada: pruebas pequeñas y aisladas para la lógica, pruebas de integración para el comportamiento real y escenarios de fallo para comprobar la robustez.

Este enfoque permite:
- detectar errores antes de que lleguen a los usuarios,
- refactorizar con seguridad gracias a las pruebas,
- garantizar que el servidor soporta varios clientes y desconexiones inesperadas,
- y medir con datos cuánto del código está realmente verificado.
