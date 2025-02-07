# Instrumento de Evaluación Unidad I
Instrumento de evaluación de la Unidad I de la materia Aplicaciones de IoT 

## Información
- **Alumno:** Pedro Uriel Pérez Monzón
- **Grupo:** GDS0653
- **N.Control:**  1223100428
- **Materia:**  Aplicaciones de IoT

# PARTE PRÁCTICA
## Almacenamiento de Datos y Control de Actuadores 

# Video Demostrativo
https://drive.google.com/drive/folders/1kxQg-n06zx9qULW40_sXRukujDZvkuuc?usp=sharing
# Codigo JSON 
```json
[
    {
        "id": "98b13d5a7684b802",
        "type": "tab",
        "label": "Flow 1",
        "disabled": false,
        "info": "",
        "env": []
    },
    {
        "id": "mqtt-in",
        "type": "mqtt in",
        "z": "98b13d5a7684b802",
        "name": "Sensor Proximidad",
        "topic": "sensor/proximidad",
        "qos": "2",
        "datatype": "json",
        "broker": "2249adb74cf55197",
        "nl": false,
        "rap": false,
        "inputs": 0,
        "x": 110,
        "y": 100,
        "wires": [
            [
                "76307f6e632c54d4",
                "prepare-data"
            ]
        ]
    },
    {
    "id": "prepare-data",
    "type": "function",
    "z": "98b13d5a7684b802",
    "name": "Preparar datos",
    "func": "if (msg.payload && msg.payload.distancia) {\n    msg.topic = \"INSERT INTO sensor_details(sensor_id, user_id, value) VALUES($1, $2, $3)\";\n    msg.params = [1, 1, msg.payload.distancia];\n    return msg;\n} else {\n    return null;\n}",
    "outputs": 1,
    "timeout": "",
    "noerr": 0,
    "initialize": "",
    "finalize": "",
    "libs": [],
    "x": 420,
    "y": 100,
    "wires": [
        [
            "postgres"
        ]
    ]
},

    {
        "id": "postgres",
        "type": "postgresql",
        "z": "98b13d5a7684b802",
        "name": "Guardar en PostgreSQL",
        "query": "INSERT INTO sensor_details(sensor_id, user_id, value) VALUES($1, $2, $3)\n",
        "postgreSQLConfig": "209c199c9ecea50f",
        "split": false,
        "rowsPerMsg": "",
        "outputs": 1,
        "x": 650,
        "y": 100,
        "wires": [
            [
                "debug"
            ]
        ]
    },
    {
        "id": "debug",
        "type": "debug",
        "z": "98b13d5a7684b802",
        "name": "Final Debug",
        "active": true,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "true",
        "targetType": "full",
        "statusVal": "",
        "statusType": "auto",
        "x": 890,
        "y": 100,
        "wires": []
    },
    {
        "id": "76307f6e632c54d4",
        "type": "debug",
        "z": "98b13d5a7684b802",
        "name": "MQTT Raw",
        "active": false,
        "tosidebar": true,
        "console": false,
        "tostatus": false,
        "complete": "true",
        "targetType": "full",
        "statusVal": "",
        "statusType": "auto",
        "x": 290,
        "y": 180,
        "wires": []
    },
    {
        "id": "2249adb74cf55197",
        "type": "mqtt-broker",
        "name": "",
        "broker": "broker.emqx.io",
        "port": 1883,
        "clientid": "",
        "autoConnect": true,
        "usetls": false,
        "protocolVersion": 4,
        "keepalive": 60,
        "cleansession": true,
        "autoUnsubscribe": true,
        "birthTopic": "",
        "birthQos": "0",
        "birthRetain": "false",
        "birthPayload": "",
        "birthMsg": {},
        "closeTopic": "",
        "closeQos": "0",
        "closeRetain": "false",
        "closePayload": "",
        "closeMsg": {},
        "willTopic": "",
        "willQos": "0",
        "willRetain": "false",
        "willPayload": "",
        "willMsg": {},
        "userProps": "",
        "sessionExpiry": ""
    },
    {
        "id": "209c199c9ecea50f",
        "type": "postgreSQLConfig",
        "name": "",
        "host": "192.168.200.162",
        "hostFieldType": "str",
        "port": 5432,
        "portFieldType": "num",
        "database": "aiot",
        "databaseFieldType": "str",
        "ssl": "false",
        "sslFieldType": "bool",
        "applicationName": "",
        "applicationNameType": "str",
        "max": 10,
        "maxFieldType": "num",
        "idle": 1000,
        "idleFieldType": "num",
        "connectionTimeout": 10000,
        "connectionTimeoutFieldType": "num",
        "user": "utng",
        "userFieldType": "str",
        "password": "1234",
        "passwordFieldType": "str"
    }
]
```
# Codigo Python
```python
from machine import Pin, time_pulse_us, reset
import network
import time
from umqtt.robust import MQTTClient  
import json

# Configuración WiFi
SSID = "MORENO"
PASSWORD = "MMPM0607"

# Configuración MQTT
MQTT_SERVER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = b"sensor/proximidad"
CLIENT_ID = "ESP32Client"

# Configuración del sensor HC-SR04
TRIG_PIN = 16
ECHO_PIN = 4

def conectar_wifi():
    """Conecta el ESP32 a la red WiFi"""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando a WiFi...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(0.5)
            print('.', end='')
    print('\nConectado a WiFi')
    print('Dirección IP:', wlan.ifconfig()[0])

def medir_distancia(trigger, echo):
    """Mide la distancia usando el sensor HC-SR04"""
    try:
        # Enviar pulso
        trigger.value(0)
        time.sleep_us(2)
        trigger.value(1)
        time.sleep_us(10)
        trigger.value(0)
        
        # Medir el tiempo del pulso
        duration = time_pulse_us(echo, 1, 30000)  # Timeout de 30ms
        
        # Calcular distancia en cm
        if duration > 0:
            distance = duration * 0.034 / 2
            return distance
        return None
    except Exception as e:
        print(f"Error midiendo distancia: {e}")
        return None

def conectar_mqtt():
    """Conecta al broker MQTT y retorna el cliente"""
    try:
        # Usar MQTTClient de umqtt.robust
        client = MQTTClient(CLIENT_ID, MQTT_SERVER, MQTT_PORT, keepalive=30)
        client.connect(clean_session=True)
        print("Conectado a MQTT")
        return client
    except Exception as e:
        print(f"Error conectando a MQTT: {e}")
        return None

def main():
    try:
        # Inicializar pines
        trigger = Pin(TRIG_PIN, Pin.OUT)
        echo = Pin(ECHO_PIN, Pin.IN)
        
        # Conectar a WiFi
        conectar_wifi()
        
        # Iniciar cliente MQTT
        client = None
        reconnect_count = 0
        
        while True:
            try:
                # Reconectar MQTT si es necesario
                if client is None:
                    if reconnect_count >= 3:
                        print("Demasiados intentos de reconexión, reiniciando...")
                        reset()
                    client = conectar_mqtt()
                    if client is None:
                        reconnect_count += 1
                        time.sleep(5)
                        continue
                    reconnect_count = 0
                
                # Medir distancia
                distancia = medir_distancia(trigger, echo)
                
                if distancia is not None:
                    # Crear mensaje JSON
                    mensaje = {
                        "sensor": "proximidad",
                        "distancia": distancia,
                        "unidad": "cm",
                        "timestamp": time.time()
                    }
                    
                    # Convertir a JSON y publicar
                    mensaje_json = json.dumps(mensaje)
                    print("Mensaje enviado:", mensaje_json)  # Añadir este print para debug

                    try:
                        client.publish(MQTT_TOPIC, mensaje_json.encode())
                        print(f"Distancia medida: {distancia} cm")
                        client.ping()  # Mantener la conexión viva
                    except Exception as e:
                        print(f"Error publicando mensaje: {e}")
                        client = None  # Forzar reconexión
                
                time.sleep(5)  # Esperar 5 segundos entre mediciones
                
            except Exception as e:
                print(f"Error en el loop principal: {e}")
                client = None
                time.sleep(5)	
                
    except Exception as e:
        print(f"Error fatal: {e}")
        reset()

if __name__ == "__main__":
    main()

```
# Base de Datos Postgres
```postgres
-- Tabla de usuarios
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100),
    clave VARCHAR(255),
    record_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de sensores
CREATE TABLE sensors (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    type VARCHAR(50),
    record_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de detalles de sensores
CREATE TABLE sensor_details (
    id SERIAL PRIMARY KEY,
    sensor_id INTEGER REFERENCES sensors(id),
    user_id INTEGER REFERENCES users(id),
    value VARCHAR(50),
    record_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de actuadores
CREATE TABLE actuators (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    type VARCHAR(50),
    record_at TIMESTAMP DEFAULT NOW()
);

-- Tabla de detalles de actuadores
CREATE TABLE actuator_details (
    id SERIAL PRIMARY KEY,
    actuator_id INTEGER REFERENCES actuators(id),
    user_id INTEGER REFERENCES users(id),
    state VARCHAR(50),
    record_at TIMESTAMP DEFAULT NOW()
);
```

