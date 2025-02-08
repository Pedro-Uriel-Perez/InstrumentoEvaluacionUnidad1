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
TRIG_PIN = 16  # Pin para el Trigger
ECHO_PIN = 4   # Pin para el Echo

# Configuración de LEDs
LED_ROJO = 2      # GPIO16
LED_AMARILLO = 5   # GPIO5
LED_VERDE = 18     # GPIO18

def setup_leds():
    """Inicializa los pines de los LEDs"""
    led_rojo = Pin(LED_ROJO, Pin.OUT)
    led_amarillo = Pin(LED_AMARILLO, Pin.OUT)
    led_verde = Pin(LED_VERDE, Pin.OUT)
    return led_rojo, led_amarillo, led_verde

def actualizar_leds(distancia, led_rojo, led_amarillo, led_verde):
    """Actualiza los LEDs según la distancia medida"""
    # Apagar todos los LEDs primero
    led_rojo.value(0)
    led_amarillo.value(0)
    led_verde.value(0)
    
    # Encender LED según la distancia
    if distancia < 20:  # Distancia cercana
        led_rojo.value(1)
    elif 20 <= distancia <= 50:  # Distancia media
        led_amarillo.value(1)
    else:  # Distancia lejana
        led_verde.value(1)

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
        client = MQTTClient(CLIENT_ID, MQTT_SERVER, MQTT_PORT, keepalive=30)
        client.connect(clean_session=True)
        print("Conectado a MQTT")
        return client
    except Exception as e:
        print(f"Error conectando a MQTT: {e}")
        return None

def main():
    try:
        # Inicializar pines del sensor
        trigger = Pin(TRIG_PIN, Pin.OUT)
        echo = Pin(ECHO_PIN, Pin.IN)
        
        # Inicializar LEDs
        led_rojo, led_amarillo, led_verde = setup_leds()
        
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
                    # Actualizar LEDs según la distancia
                    actualizar_leds(distancia, led_rojo, led_amarillo, led_verde)
                    
                    # Crear mensaje JSON
                    mensaje = {
                        "distancia": distancia,
                        "unidad": "cm"
                    }
                    
                    # Convertir a JSON y publicar
                    mensaje_json = json.dumps(mensaje)
                    print("Mensaje enviado:", mensaje_json)

                    try:
                        client.publish(MQTT_TOPIC, mensaje_json.encode())
                        print(f"Distancia medida: {distancia} cm")
                        client.ping()  # Mantener la conexión viva
                    except Exception as e:
                        print(f"Error publicando mensaje: {e}")
                        client = None  # Forzar reconexión
                
                time.sleep(2)  # Esperar 2 segundos entre mediciones
                
            except Exception as e:
                print(f"Error en el loop principal: {e}")
                client = None
                time.sleep(5)
                
    except Exception as e:
        print(f"Error fatal: {e}")
        reset()

if __name__ == "__main__":
    main()