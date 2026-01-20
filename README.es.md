# TouchlessMouse V1.1

*[English version](README.md)*

Controla el cursor de tu ordenador mediante gestos y visión artificial, sin necesidad de tocar el mouse físico.

## Novedades en v1.1

 **Nuevas funciones**
- **Click derecho**: Anular extendido activa click derecho.
- **Detección Dinámica de Manos**: Indicador de círculo blanco en la muñeca cuando la mano está cerrada.
- **Seguimiento de Una Sola Mano**: Al abrir completamente, el sistema se bloquea a esa mano (elimina detecciones cruzadas).

**Mejoras**
- **Feedback Visual**: Indicadores de dedos mejorados (colores, tamaños y tiempos).
- **Rendimiento**: Eliminados procesos innecesarios de iluminación.
- **Estabilizador de Cursor**: Congelamiento momentáneo al salir del Modo Precisión para evitar saltos indeseados.
- **Asistencia Anatómica**: Algoritmo para inferir la posición del dedo anular cuando es ocultado por el meñique.

---

## Requisitos
- **Python 3.10** o superior
- Una **Webcam** conectada

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

### Selección de Mano
**Bloquear/Desbloquear mano**: Tus puños cerrados mostrarán un **círculo blanco** en la muñeca. Abre completamente la mano que quieras usar - esto bloqueará esa mano para seguimiento. Para desbloquear, simplemente cierra el puño nuevamente.

### Control del Cursor
1. **Mover el cursor**: Levanta el dedo índice (se ilumina en **Verde**) para arrastrar el cursor con alta sensibilidad.

2. **Click y Modo precisión**: Mientras levantas el índice, levanta el dedo meñique (se ilumina en **Rojo**). Para hacer **click**, retrae y extiende el meñique rápidamente (gesto de doble toque).

3. **Mantener click para arrastrar**: Mientras arrastras el cursor, levanta el dedo corazón (se ilumina en **Naranja**). Mantenlo extendido hasta que cambie a **Azul**; ahora el click está sostenido.

### Click Derecho (Dos Métodos)
- **Método 1**: Levanta solo el anular (se ilumina en **Naranja**), mantén brevemente hasta que se ponga **Azul** para click derecho.

- **Método 2 (Ergonómico)**: Levanta el anular y el corazón al mismo tiempo. Se iluminarán en **naranja**, espera hasta que se ponga azul y dará click derecho.

### Parada de Emergencia
**"¡Detente!"**: Abre la mano completamente - todos los dedos se iluminan en **Rojo** y el sistema se pausa.

**Consideración**: Las condiciones de iluminación pueden afectar el reconocimiento de gestos. Ajusta los parámetros en **config.py** para un rendimiento óptimo.

---

## Configuraciones (`config.py`)

Personaliza el comportamiento del sistema modificando estos parámetros clave:

### Configuración de Cámara
- `FRAME_WIDTH` / `FRAME_HEIGHT`: Resolución (predeterminado 640x480 para mejor precisión)
- `FPS_TARGET`: Velocidad de captura

### Detección
- `MIN_DETECTION_CONFIDENCE`: Umbral de detección
- `MODEL_COMPLEXITY`: 0 (Rápido) o 1 (Preciso, predeterminado)

### Movimiento
- `SENSITIVITY`: Velocidad del cursor
- `SMOOTHING_FACTOR`: Reduce temblor/vibración de mano

### Gestos
- `PINKY_TRIGGER_RATIO`: Sensibilidad de click
- `DRAG_ACTIVATION_TIME`: Tiempo de espera antes de activar arrastre

### Depuración
- `SHOW_DEBUG_WINDOW`: Activa/Desactiva ventana de retroalimentación visual

**Nota**: Los módulos individuales pueden personalizarse aún más para necesidades específicas.

---

## Registro de Cambios

### v1.1 (20 de Enero, 2026)
- Detección dinámica de dos manos con indicadores visuales en muñeca.
- Sistema de seguimiento de una sola mano activa (previene interferencias).
- Click derecho: anular extendido.
- Click derecho alternativo: corazón + anular (modo ergonómico de 4 dedos).
- Retroalimentación visual mejorada para estados de mano.
- Optimizaciones de rendimiento.

### v1.0 (Lanzamiento Inicial)
- Control básico de cursor mediante dedo índice.
- Funcionalidad de click con meñique.
- Arrastrar y mantener con dedo corazón.
- Gesto de parada de emergencia.
- Sensibilidad y suavizado configurables.

---

## Licencia

Licencia MIT - Vea **LICENSE** para más detalles.

## Contribuciones

¡Siéntete libre de abrir issues o enviar pull requests para mejoras!