# Materiales utilizados
| Material                | Imagen                                                                 
|-------------------------|-----------------------------------------------------------------------|
| ESP32                   | <img src="https://github.com/user-attachments/assets/f3099b50-c652-436f-bd88-ca77c850709a" width="150" /> |
| Sensor HC-SR04           | <img src="https://www.geekfactory.mx/wp-content/uploads/pinout-o-patillaje-sensor-hc-sr04.jpg" width="150" />    |
| Protoboard              | <img src="https://github.com/user-attachments/assets/0870c689-bc56-420d-8460-bae81f7221cb" width="150" />     |
| Boton              | <img src="https://github.com/user-attachments/assets/0689a889-53df-4bf9-b9a7-76cee842c42c" width="150" />     |





# CRUD en PostgreSQL
# https://drive.google.com/drive/folders/1VB7PM8NzoIkO7pQpWmZ1pTyqPlA6zpBx?usp=sharing

# Videos Demostrativos de los ejercicios individuales

# [Button_gpiozero](https://drive.google.com/file/d/1-m9GogI56a76HYkOtml2_t5jZCQIheaJ/view?usp=drive_link)
# [Button_pigpio](https://drive.google.com/file/d/18eZWBnwjZnYfZdq-M8H7aB1pzH8Ae0TH/view?usp=drive_link)
# [Led_pigpio](https://drive.google.com/file/d/149ihfkejvCFi8UhSLwsAaRnA7x8RPFOw/view?usp=drive_link)
# [Let_gpiozero](https://drive.google.com/file/d/1TsMygmEtwHeRLzsCJyU1b-1Jx806XAPY/view?usp=drive_link)
# [Instalación y Configuraciones Básicas](https://drive.google.com/file/d/16CI9v2FEhKU4_qPN3p96XlsLyfAJSfV5/view?usp=drive_link)
# [Configuración de un sistema de publicación y suscripción con Mosquitt](Aqui va el video)




