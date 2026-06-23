import json
import os
from datetime import datetime, timedelta
import threading

ALERTS_FILE = "alerts.json"

class AlertService:
    def __init__(self, umbral_stock:int=5, tiempo_max_mesas_hours:int=24, check_interval_seconds:int=60):
        self.umbral_stock = umbral_stock
        self.tiempo_max_mesas = timedelta(hours=tiempo_max_mesas_hours)
        self.check_interval = check_interval_seconds
        self._alerts = []
        self._load()
        self._lock = threading.Lock()
        self._running = False

    def _load(self):
        if not os.path.exists(ALERTS_FILE):
            self._alerts = []
            return
        try:
            with open(ALERTS_FILE, 'r', encoding='utf-8') as f:
                self._alerts = json.load(f)
        except Exception:
            self._alerts = []

    def _save(self):
        try:
            with open(ALERTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(self._alerts, f, ensure_ascii=False, indent=4)
        except Exception:
            pass

    def _next_id(self):
        return max((a.get('id',0) for a in self._alerts), default=0) + 1

    def _find_active(self, tipo, referencia):
        for a in self._alerts:
            if a.get('tipo')==tipo and a.get('referencia')==referencia and a.get('estado')=='activo':
                return a
        return None

    def create_alert(self, tipo:str, mensaje:str, referencia:str):
        with self._lock:
            if self._find_active(tipo, referencia):
                return None
            a = {
                'id': self._next_id(),
                'tipo': tipo,
                'mensaje': mensaje,
                'referencia': referencia,
                'created_at': datetime.now().isoformat(),
                'estado': 'activo'
            }
            self._alerts.append(a)
            self._save()
            return a

    def resolve_alerts_for(self, tipo, referencia):
        changed = False
        with self._lock:
            for a in self._alerts:
                if a.get('tipo')==tipo and a.get('referencia')==referencia and a.get('estado')=='activo':
                    a['estado']='resuelto'
                    a['resolved_at']=datetime.now().isoformat()
                    changed = True
            if changed:
                self._save()
        return changed

    def check_stock_for_ingredient(self, ing):
        # ing expected to have nombre, stock_unidades, min_stock
        nombre = getattr(ing, 'nombre', None)
        stock = int(getattr(ing, 'stock_unidades', 0))
        min_stock = int(getattr(ing, 'min_stock', self.umbral_stock))

        if stock <= 0:
            # sin stock
            if not self._find_active('sin_stock', nombre):
                msg = f"Sin stock: {nombre}. No está disponible."
                self.create_alert('sin_stock', msg, nombre)
            # mark any low-stock alerts resolved
            self.resolve_alerts_for('stock_bajo', nombre)
            return

        if stock <= min_stock:
            # stock bajo
            if not self._find_active('stock_bajo', nombre):
                msg = f"Stock bajo: {nombre}. Quedan {stock} u."
                self.create_alert('stock_bajo', msg, nombre)
            return

        # stock por encima del umbral -> resolver alertas
        self.resolve_alerts_for('stock_bajo', nombre)
        self.resolve_alerts_for('sin_stock', nombre)

    def _parse_fecha(self, valor):
        if not valor:
            return None
        if isinstance(valor, datetime):
            return valor
        try:
            return datetime.fromisoformat(valor)
        except Exception:
            pass
        try:
            return datetime.strptime(valor, "%d/%m/%Y")
        except Exception:
            return None

    def _obtener_fecha_mesa(self, mesa, pedidos):
        # Usa la marca de ocupación de mesa si existe, y si hay pedido abierto
        # usa la fecha de creación del pedido para calcular el inicio real.
        candidato = None

        desde = getattr(mesa, 'ocupada_desde', None)
        fecha_mesa = self._parse_fecha(desde)
        if fecha_mesa:
            candidato = fecha_mesa

        if not getattr(mesa, 'ocupada', False):
            return candidato

        for pedido in pedidos:
            if getattr(pedido, 'estado', '').lower() != 'abierto':
                continue
            if getattr(pedido, 'mesa1', None) and getattr(pedido.mesa1, 'numero', None) == mesa.numero:
                fecha_pedido = self._parse_fecha(getattr(pedido, 'created_at', None))
                if fecha_pedido and (candidato is None or fecha_pedido < candidato):
                    candidato = fecha_pedido
            if getattr(pedido, 'mesa2', None) and getattr(pedido.mesa2, 'numero', None) == mesa.numero:
                fecha_pedido = self._parse_fecha(getattr(pedido, 'created_at', None))
                if fecha_pedido and (candidato is None or fecha_pedido < candidato):
                    candidato = fecha_pedido

        return candidato

    def check_mesas(self, mesas):
        # mesas: list of Mesa objects with numero, ocupada, ocupada_desde
        try:
            import repositorio
            pedidos = repositorio.cargarPedidos()
        except Exception:
            pedidos = []

        for m in mesas:
            num = getattr(m, 'numero', None)
            ocupada = getattr(m, 'ocupada', False)
            if ocupada:
                fecha_inicio = self._obtener_fecha_mesa(m, pedidos)
                if not fecha_inicio:
                    continue
                try:
                    if datetime.now() - fecha_inicio > self.tiempo_max_mesas:
                        if not self._find_active('mesa_ocupada', str(num)):
                            delta = datetime.now() - fecha_inicio
                            dias = delta.days
                            horas = delta.seconds // 3600
                            minutos = (delta.seconds % 3600) // 60
                            tiempo_str = f"{dias}d {horas}h {minutos}m"
                            msg = f"Atención: La mesa {num} lleva {tiempo_str} ocupada. Verificar si debe cerrarse."
                            self.create_alert('mesa_ocupada', msg, str(num))
                except Exception:
                    continue
            else:
                self.resolve_alerts_for('mesa_ocupada', str(num))

    def list_alerts(self):
        # retorna copia para evitar manipulación externa
        with self._lock:
            return list(self._alerts)

    def delete_alert(self, alert_id: int):
        """Eliminar una alerta por id (borrado físico)."""
        removed = False
        with self._lock:
            new_alerts = [a for a in self._alerts if a.get('id') != alert_id]
            if len(new_alerts) != len(self._alerts):
                self._alerts = new_alerts
                try:
                    self._save()
                except Exception:
                    pass
                removed = True
        return removed

    def start_periodic_check(self):
        if self._running:
            return
        self._running = True
        def loop():
            import repositorio
            while self._running:
                try:
                    mesas = repositorio.cargarMesas()
                    self.check_mesas(mesas)
                except Exception:
                    pass
                finally:
                    threading.Event().wait(self.check_interval)
        t = threading.Thread(target=loop, daemon=True, name="AlertChecker")
        t.start()

    def stop(self):
        self._running = False
