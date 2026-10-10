# bluetored-android

Turns blue into red on an Android phone's entire screen. A Python script on your
PC sends a color matrix to Android's compositor (SurfaceFlinger) over adb.

## Setup

1. Install [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) so `adb` is on your PATH.
2. On the phone, enable Developer options (tap Build number 7 times), then turn on USB debugging.
3. Connect via USB and accept the debugging prompt.

## Run

```
python bluetored_android.py swap       # red and blue trade places (default)
python bluetored_android.py blue2red   # blue becomes red, reds stay red
python bluetored_android.py off        # restore normal colors
```

The effect resets when the phone reboots. For wireless use, pair with
`adb pair` / `adb connect` (Android 11+, Developer options > Wireless debugging).

## Limitations

- Needs a computer (or Termux with adb) to send the command; it is not a
  standalone on-phone app.
- Some manufacturers and Android versions block the SurfaceFlinger call. If
  nothing changes, that's likely why.
- The matrix is linear, so it can't target only blue hues exactly.

## Standalone app option

A real on-phone app would need native Android code (Kotlin/Java) with an
accessibility service or `WRITE_SECURE_SETTINGS`. Python alone can't provide a
system-wide color filter without a native layer.

## License

MIT
