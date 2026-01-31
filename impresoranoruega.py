import sqlite3
from datetime import datetime
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, RoundedRectangle

# --- MOTOR DE IMPRESIÓN ANDROID ---
try:
    from jnius import autoclass
    ANDROID_AVAILABLE = True
except:
    ANDROID_AVAILABLE = False

def imprimir_ticket_bluetooth(folio, cliente, monto, fecha, info):
    if not ANDROID_AVAILABLE:
        print("Impresión solo disponible en Android")
        return False
    
    try:
        BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
        UUID = autoclass('java.util.UUID')
        uuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
        adapter = BluetoothAdapter.getDefaultAdapter()
        
        paired_devices = adapter.getBondedDevices().toArray()
        for device in paired_devices:
            # Busca nombres comunes de impresoras térmicas
            name = device.getName()
            if any(x in name for x in ["Printer", "MTP", "58mm", "80mm"]):
                socket = device.createRfcommSocketToServiceRecord(uuid)
                socket.connect()
                out = socket.getOutputStream()
                
                # Formato ESC/POS para la térmica
                msg = f"--- FJORD RECEIPTS ---\\n"
                msg += f"Folio: #{folio}\\n"
                msg += f"Fecha: {fecha}\\n"
                msg += f"----------------------\\n"
                msg += f"CLIENTE: {cliente}\\n"
                msg += f"MONTO: ${monto}\\n"
                msg += f"CONCEPTO: {info}\\n"
                msg += f"----------------------\\n"
                msg += f"Gracias por su pago\\n\\n\\n\\n"
                
                out.write(msg.encode('gbk'))
                out.flush()
                socket.close()
                return True
        return False
    except:
        return False

# --- TEMAS ---
TEMAS = {
    'oscuro': {'fondo': (0.05, 0.05, 0.08, 1), 'card': (0.1, 0.12, 0.18, 1), 'texto_p': (0.1, 0.5, 1, 1), 'texto_s': (1, 1, 1, 1), 'input': (0.15, 0.15, 0.22, 1)},
    'claro': {'fondo': (0.95, 0.95, 0.98, 1), 'card': (1, 1, 1, 1), 'texto_p': (0.05, 0.3, 0.7, 1), 'texto_s': (0.1, 0.1, 0.1, 1), 'input': (0.88, 0.88, 0.92, 1)}
}

class VentasScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        
        header = BoxLayout(size_hint_y=None, height=80, spacing=10)
        self.lbl_titulo = Label(text="FJORD RECEIPTS", font_size='26sp', bold=True)
        self.btn_tema = Button(text="MODO", size_hint_x=None, width=120, bold=True)
        self.btn_tema.bind(on_press=self.cambiar_estilo)
        header.add_widget(self.lbl_titulo); header.add_widget(self.btn_tema); self.layout.add_widget(header)
        
        self.cli = TextInput(hint_text="Cliente", multiline=False, size_hint_y=None, height=90, font_size='18sp', padding=[15, 20])
        self.mon = TextInput(hint_text="Monto $", multiline=False, input_filter='float', size_hint_y=None, height=90, font_size='18sp', padding=[15, 20])
        self.inf = TextInput(hint_text="Concepto", multiline=False, size_hint_y=None, height=90, font_size='18sp', padding=[15, 20])
        self.layout.add_widget(self.cli); self.layout.add_widget(self.mon); self.layout.add_widget(self.inf)
        
        self.btn_gen = Button(text="GENERAR E IMPRIMIR", bold=True, size_hint_y=None, height=120)
        self.btn_gen.bind(on_press=self.guardar_e_imprimir); self.layout.add_widget(self.btn_gen)
        
        self.hist_resumen = Label(text="Listo para registrar", size_hint_y=None, height=100)
        self.layout.add_widget(self.hist_resumen)
        
        nav = BoxLayout(size_hint_y=None, height=100, spacing=10)
        btn_corte = Button(text="CORTE", background_color=(0.8, 0.2, 0.2, 1), bold=True); btn_corte.bind(on_press=self.cortar)
        btn_hist = Button(text="HISTORIAL >", bold=True); btn_hist.bind(on_press=lambda x: setattr(self.manager, 'current', 'historial'))
        nav.add_widget(btn_corte); nav.add_widget(btn_hist); self.layout.add_widget(nav)
        
        self.add_widget(self.layout); self.aplicar_colores('oscuro')

    def cambiar_estilo(self, instance):
        app = App.get_running_app()
        app.tema = 'claro' if app.tema == 'oscuro' else 'oscuro'
        for s in self.manager.screens: 
            if hasattr(s, 'aplicar_colores'): s.aplicar_colores(app.tema)

    def aplicar_colores(self, modo):
        c = TEMAS[modo]; Window.clearcolor = c['fondo']
        self.lbl_titulo.color = c['texto_p']; self.btn_gen.background_color = c['texto_p']
        self.btn_tema.background_color = c['card']; self.btn_tema.color = c['texto_s']
        for w in [self.cli, self.mon, self.inf]:
            w.background_color = c['input']; w.foreground_color = c['texto_s']
        self.hist_resumen.color = (0.5, 0.5, 0.5, 1)

    def guardar_e_imprimir(self, instance):
        if self.cli.text and self.mon.text:
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            conn = sqlite3.connect('fjord_mobile.db'); curr = conn.cursor()
            curr.execute("INSERT INTO recibos (cliente, monto, info, fecha) VALUES (?,?,?,?)", (self.cli.text, self.mon.text, self.inf.text, fecha))
            folio = curr.lastrowid; conn.commit(); conn.close()
            
            # Intenta imprimir directamente
            imprimir_ticket_bluetooth(folio, self.cli.text, self.mon.text, fecha, self.inf.text)
            
            self.cli.text = ""; self.mon.text = ""; self.inf.text = ""
            self.hist_resumen.text = f"¡Recibo #{folio} enviado a impresora!"

    def cortar(self, instance):
        conn = sqlite3.connect('fjord_mobile.db'); curr = conn.cursor()
        curr.execute("SELECT SUM(monto) FROM recibos WHERE estado='ABIERTO'")
        total = curr.fetchone()[0] or 0.0
        Popup(title='Corte', content=Label(text=f"Total: ${total:,.2f}"), size_hint=(0.7, 0.3)).open()
        curr.execute("UPDATE recibos SET estado='CERRADO' WHERE estado='ABIERTO'"); conn.commit(); conn.close()

class HistorialScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        self.lbl_t = Label(text="HISTORIAL", font_size='22sp', bold=True, size_hint_y=None, height=60); self.layout.add_widget(self.lbl_t)
        self.search = TextInput(hint_text="Buscar cliente...", multiline=False, size_hint_y=None, height=90, font_size='18sp'); self.search.bind(text=self.buscar); self.layout.add_widget(self.search)
        self.scroll = ScrollView(); self.grid = GridLayout(cols=1, spacing=15, size_hint_y=None); self.grid.bind(minimum_height=self.grid.setter('height')); self.scroll.add_widget(self.grid); self.layout.add_widget(self.scroll)
        self.btn_v = Button(text="< VOLVER", size_hint_y=None, height=100, bold=True); self.btn_v.bind(on_press=lambda x: setattr(self.manager, 'current', 'ventas')); self.layout.add_widget(self.btn_v); self.add_widget(self.layout)

    def aplicar_colores(self, modo):
        self.modo_actual = modo; c = TEMAS[modo]; self.lbl_t.color = c['texto_p']
        self.search.background_color = c['input']; self.search.foreground_color = c['texto_s']
        self.btn_v.background_color = c['card']; self.btn_v.color = c['texto_s']; self.buscar(None, self.search.text)

    def buscar(self, instance, value):
        self.grid.clear_widgets(); c = TEMAS[self.modo_actual]
        conn = sqlite3.connect('fjord_mobile.db'); curr = conn.cursor()
        curr.execute("SELECT folio, cliente, monto, fecha, info FROM recibos WHERE cliente LIKE ? ORDER BY folio DESC", (f'%{value}%',))
        filas = curr.fetchall(); conn.close()
        for f in filas:
            card = BoxLayout(orientation='vertical', size_hint_y=None, height=220, padding=15)
            with card.canvas.before:
                Color(*c['card']); self.rect = RoundedRectangle(pos=card.pos, size=card.size, radius=[15,])
                card.bind(pos=self.update_rect, size=self.update_rect)
            card.add_widget(Label(text=f"Folio: #{f[0]} | {f[1]}", bold=True, color=c['texto_p']))
            card.add_widget(Label(text=f"${f[2]:,.2f} - {f[3]}", color=c['texto_s']))
            btn_rep = Button(text="REIMPRIMIR", size_hint_y=None, height=60, background_color=c['texto_p'])
            btn_rep.bind(on_press=lambda x, d=f: imprimir_ticket_bluetooth(d[0], d[1], d[2], d[3], d[4]))
            card.add_widget(btn_rep); self.grid.add_widget(card)

    def update_rect(self, instance, value):
        instance.canvas.before.children[-1].pos = instance.pos
        instance.canvas.before.children[-1].size = instance.size

class FjordApp(App):
    tema = 'oscuro'
    def build(self):
        with sqlite3.connect('fjord_mobile.db') as conn:
            conn.cursor().execute('''CREATE TABLE IF NOT EXISTS recibos (folio INTEGER PRIMARY KEY AUTOINCREMENT, cliente TEXT, monto REAL, info TEXT, fecha TEXT, estado TEXT DEFAULT 'ABIERTO')''')
        sm = ScreenManager()
        sm.add_widget(VentasScreen(name='ventas')); sm.add_widget(HistorialScreen(name='historial'))
        return sm

if __name__ == "__main__":
    FjordApp().run()
