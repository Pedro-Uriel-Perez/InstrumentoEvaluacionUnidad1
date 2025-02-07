# Instrumento de Evaluación Unidad I
Instrumento de evaluación de la Unidad I de la materia Aplicaciones de IoT 

## Información
- **Alumno:** Pedro Uriel Pérez Monzón
- **Grupo:** GDS0643
- **N.Control:**  1223100428
- **Materia:**  Aplicaciones de IoT


# Almacenamiento de Datos
Diseña un sistema IoT que capture datos desde un sensor (libre elección) y los almacene en:
Base de datos PostgreSQL mediante Node-RED.
# Video Demostrativo
https://drive.google.com/drive/folders/1kxQg-n06zx9qULW40_sXRukujDZvkuuc?usp=sharing
# Codigos
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
        "func": "if (msg.payload && msg.payload.distancia) {\n    msg.topic = \"INSERT INTO sensor_details(sensor_id, user_id, value) VALUES($1, $2, $3)\";\n    msg.params = [1, 1, msg.payload.distancia];
   return msg;\n} else {\n    return null;\n}\n",
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

-Python
-Node-red
-BD Postgres

# Materiales utilizados
| Material                | Imagen                                                                 
|-------------------------|-----------------------------------------------------------------------|
| ESP32                   | <img src="https://github.com/user-attachments/assets/f3099b50-c652-436f-bd88-ca77c850709a" width="150" /> |
| Sensor HC-SR04           | <img src="https://www.geekfactory.mx/wp-content/uploads/pinout-o-patillaje-sensor-hc-sr04.jpg" width="150" />    |
| Protoboard              | <img src="https://github.com/user-attachments/assets/0870c689-bc56-420d-8460-bae81f7221cb" width="150" />     |


## INFORMACION AQUI
https://drive.google.com/drive/folders/1X6jZeg_6ULijYEA6FLuTeC4TZpiH4qyW?usp=drive_link

# INFORMACION AQUI
https://drive.google.com/drive/folders/1jpgsMl4b6JE_hzsYOiqz5bL08U3oIH16?usp=drive_link

## Materiales utilizados:







# CRUD en PostgreSQL
https://drive.google.com/drive/folders/1VB7PM8NzoIkO7pQpWmZ1pTyqPlA6zpBx?usp=sharing

## Videos Demostrativos de los 4 videos
# Button_gpiozero, Button_pigpio, Led_pigpio, Let_gpiozero
https://drive.google.com/drive/folders/1no93ATnBk6CoKC8oaRVlQJa56m7xKZ6H?usp=sharing

# Para poner videos
https://vm.tiktok.com/ZMke2V9HD/

# Figura Copa
<img src="https://github.com/user-attachments/assets/097c481a-faf7-4c37-9366-7346c1529388" alt="Oogie Boogie" width="250">

# Soldadura de placa
<img src="https://github.com/user-attachments/assets/8358b9a9-5d39-4583-8421-015ac53ab32a" alt="Oogie Boogie" width="250">




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
<img src="https://github.com/user-attachments/assets/2131cd27-90c1-4b1e-8cec-dbcb908872e4" width="600" alt="Examen Final"/>
