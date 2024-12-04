import pymysql
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# Configuración de la conexión a la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345678',
    'database': 'marketug_db'
}

# Función para ejecutar consultas
def execute_query(query, params=()):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query, params)
        connection.commit()
        connection.close()
    except Exception as e:
        messagebox.showerror("Error", f"Error al ejecutar consulta: {e}")

# Función para obtener datos
def fetch_data(query, params=()):
    try:
        connection = pymysql.connect(**db_config)
        cursor = connection.cursor()
        cursor.execute(query, params)
        rows = cursor.fetchall()
        connection.close()
        return rows
    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener datos: {e}")
        return []

def go_back(user_id):
    """Regresa al menú principal."""
    main_menu(user_id)

def logout():
    """Cerrar sesión y regresar al inicio."""
    login_screen()


# Pantalla de inicio de sesión
def login_screen():
    """Pantalla inicial con opciones de ingreso y registro."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Bienvenido al Sistema de Administración", font=("Arial", 16)).pack(pady=20)

    def show_register_form():
        manage_users()

    def login_user():
        email = email_entry.get().strip()
        password = password_entry.get().strip()

        if not (email and password):
            messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos.")
            return

        user = fetch_data("SELECT id_usuario, nombre FROM usuarios WHERE correo = %s AND contrasena = %s", (email, password))
        if user:
            user_id = user[0][0]  # Recuperar el id_usuario
            messagebox.showinfo("Éxito", f"Bienvenido, {user[0][1]}!")
            main_menu(user_id)  # Pasar el user_id al menú principal
        else:
            messagebox.showerror("Error", "Correo o contraseña incorrectos.")


    # Formulario de inicio de sesión
    tk.Label(content_frame, text="Correo:").pack(pady=5)
    email_entry = tk.Entry(content_frame)
    email_entry.pack(pady=5)

    tk.Label(content_frame, text="Contraseña:").pack(pady=5)
    password_entry = tk.Entry(content_frame, show="*")
    password_entry.pack(pady=5)

    tk.Button(content_frame, text="Ingresar", command=login_user).pack(pady=10)
    tk.Label(content_frame, text="¿No tienes cuenta?").pack(pady=10)
    tk.Button(content_frame, text="Regístrate aquí", command=show_register_form).pack(pady=5)



# Pantalla de registro de usuarios
def manage_users():
    """Pantalla para registrar un nuevo usuario."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Registrar Nuevo Usuario", font=("Arial", 16)).pack(pady=20)

    tk.Label(content_frame, text="Nombre:").pack(pady=5)
    name_entry = tk.Entry(content_frame)
    name_entry.pack(pady=5)

    tk.Label(content_frame, text="Correo:").pack(pady=5)
    email_entry = tk.Entry(content_frame)
    email_entry.pack(pady=5)

    tk.Label(content_frame, text="Carrera:").pack(pady=5)
    career_entry = tk.Entry(content_frame)
    career_entry.pack(pady=5)

    tk.Label(content_frame, text="Contraseña:").pack(pady=5)
    password_entry = tk.Entry(content_frame, show="*")
    password_entry.pack(pady=5)

    def add_user():
        name = name_entry.get().strip()
        email = email_entry.get().strip()
        career = career_entry.get().strip()
        password = password_entry.get().strip()

        if not (name and email and password):
            messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos obligatorios.")
            return

        execute_query(
            "INSERT INTO usuarios (nombre, correo, carrera, contrasena) VALUES (%s, %s, %s, %s)",
            (name, email, career, password),
        )
        messagebox.showinfo("Éxito", "Usuario registrado correctamente.")
        login_screen()

    tk.Button(content_frame, text="Registrar Usuario", command=add_user).pack(pady=10)
    tk.Button(content_frame, text="Regresar", command=login_screen).pack(pady=5)

# Pantalla principal
def main_menu():
    """Pantalla principal después del inicio de sesión."""
    for widget in content_frame.winfo_children():
        widget.destroy()
    tk.Label(content_frame, text="Bienvenido al Sistema de Administración", font=("Arial", 16)).pack(pady=20)

