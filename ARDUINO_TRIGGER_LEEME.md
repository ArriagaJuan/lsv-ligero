# Trigger Arduino UNO V1

El firmware permite controlar dos salidas de trigger, D12 y D10, y un buzzer en D13. La comunicación utiliza 9600 baudios.

## Instalación

1. Abra arduino/trigger_ttl_controller/trigger_ttl_controller.ino en Arduino IDE.
2. Seleccione Arduino Uno y el puerto COM correspondiente.
3. Cargue el firmware.
4. Cierre el Monitor Serie antes de conectar la aplicación.

El dispositivo anuncia READY,TRIGGER_TTL_V1 al iniciar. El comando PING devuelve PONG.

## Prueba independiente

Ejecute ejecutar.bat para preparar las dependencias y después abrir_trigger_arduino.bat para abrir la interfaz del trigger. Esta interfaz permite seleccionar el puerto, configurar pulsos y controlar las salidas. Compruebe las señales con el trigger desconectado del instrumento.

## Uso desde la aplicación principal

Seleccione el puerto del Arduino y pulse Conectar trigger. Configure la duración del pulso D12 o D10 en microsegundos. Un valor de cero deshabilita el canal; al menos uno debe tener un valor mayor que cero para iniciar una adquisición real.

Al comenzar cada ciclo se envía PULSE y se comprueba OK,PULSE. Al finalizar se envía RESET y se comprueba OK,RESET. Los pulsos son breves; no permanecen activos durante toda la medición.

## Compatibilidad y límites

Las salidas del UNO son aproximadamente 0/5 V, con LOW inactivo y HIGH durante el pulso. Verifique tensión, polaridad, masa común y aislamiento antes de conectar un instrumento. No conecte directamente una entrada de 24 V.

Arduino V1 no es intercambiable con TRIGGER_TTL_V3 ni KISTLER_TRIGGER_V2: sus comandos y transiciones pueden ser distintos. La sincronización y la duración real de los pulsos requieren comprobación instrumental.
