import uasyncio
from curtain import Curtain
from light_sensor import LightSensor

import config


async def get_light_value():
    threshold = 1.5  # Umbral en voltios (1.5V)
    previous_above_threshold = None  # Inicialmente desconocido

    lig = LightSensor(config.LIGHT_SENSOR_PIN)
    cur = Curtain(config.SERVO_PIN)

    while True:
        value = lig.get_value()
        print(f"Light Sensor Value: {value}V")  # Print the LDR value

        # Determinar si el valor actual está por encima del umbral
        current_above_threshold = value > threshold

        # Detectar cambios en el estado del umbral
        if previous_above_threshold is not None:  # Ignorar la primera lectura
            if current_above_threshold and not previous_above_threshold:
                # Cambio de abajo hacia arriba del umbral
                print("Light increased above threshold - Opening curtain")
                cur.curtain_open()
            elif not current_above_threshold and previous_above_threshold:
                # Cambio de arriba hacia abajo del umbral
                print("Light decreased below threshold - Stopping curtain")
                cur.curtain_close()

        # Actualizar el estado anterior
        previous_above_threshold = current_above_threshold

        await uasyncio.sleep_ms(300)  # Non-blocking delay