# Crear la ventana principal
root = tk.Tk()
root.title("Sistema de Administración de Datos")
root.geometry("800x600")

# Marco de contenido
content_frame = tk.Frame(root)
content_frame.pack(fill="both", expand=True)

# Función para agregar productos
def add_product_screen(user_id):
    """Pantalla para agregar un nuevo producto"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Agregar Nuevo Producto", font=("Arial", 16)).pack(pady=20)

    tk.Label(content_frame, text="Nombre del Producto:").pack(pady=5)
    product_name_entry = tk.Entry(content_frame)
    product_name_entry.pack(pady=5)

    tk.Label(content_frame, text="Descripción:").pack(pady=5)
    product_desc_entry = tk.Entry(content_frame)
    product_desc_entry.pack(pady=5)

    tk.Label(content_frame, text="Precio:").pack(pady=5)
    product_price_entry = tk.Entry(content_frame)
    product_price_entry.pack(pady=5)

    tk.Label(content_frame, text="Categoría:").pack(pady=5)

    categories = fetch_data("SELECT id_categoria, nombre_categoria FROM categorias")
    category_options = {cat[1]: cat[0] for cat in categories}
    selected_category = tk.StringVar(content_frame)
    category_menu = tk.OptionMenu(content_frame, selected_category, *category_options.keys())
    category_menu.pack(pady=5)

    def add_product():
        name = product_name_entry.get().strip()
        desc = product_desc_entry.get().strip()
        price = product_price_entry.get().strip()
        category_name = selected_category.get()

        if not (name and price and category_name):
            messagebox.showwarning("Campos Vacíos", "Por favor, completa todos los campos obligatorios.")
            return

        category_id = category_options.get(category_name)

        try:
            execute_query(
                "INSERT INTO productos (nombre, descripcion, precio, id_usuario, id_categoria) VALUES (%s, %s, %s, %s, %s)",
                (name, desc, float(price), user_id, category_id),
            )
            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
            main_menu(user_id)
        except Exception as e:
            messagebox.showerror("Error", f"Error al agregar el producto: {e}")

    tk.Button(content_frame, text="Agregar Producto", command=add_product).pack(pady=10)
    tk.Button(content_frame, text="Regresar", command=lambda: go_back(user_id)).pack(pady=5)


# Función para comprar productos
def buy_product_screen(user_id):
    """Pantalla para comprar productos disponibles y ver productos comprados."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Comprar Productos", font=("Arial", 16)).pack(pady=20)

    # Obtener los productos disponibles
    products = fetch_data("SELECT id_producto, nombre, descripcion, precio FROM productos WHERE estado = 'disponible'")
    if not products:
        tk.Label(content_frame, text="No hay productos disponibles.").pack(pady=10)
    else:
        tk.Label(content_frame, text="Productos Disponibles:").pack(pady=10)
        tree = ttk.Treeview(content_frame, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Descripción", text="Descripción")
        tree.heading("Precio", text="Precio")

        for product in products:
            tree.insert("", "end", values=product)

        tree.pack(fill="both", expand=True, pady=10)

        def buy_product():
            selected_item = tree.focus()
            if not selected_item:
                messagebox.showwarning("Selección Vacía", "Por favor, selecciona un producto.")
                return

            product_id = tree.item(selected_item)["values"][0]

            try:
                # Registrar la compra
                execute_query(
                    "INSERT INTO compras (id_producto, id_comprador) VALUES (%s, %s)",
                    (product_id, user_id),
                )

                # Actualizar el estado del producto a 'vendido'
                execute_query(
                    "UPDATE productos SET estado = 'vendido' WHERE id_producto = %s",
                    (product_id,)
                )

                messagebox.showinfo("Éxito", "Producto comprado exitosamente.")
                buy_product_screen(user_id)  # Recargar la pantalla
            except Exception as e:
                messagebox.showerror("Error", f"Error al registrar la compra: {e}")

        tk.Button(content_frame, text="Comprar Producto", command=buy_product).pack(pady=10)

    # Mostrar productos comprados
    tk.Label(content_frame, text="Productos Comprados:").pack(pady=20)
    purchased_products = fetch_data("""
        SELECT p.id_producto, p.nombre, p.descripcion, p.precio
        FROM compras c
        JOIN productos p ON c.id_producto = p.id_producto
        WHERE c.id_comprador = %s
    """, (user_id,))
    if purchased_products:
        purchased_tree = ttk.Treeview(content_frame, columns=("ID", "Nombre", "Descripción", "Precio"), show="headings")
        purchased_tree.heading("ID", text="ID")
        purchased_tree.heading("Nombre", text="Nombre")
        purchased_tree.heading("Descripción", text="Descripción")
        purchased_tree.heading("Precio", text="Precio")

        for product in purchased_products:
            purchased_tree.insert("", "end", values=product)

        purchased_tree.pack(fill="both", expand=True, pady=10)
    else:
        tk.Label(content_frame, text="No has comprado ningún producto aún.").pack(pady=10)

    tk.Button(content_frame, text="Regresar", command=lambda: main_menu(user_id)).pack(pady=10)



# Función para enviar mensajes
def message_screen(user_id):
    """Pantalla para enviar y recibir mensajes"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Encabezado de la pantalla
    tk.Label(content_frame, text="Mensajería", font=("Arial", 16)).pack(pady=10)

    # Sección: Enviar mensajes
    tk.Label(content_frame, text="Usuarios con productos disponibles:").pack(pady=10)
    users = fetch_data("""
        SELECT DISTINCT u.id_usuario, u.nombre, p.nombre AS producto
        FROM usuarios u
        JOIN productos p ON u.id_usuario = p.id_usuario
        WHERE u.id_usuario != %s AND p.estado = 'disponible'
    """, (user_id,))
    
    if not users:
        tk.Label(content_frame, text="No hay usuarios disponibles para enviar mensajes.").pack(pady=10)
    else:
        user_list = ttk.Treeview(content_frame, columns=("ID", "Nombre", "Producto"), show="headings")
        user_list.heading("ID", text="ID")
        user_list.heading("Nombre", text="Nombre")
        user_list.heading("Producto", text="Producto")
        user_list.column("ID", width=50, anchor="center")
        user_list.column("Nombre", width=200, anchor="center")
        user_list.column("Producto", width=200, anchor="center")

        for user in users:
            user_list.insert("", "end", values=user)
        user_list.pack(fill="both", expand=True, pady=10)

    tk.Label(content_frame, text="Escribe tu mensaje:").pack(pady=5)
    message_entry = tk.Entry(content_frame, width=50)
    message_entry.pack(pady=5)

    def send_message():
        selected_item = user_list.focus()
        if not selected_item:
            messagebox.showwarning("Selección Vacía", "Por favor, selecciona un usuario.")
            return

        recipient_id = user_list.item(selected_item)["values"][0]
        message = message_entry.get().strip()

        if not message:
            messagebox.showwarning("Mensaje Vacío", "Por favor, escribe un mensaje.")
            return

        execute_query(
            "INSERT INTO mensajes (id_emisor, id_receptor, mensaje) VALUES (%s, %s, %s)",
            (user_id, recipient_id, message),
        )
        messagebox.showinfo("Éxito", "Mensaje enviado correctamente.")
        message_entry.delete(0, tk.END)

    tk.Button(content_frame, text="Enviar Mensaje", command=send_message, width=20).pack(pady=10)

    # Sección: Mensajes recibidos
    tk.Label(content_frame, text="Mensajes Recibidos:").pack(pady=20)
    received_messages = fetch_data("""
        SELECT m.id_mensaje, u.nombre AS emisor, m.mensaje, m.fecha_envio, m.id_emisor
        FROM mensajes m
        JOIN usuarios u ON m.id_emisor = u.id_usuario
        WHERE m.id_receptor = %s
        ORDER BY m.fecha_envio DESC
    """, (user_id,))
    
    if not received_messages:
        tk.Label(content_frame, text="No tienes mensajes recibidos.").pack(pady=10)
    else:
        message_list = ttk.Treeview(content_frame, columns=("ID", "Emisor", "Mensaje", "Fecha"), show="headings")
        message_list.heading("ID", text="ID")
        message_list.heading("Emisor", text="Emisor")
        message_list.heading("Mensaje", text="Mensaje")
        message_list.heading("Fecha", text="Fecha")
        message_list.column("ID", width=50, anchor="center")
        message_list.column("Emisor", width=150, anchor="center")
        message_list.column("Mensaje", width=300, anchor="center")
        message_list.column("Fecha", width=150, anchor="center")

        for idx, msg in enumerate(received_messages):
            message_list.insert("", "end", iid=idx, values=msg[:-1])  # Excluir id_emisor al mostrar
        message_list.pack(fill="both", expand=True, pady=10)

        def reply_message():
            selected_item = message_list.focus()
            if not selected_item:
                messagebox.showwarning("Selección Vacía", "Por favor, selecciona un mensaje para responder.")
                return

            selected_index = int(selected_item)
            emisor_id = received_messages[selected_index][-1]  # Recuperar id_emisor
            reply_content = message_entry.get().strip()

            if not reply_content:
                messagebox.showwarning("Mensaje Vacío", "Por favor, escribe un mensaje.")
                return

            execute_query(
                "INSERT INTO mensajes (id_emisor, id_receptor, mensaje) VALUES (%s, %s, %s)",
                (user_id, emisor_id, reply_content),
            )
            messagebox.showinfo("Éxito", "Respuesta enviada correctamente.")
            message_entry.delete(0, tk.END)

        tk.Button(content_frame, text="Responder Mensaje", command=reply_message, width=20).pack(pady=10)

    # Colocar botón "Regresar" siempre visible al final
    tk.Button(content_frame, text="Regresar", command=lambda: main_menu(user_id), width=20).pack(side=tk.BOTTOM, pady=10)

    """Pantalla para enviar y recibir mensajes"""
    for widget in content_frame.winfo_children():
        widget.destroy()

    # Encabezado de la pantalla
    tk.Label(content_frame, text="Mensajería", font=("Arial", 16)).pack(pady=10)

    # Sección: Enviar mensajes
    tk.Label(content_frame, text="Usuarios con productos disponibles:").pack(pady=10)
    users = fetch_data("""
        SELECT DISTINCT u.id_usuario, u.nombre, p.nombre AS producto
        FROM usuarios u
        JOIN productos p ON u.id_usuario = p.id_usuario
        WHERE u.id_usuario != %s AND p.estado = 'disponible'
    """, (user_id,))
    
    if not users:
        tk.Label(content_frame, text="No hay usuarios disponibles para enviar mensajes.").pack(pady=10)
    else:
        user_list = ttk.Treeview(content_frame, columns=("ID", "Nombre", "Producto"), show="headings")
        user_list.heading("ID", text="ID")
        user_list.heading("Nombre", text="Nombre")
        user_list.heading("Producto", text="Producto")
        user_list.column("ID", width=50, anchor="center")
        user_list.column("Nombre", width=200, anchor="center")
        user_list.column("Producto", width=200, anchor="center")

        for user in users:
            user_list.insert("", "end", values=user)
        user_list.pack(fill="both", expand=True, pady=10)

    tk.Label(content_frame, text="Escribe tu mensaje:").pack(pady=5)
    message_entry = tk.Entry(content_frame, width=50)
    message_entry.pack(pady=5)

    def send_message():
        selected_item = user_list.focus()
        if not selected_item:
            messagebox.showwarning("Selección Vacía", "Por favor, selecciona un usuario.")
            return

        recipient_id = user_list.item(selected_item)["values"][0]
        message = message_entry.get().strip()

        if not message:
            messagebox.showwarning("Mensaje Vacío", "Por favor, escribe un mensaje.")
            return

        execute_query(
            "INSERT INTO mensajes (id_emisor, id_receptor, mensaje) VALUES (%s, %s, %s)",
            (user_id, recipient_id, message),
        )
        messagebox.showinfo("Éxito", "Mensaje enviado correctamente.")
        message_entry.delete(0, tk.END)

    tk.Button(content_frame, text="Enviar Mensaje", command=send_message, width=20).pack(pady=10)

    # Sección: Mensajes recibidos
    tk.Label(content_frame, text="Mensajes Recibidos:").pack(pady=20)
    received_messages = fetch_data("""
        SELECT m.id_mensaje, u.nombre AS emisor, m.mensaje, m.fecha_envio, m.id_emisor
        FROM mensajes m
        JOIN usuarios u ON m.id_emisor = u.id_usuario
        WHERE m.id_receptor = %s
        ORDER BY m.fecha_envio DESC
    """, (user_id,))
    
    if not received_messages:
        tk.Label(content_frame, text="No tienes mensajes recibidos.").pack(pady=10)
    else:
        message_list = ttk.Treeview(content_frame, columns=("ID", "Emisor", "Mensaje", "Fecha"), show="headings")
        message_list.heading("ID", text="ID")
        message_list.heading("Emisor", text="Emisor")
        message_list.heading("Mensaje", text="Mensaje")
        message_list.heading("Fecha", text="Fecha")
        message_list.column("ID", width=50, anchor="center")
        message_list.column("Emisor", width=150, anchor="center")
        message_list.column("Mensaje", width=300, anchor="center")
        message_list.column("Fecha", width=150, anchor="center")

        for idx, msg in enumerate(received_messages):
            message_list.insert("", "end", iid=idx, values=msg[:-1])  # Excluir id_emisor al mostrar
        message_list.pack(fill="both", expand=True, pady=10)

        def reply_message():
            selected_item = message_list.focus()
            if not selected_item:
                messagebox.showwarning("Selección Vacía", "Por favor, selecciona un mensaje para responder.")
                return

            selected_index = int(selected_item)
            emisor_id = received_messages[selected_index][-1]  # Recuperar id_emisor
            reply_content = message_entry.get().strip()

            if not reply_content:
                messagebox.showwarning("Mensaje Vacío", "Por favor, escribe un mensaje.")
                return

            execute_query(
                "INSERT INTO mensajes (id_emisor, id_receptor, mensaje) VALUES (%s, %s, %s)",
                (user_id, emisor_id, reply_content),
            )
            messagebox.showinfo("Éxito", "Respuesta enviada correctamente.")
            message_entry.delete(0, tk.END)

        tk.Button(content_frame, text="Responder Mensaje", command=reply_message, width=20).pack(pady=10)

    # Frame para el botón "Regresar"
    bottom_frame = tk.Frame(content_frame)
    bottom_frame.pack(side=tk.BOTTOM, fill="x", pady=10)
    tk.Button(bottom_frame, text="Regresar", command=lambda: main_menu(user_id), width=20).pack()




# Modificar la función principal para incluir las nuevas opciones
def main_menu(user_id=None):
    """Pantalla principal después del inicio de sesión."""
    for widget in content_frame.winfo_children():
        widget.destroy()

    tk.Label(content_frame, text="Bienvenido al Sistema de Administración", font=("Arial", 16)).pack(pady=20)

    tk.Button(content_frame, text="Agregar Producto", command=lambda: add_product_screen(user_id)).pack(pady=10)
    tk.Button(content_frame, text="Comprar Producto", command=lambda: buy_product_screen(user_id)).pack(pady=10)
    tk.Button(content_frame, text="Mensajería", command=lambda: message_screen(user_id)).pack(pady=10)
    tk.Button(content_frame, text="Salir", command=logout).pack(pady=10)


# Mostrar la pantalla de inicio
login_screen()

# Ejecutar la aplicación
root.mainloop()
