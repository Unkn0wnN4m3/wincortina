# Wincortina

<p align="center">
  <img src="./media/wincortina.png", alt="wincortina logo">
</p>

Put this code inside `pyrightconfig.json`. Change what's inside `".venv"` to
your own venv

```json
{
  "venvPath": ".",
  "venv": ".venv",
  "extraPaths": ["./lib"]
}
```

Wi-Fi config fille should be named: `config_wifi.py` with the following content:

```python
WIFI_CONFIG = {
    "ssid": "your_ssid",
    "password": "your_password",
}
```

- servo library from [TTitanUA/micropython_servo_pdm_360](https://github.com/TTitanUA/micropython_servo_pdm_360)
- rest server library from [pimoroni/phew](https://github.com/pimoroni/phew)
