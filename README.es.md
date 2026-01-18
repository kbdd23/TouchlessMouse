# TouchlessMouse V1.0

*[English version](README.md)*

Controla el cursor de tu ordenador mediante gestos y visión artificial, sin necesidad de tocar el mouse físico.

## Requisitos
- **Python 3.10** o superior.
- Una **Webcam** conectada.

---

## Linux (Instalación y Ejecución)

1. **Abrir terminal** en la carpeta del proyecto.
2. **Crear entorno virtual** (opcional pero recomendado):
   ```bash
   python3 -m venv venv
   ```
3. **Activar entorno**:
   ```bash
   source venv/bin/activate
   ```
4. **Instalar dependencias**:
   ```bash
   pip install opencv-python mediapipe pyautogui sounddevice numpy
   ```
5. **Ejecutar**:
   ```bash
   python main.py
   ```

---

## Windows (Instalación y Ejecución)

1. **Abrir CMD o PowerShell** en la carpeta del proyecto.
2. **Crear entorno virtual** (opcional pero recomendado):
   ```bash
   python -m venv venv
   ```
3. **Activar entorno**:
   ```bash
   venv\Scripts\activate
   ```
4. **Instalar dependencias**:
   ```bash
   pip install opencv-python mediapipe pyautogui sounddevice numpy
   ```
5. **Ejecutar**:
   ```bash
   python main.py
   ```
   
---

## Comandos 

1. **Mover el cursor**: Levanta el dedo índice, se iluminará en verde y podrás arrastrar. (Sensibilidad alta)

2. **Click y Modo precisión**: Mientras levantas el índice, levanta el dedo meñique y se iluminará en rojo, baja y levanta rápidamente el meñique y darás click. (Sensibilidad baja)

3. **Mantener click para arrastrar**: Mientras arrastras el cursor, levanta el dedo corazón y se iluminará en naranja, mantenlo extendido durante un momento y se iluminará en azul, ahora el click se mantiene, permitiendo el scroll.

4. **"Detente!"**: Abre la mano por completo y el sistema se detendrá por completo. (Se iluminarán todos los dedos)

**Consideración**: La iluminación puede influir en la interpretación de combinaciones múltiples, se recomienda configurar atributos específicos de **config.py**.

---

## Configuraciones

- Resolución de la cámara y limitación de FPS
- Sensibilidad de detección de manos
- Umbrales de activación por gestos
- Sensibilidad del cursor
- Configuración de la ventana de depuración

**Nota**: Los módulos del programa pueden ser mejorados y podrían necesitar sus propias configuraciones.

---

## Licencia

Licencia MIT - Vea **LICENSE** para más detalles.

## Contribuciones

Siéntase libre de comentar o hacer pull requests para mejoras!
