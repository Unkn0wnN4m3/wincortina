import gc

import config
import curtain

if __name__ == "__main__":
    c = None

    try:
        c = curtain.Curtain(config.SERVO_PIN, config.LIGHT_SENSOR_PIN, 16)
        c.start()
    except KeyboardInterrupt:
        print("System interrumpet by the user")
    except Exception as e:
        print(f"Fatal erro: {e}")
    finally:
        if c:
            c.stop()
        gc.collect()
