import streamlit as st
from reportlab.lib.pagesizes import A6
from reportlab.pdfgen import canvas
from datetime import datetime

# Estado inicial
if "empresa" not in st.session_state:
    st.session_state.empresa = "Panadería Familiar"

if "clientes" not in st.session_state:
    st.session_state.clientes = {"Paqui": "paqui@email.com"}

# --- CONFIGURACIÓN ---
with st.sidebar:
    st.header("Configuración")
    nueva_empresa = st.text_input("Nombre de la empresa", value=st.session_state.empresa)
    if st.button("Actualizar nombre"):
        st.session_state.empresa = nueva_empresa
        st.success("Nombre de empresa actualizado")

    st.subheader("Clientes frecuentes")
    nuevo_nombre = st.text_input("Nombre del cliente")
    nuevo_correo = st.text_input("Correo del cliente")
    if st.button("Guardar cliente"):
        if nuevo_nombre and nuevo_correo:
            st.session_state.clientes[nuevo_nombre] = nuevo_correo
            st.success(f"Cliente {nuevo_nombre} guardado")

# --- FUNCIONES ---
def crear_ticket_pdf(cliente, items):
    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    nombre_archivo = f"ticket_{fecha}.pdf"
    c = canvas.Canvas(nombre_archivo, pagesize=A6)

    c.setFont("Helvetica", 10)
    c.drawString(20, 260, st.session_state.empresa)
    c.drawString(20, 245, f"Cliente: {cliente}")
    c.drawString(20, 230, f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    y = 210
    total = 0
    for producto, precio in items:
        c.drawString(20, y, f"{producto} - {precio:.2f} €")
        total += precio
        y -= 15

    c.drawString(20, y-10, f"Total: {total:.2f} €")
    c.save()
    return nombre_archivo

# --- APP PRINCIPAL ---
st.title("Generador de Tickets")
cliente = st.selectbox("Selecciona cliente o escribe uno nuevo", options=[""] + list(st.session_state.clientes.keys()))

if cliente:
    email_cliente = st.session_state.clientes.get(cliente, "")
else:
    cliente = st.text_input("Nombre del cliente")
    email_cliente = ""

productos = []
n_items = st.number_input("Número de productos", min_value=1, max_value=20, step=1)

for i in range(n_items):
    col1, col2 = st.columns(2)
    with col1:
        prod = st.text_input(f"Producto {i+1}", key=f"prod{i}")
    with col2:
        precio = st.number_input(f"Precio {i+1} (€)", min_value=0.0, step=0.1, key=f"precio{i}")
    if prod:
        productos.append((prod, precio))

if st.button("Generar Ticket PDF"):
    if cliente and productos:
        nombre_archivo = crear_ticket_pdf(cliente, productos)
        with open(nombre_archivo, "rb") as f:
            st.download_button(
                label="Descargar Ticket",
                data=f,
                file_name=nombre_archivo,
                mime="application/pdf"
            )
    else:
        st.warning("Rellena el nombre del cliente y al menos un producto.")