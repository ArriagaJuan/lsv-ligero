"""Trigger serial V3 / Kistler V2 / legado y Arduino UNO V1.

Arduino V1: firmware incluido en arduino/trigger_ttl_controller.
El modo V1 requiere anchuras explicitas para generar pulsos TTL 0/5 V.


AVISO: protocolo NO verificado con hardware: ensayar desconectado antes de usar.
"""
import time
from serial_device import SerialDevice

class TriggerController:
    def __init__(self):
        self.device = SerialDevice()
        self.mode = None

    @property
    def connected(self):
        return self.device.connected

    def connect(self, port):
        self.mode = None
        self.device.open(port, 9600)
        # Arduino UNO reinicia al abrir el puerto; concedemos tiempo al bootloader.
        deadline = time.monotonic() + 4
        while time.monotonic() < deadline:
            self.device.write(b"PING\n")
            reply = self.device.port.readline().decode(errors="ignore").strip()
            if reply == "PONG":
                self.mode = "v1"
                return "Arduino UNO TTL V1 (9600 baud, D12/D10, PULSE)"
            if reply.startswith("PONG,TRIGGER_TTL_V3"):
                self.mode = "v3"
                return "TTL V3 (9600 baud, D12/D10)"
            if reply.startswith("PONG,KISTLER_TRIGGER_V2"):
                self.mode = "kistler"
                return "Kistler Trigger V2 (9600 baud, D10/D12)"
            time.sleep(0.15)
        # El firmware legado se anuncia por telemetría a 115200.
        self.device.open(port, 115200)
        deadline = time.monotonic() + 2
        while time.monotonic() < deadline:
            msg = self.device.port.read_all().decode(errors="ignore")
            if "boton_inicio" in msg:
                self.mode = "legacy"
                return "Arduino anterior (115200 baud, START_MEASURE / D5)"
            time.sleep(0.1)
        self.device.close()
        raise RuntimeError("No respondió como Arduino V1, Trigger TTL V3, Kistler V2 ni legado")

    def status(self):
        if not self.connected:
            raise RuntimeError("Trigger no conectado")
        if self.mode in ("v1", "v3", "kistler"):
            self.device.port.reset_input_buffer()
            self.device.write(b"STATUS\n")
            time.sleep(0.15)
        return self.device.port.read_all().decode(errors="replace").strip()

    def _prepare_edge_buffers(self):
        if not self.connected:
            raise RuntimeError("Trigger no conectado")
        self.device.port.reset_input_buffer()
        self.device.port.reset_output_buffer()

    def request_start(self, duration_us_12=0, duration_us_10=0):
        """Envía comando, sin garantizar recepción; confirmar con wait_start_confirmation."""
        self._prepare_edge_buffers()
        if self.mode == "v1":
            d12, d10 = int(duration_us_12), int(duration_us_10)
            if d12 < 0 or d10 < 0 or d12 > 1_000_000 or d10 > 1_000_000:
                raise ValueError("Arduino V1: duraciones permitidas de 0 a 1000000 microsegundos")
            if d12 == 0 and d10 == 0:
                raise ValueError("Arduino V1: configura un pulso para D12 o D10; ambos están en 0")
            self.device.write(f"PULSE,{d12},{d10},0,0\n".encode("ascii"))
        elif self.mode == "v3":
            cmd = f"START,{int(duration_us_12)},{int(duration_us_10)}\n"
            self.device.write(cmd.encode("ascii"))
        elif self.mode == "kistler":
            self.device.write(b"START\n")
        elif self.mode == "legacy":
            self.device.write(b"START_MEASURE\n")
        else:
            raise RuntimeError("No se reconoció el modo del trigger")

    def wait_start_confirmation(self, seconds=2):
        if self.mode not in ("v1", "kistler"):
            return None
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            line = self.device.port.readline().decode(errors="replace").strip()
            if self.mode == "v1" and line == "OK,PULSE":
                return line
            if self.mode == "kistler" and line.startswith("TRIGGER,START,"):
                return line
            if line.startswith("ERR,"):
                raise RuntimeError("Trigger respondió: " + line)
        raise TimeoutError("Trigger no confirmó START/PULSE")

    def start(self, duration_us_12=0, duration_us_10=0):
        self.request_start(duration_us_12, duration_us_10)
        return self.wait_start_confirmation()

    def request_stop(self):
        if not self.connected:
            return False
        self._prepare_edge_buffers()
        self.device.write(b"STOP\n" if self.mode in ("v3", "kistler") else b"RESET\n")
        return True

    def wait_stop_confirmation(self, seconds=2):
        if self.mode not in ("v1", "kistler"):
            return None
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            line = self.device.port.readline().decode(errors="replace").strip()
            if self.mode == "v1" and line == "OK,RESET":
                return line
            if self.mode == "kistler" and line.startswith("TRIGGER,STOP,"):
                return line
            if line.startswith("ERR,"):
                raise RuntimeError("Trigger respondió: " + line)
        raise TimeoutError("Trigger no confirmó STOP/RESET")

    def stop(self):
        sent = self.request_stop()
        if sent:
            return self.wait_stop_confirmation()
        return None

    def close(self):
        if self.connected:
            try:
                self.stop()
            except Exception:
                pass
        self.device.close()
        self.mode = None
