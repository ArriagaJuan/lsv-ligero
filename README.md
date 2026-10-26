# LSV ligero

La aplicación permite adquirir lecturas de velocidad de un equipo LSV, calcular la distancia recorrida y coordinar ciclos de medición mediante un trigger. Los resultados se muestran en pantalla y se exportan a Excel. Durante la adquisición se generan respaldos incrementales en JSONL.

## Funciones

- Comunicación con el LSV por RS-232 o TCP.
- Control de trigger, incluida la integración con Arduino UNO V1.
- Configuración de duración, repeticiones, pausas e intervalo de lectura.
- Registro de tiempo, velocidad, distancia, ciclos e intentos.
- Desfase temporal manual y revisión de continuidad de las lecturas.
- Simulación sin conexiones ni salidas físicas.

## Requisitos

- Windows y Python 3.11 o 3.12.
- Conexión a Internet para instalar las dependencias la primera vez.
- Bibliotecas PySide6, pyserial y openpyxl, declaradas en requirements.txt.
- Para mediciones reales: LSV compatible, conexión RS-232 o TCP y trigger compatible.
- Para preparar el Arduino UNO: Arduino IDE y cable USB.

## Instalación

1. Descargue la carpeta completa y extráigala antes de ejecutar el programa.
2. Instale Python 3.11 o 3.12 y active la opción Add Python to PATH.
3. Ejecute ejecutar.bat.
4. Espere mientras se crea el entorno .venv y se instalan las dependencias.

El lanzador requiere Python instalado previamente. En ejecuciones posteriores, utilice ejecutar.bat.

Instalación alternativa desde PowerShell, en la carpeta del proyecto:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe sincronizador_laser_lsv.py
```

## Uso en simulación

1. Mantenga activada la opción Simulación.
2. Configure segundos por ciclo, cantidad de ciclos, pausa e intervalo de lectura.
3. Seleccione Carpeta de exportación.
4. Pulse Iniciar adquisición y revise la tabla.
5. Utilice Detener / cancelar para interrumpir el proceso si es necesario.
6. Pulse Exportar Excel para guardar los resultados.

La simulación genera datos sintéticos; no produce resultados de calibración.

## Uso con instrumentos

1. Verifique los comandos, la conexión y los niveles eléctricos de los equipos.
2. Prepare el trigger según ARDUINO_TRIGGER_LEEME.md si utiliza Arduino UNO V1.
3. Desactive Simulación.
4. Seleccione RS232 y el puerto COM del LSV, o TCP y la dirección y puerto del equipo.
5. Seleccione el puerto del trigger y utilice Conectar LSV y Conectar trigger.
6. Configure el plan y, en Arduino V1, un pulso mayor que cero en al menos uno de los canales D12 o D10.
7. Inicie la adquisición y exporte los resultados.

## Alcance y limitaciones

Esta implementación requiere validación con los instrumentos reales. El protocolo del LSV, la consulta de velocidad y la comunicación TCP deben contrastarse con el manual del equipo.

El divisor DAQ se almacena como referencia; no configura el hardware. La lectura RS-232 utiliza consultas periódicas. El desfase es manual y no equivale a una calibración automática. El control por puerto serie no garantiza sincronización submilisegundo.

No se especifica una marca o modelo exacto de LSV compatible. La compatibilidad debe confirmarse antes del uso real. Los resultados no deben utilizarse como calibración metrológica validada sin pruebas independientes.

## Archivos principales

- main.py: interfaz y adquisición.
- lsv_connection.py y serial_device.py: comunicaciones.
- trigger.py: control del trigger.
- acquisition_plan.py: ciclos e intentos.
- measurements.py y synchronization.py: procesamiento y alineación.
- exporter.py: exportación y respaldo.
- arduino/: firmware y aplicación independiente del trigger.
- tests/: pruebas automatizadas.

## Datos locales

Los ajustes de conexión y los resultados se guardan localmente. El archivo .gitignore excluye configuraciones personales, entornos, respaldos y archivos de medición habituales. Antes de publicar archivos adicionales, revise su contenido: .gitignore no elimina archivos ya versionados ni detecta información sensible.