# Figura Copa
<img src="https://github.com/user-attachments/assets/097c481a-faf7-4c37-9366-7346c1529388" alt="Oogie Boogie" width="250">



## Soldadura de Placa Fenólica
| Imagen Uno | Imagen Dos |
|----------|----------|
|![Imagen de WhatsApp 2025-02-07 a las 10 42 37_f6588a44](https://github.com/user-attachments/assets/8358b9a9-5d39-4583-8421-015ac53ab32a)|![Imagen de WhatsApp 2025-02-07 a las 10 42 37_b0a23419](https://github.com/user-attachments/assets/ab02f694-28e6-4401-93b9-dbaf6842f64a)|



## Capturas de Evaluaciones de Curso de Python Fundamentals 2

### Examen Módulo 1
<img src="https://github.com/user-attachments/assets/7e11ba68-8f1e-4caf-8794-24062e94e0a5" width="600" alt="Examen Módulo 2"/>

### Examen Módulo 2
<img src="https://github.com/user-attachments/assets/69f90d62-b551-4d26-9eb6-00987526e710" width="600" alt="Examen Módulo 2"/>

### Examen Módulo 3
<img src="https://github.com/user-attachments/assets/b1d92df8-e08d-42da-bc9d-07a141cbc2fd" width="600" alt="Examen Módulo 3"/>

### Examen Módulo 4
<img src="https://github.com/user-attachments/assets/00db0fc9-06d9-4791-aaee-b55e8c545136" width="600" alt="Examen Módulo 4"/>

### Examen Final
<img src="https://github.com/user-attachments/assets/5565fe5a-6f70-430a-a690-2039a3366f35" width="600" alt="Examen Final"/>
