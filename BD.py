import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Aplicar tema a la aplicación
style = ttk.Style()
style.theme_use("clam")

# Configurar estilos personalizados
style.configure("TButton",
                padding=6,
                relief="flat",
                background="#4CAF50",  # Color de fondo del botón
                foreground="white")  # Color de texto del botón

style.configure("TLabel",
                background="#f0f0f0",  # Fondo de las etiquetas
                font=("Helvetica", 10))

style.configure("TEntry",
                padding=5,
                relief="flat",
                font=("Helvetica", 10))

style.configure("TTreeview",
                background="#f9f9f9",  # Fondo de la tabla
                foreground="black",
                fieldbackground="#f9f9f9",
                font=("Helvetica", 10))

def crear_encuesta(connection, entry_fields, treeview):
    cursor = connection.cursor()
    values = tuple(field.get() for field in entry_fields)
    query = """INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, ProblemasDigestivos, TensionAlta, DolorCabeza)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, values)
    connection.commit()
    messagebox.showinfo("Crear Encuesta", "Encuesta creada exitosamente")
    leer_encuestas(connection, treeview)

# Función para cargar las encuestas en el Treeview
def leer_encuestas(connection, tree):
    # Limpiar el Treeview antes de cargar los datos
    for row in tree.get_children():
        tree.delete(row)
    
    # Obtener todas las encuestas de la base de datos
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ENCUESTA")
    encuestas = cursor.fetchall()

    # Insertar las encuestas en el Treeview
    for encuesta in encuestas:
        tree.insert("", "end", values=encuesta)

# Función para actualizar los datos en la base de datos (CRUD)
def actualizar_encuesta(connection, entry_fields, tree):
    # Obtener el ID de la encuesta desde el primer campo (ID)
    id_encuesta = entry_fields[0].get()
    
    # Verificar que el ID no esté vacío
    if not id_encuesta:
        messagebox.showerror("Error", "Debe seleccionar una encuesta para actualizar.")
        return

    # Recoger los valores de los campos de entrada
    values = tuple(field.get() for field in entry_fields[1:])  # Excluir el primer campo (ID) del tuple
    values += (id_encuesta,)  # Agregar el ID al final de los valores para la consulta

    # Ejecutar la consulta de actualización
    cursor = connection.cursor()
    query = """UPDATE ENCUESTA SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s,
               BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, DiversionDependenciaAlcohol=%s,
               ProblemasDigestivos=%s, TensionAlta=%s, DolorCabeza=%s WHERE idEncuesta=%s"""
    cursor.execute(query, values)
    connection.commit()

    # Mostrar mensaje de éxito
    messagebox.showinfo("Actualizar Encuesta", "Encuesta actualizada exitosamente")
    
    # Recargar las encuestas en el Treeview
    leer_encuestas(connection, tree)

# Función para eliminar una encuesta de la base de datos (CRUD)
def eliminar_encuesta(connection, entry_fields, tree):
    # Obtener el ID de la encuesta desde el primer campo (ID)
    id_encuesta = entry_fields[0].get()

    # Verificar que el ID no esté vacío
    if not id_encuesta:
        messagebox.showerror("Error", "Debe seleccionar una encuesta para eliminar.")
        return

    # Ejecutar la consulta de eliminación
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ENCUESTA WHERE idEncuesta = %s", (id_encuesta,))
    connection.commit()

    # Mostrar mensaje de éxito
    messagebox.showinfo("Eliminar Encuesta", "Encuesta eliminada exitosamente")

    # Recargar las encuestas en el Treeview
    leer_encuestas(connection, tree)

# Función para exportar los datos a un archivo Excel
def exportar_excel(tree):
    # Obtener los datos del Treeview
    datos = [tree.item(row)["values"] for row in tree.get_children()]

    # Verificar si hay datos
    if not datos:
        messagebox.showwarning("Advertencia", "No hay datos para exportar.")
        return

    # Crear el DataFrame y exportar a Excel
    df = pd.DataFrame(datos, columns=["ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana",
                                      "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl",
                                      "DiversionDependenciaAlcohol", "ProblemasDigestivos", "TensionAlta", "DolorCabeza"])
    df.to_excel("reporte_encuestas.xlsx", index=False)
    
    # Mostrar mensaje de éxito
    messagebox.showinfo("Exportar", "Datos exportados a Excel correctamente")



def visualizar_grafico(filtro, connection):
    print(f"Filtro recibido: {filtro}")  # Depuración

    cursor = connection.cursor()

    if filtro == "Alta Frecuencia":
        query = "SELECT Edad, BebidasSemana FROM ENCUESTA WHERE BebidasSemana > 10"
        cursor.execute(query)
        datos = cursor.fetchall()

        if datos:
            edades, consumo = zip(*datos)
            plt.bar(edades, consumo)
            plt.xlabel("Edad")
            plt.ylabel("Bebidas por Semana")
            plt.title("Alta Frecuencia de Consumo de Alcohol")
        else:
            print("No hay datos para 'Alta Frecuencia'.")

    elif filtro == "Perdida de Control":
        query = "SELECT Edad, PerdidasControl FROM ENCUESTA WHERE PerdidasControl > 3"
        cursor.execute(query)
        datos = cursor.fetchall()

        if datos:
            edades, perdidas = zip(*datos)
            plt.plot(edades, perdidas, marker='o')
            plt.xlabel("Edad")
            plt.ylabel("Pérdidas de Control")
            plt.title("Pérdidas de Control por Edad")
        else:
            print("No hay datos para 'Perdida de Control'.")

    elif filtro == "Problemas de Salud":
        # Filtrar por la edad y problemas de salud (TensiónAlta y DolorCabeza)
        query = """SELECT edad, TensionAlta, DolorCabeza FROM ENCUESTA WHERE TensionAlta = 'Si' OR DolorCabeza IN ('A menudo', 'Muy a menudo')"""
        cursor.execute(query)
        datos = cursor.fetchall()

        if datos:
            # Inicializa los contadores
            edad_problemas = {}  # Diccionario para contar problemas por grupo de edad
            for row in datos:
                edad = row[0]
                tension_alta = row[1]
                dolor_cabeza = row[2]

                # Si hay Tensión Alta o Dolor de Cabeza frecuente, cuenta la edad
                if tension_alta == 'Si' or dolor_cabeza in ['A menudo', 'Muy a menudo']:
                    if edad in edad_problemas:
                        edad_problemas[edad] += 1
                    else:
                        edad_problemas[edad] = 1

            # Si no hay datos para graficar
            if not edad_problemas:
                print("No hay datos suficientes para generar el gráfico.")
                return

            # Prepara los datos para el gráfico
            edades = list(edad_problemas.keys())
            conteo_problemas = list(edad_problemas.values())

            # Reemplazar NaN por 0, aunque no debería haber NaN aquí
            conteo_problemas = np.nan_to_num(conteo_problemas, nan=0)

            # Verifica si todos los valores son cero
            if all(v == 0 for v in conteo_problemas):
                print("Todos los valores son cero, no se puede generar el gráfico.")
                return

            # Genera el gráfico circular
            plt.pie(conteo_problemas, labels=edades, autopct='%1.1f%%', startangle=90, colors=['orange', 'red'])
            plt.title("Proporción de Problemas de Salud Relacionados con Alcohol por Edad")

        else:
            print("No hay datos para 'Problemas de Salud'.")

    else:
        print(f"Filtro no reconocido: {filtro}")

    # Mostrar el gráfico
    plt.show()


   

    

# Limpiar Treeview
def limpiar_treeview(tree):
    for item in tree.get_children():
        tree.delete(item)

def seleccionar_fila(event, entry_fields, treeview):
    # Obtener el item seleccionado
    selected_item = treeview.selection()
    if selected_item:
        # Obtener los valores de la fila seleccionada
        item_values = treeview.item(selected_item[0], "values")
        
        # Llenar los campos de entrada con los valores de la fila seleccionada
        for i, field in enumerate(entry_fields):
            field.delete(0, tk.END)  # Limpiar el campo
            field.insert(0, item_values[i + 1])  # Insertar el valor (saltamos el ID)

def open_main_window(connection):
    root.destroy()
    
    main_window = tk.Tk()
    main_window.title("Gestión de Encuestas de Salud")
    main_window.geometry("1200x600")
    main_window.configure(bg="#f0f0f0")

    # Crear Treeview con un borde
    treeview = ttk.Treeview(main_window, selectmode="browse", height=10)
    treeview['columns'] = ("ID", "Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependencia", "ProblemasDigestivos", "TensionAlta", "DolorCabeza")
    
    for col in treeview['columns']:
        treeview.heading(col, text=col)
        treeview.column(col, anchor=tk.CENTER, width=100)
    
    treeview.pack(pady=20)

    # Frame para formularios
    form_frame = ttk.Frame(main_window, padding=10)
    form_frame.pack(pady=10)

    # Lista para los campos de entrada
    entry_fields = []
    labels = ["Edad", "Sexo", "BebidasSemana", "CervezasSemana", "BebidasFinSemana", 
              "BebidasDestiladasSemana", "VinosSemana", "PerdidasControl", "DiversionDependenciaAlcohol", 
              "ProblemasDigestivos", "TensionAlta", "DolorCabeza"]

    for idx, label in enumerate(labels):
        ttk.Label(form_frame, text=label).grid(row=idx, column=0, sticky="w", padx=10, pady=5)
        entry = ttk.Entry(form_frame)
        entry.grid(row=idx, column=1, padx=10, pady=5)
        entry_fields.append(entry)

    # Botones CRUD
    buttons_frame = ttk.Frame(main_window, padding=10)
    buttons_frame.pack(pady=20)
    ttk.Button(buttons_frame, text="Crear Encuesta", command=lambda: crear_encuesta(connection, entry_fields, treeview)).grid(row=0, column=0, padx=10)
   # Llamada a los botones con los parámetros correctos
    ttk.Button(buttons_frame, text="Actualizar Encuesta", 
           command=lambda: actualizar_encuesta(connection, entry_fields, treeview)).grid(row=0, column=1, padx=10)

    ttk.Button(buttons_frame, text="Eliminar Encuesta", 
           command=lambda: eliminar_encuesta(connection, entry_fields, treeview)).grid(row=0, column=2, padx=10)

    ttk.Button(buttons_frame, text="Exportar a Excel", 
           command=lambda: exportar_excel(treeview)).grid(row=0, column=3, padx=10)


    # Botones de consultas
    consultas_frame = ttk.Frame(main_window, padding=10)
    consultas_frame.pack(pady=20)
    ttk.Button(consultas_frame, text="Alta Frecuencia", command=lambda: visualizar_grafico("Alta Frecuencia", connection)).grid(row=0, column=0, padx=10)
    ttk.Button(consultas_frame, text="Perdida de Control", command=lambda: visualizar_grafico("Perdida de Control", connection)).grid(row=0, column=1, padx=10)
    ttk.Button(consultas_frame, text="Problemas Salud", command=lambda: visualizar_grafico("Problemas de Salud", connection)).grid(row=0, column=2, padx=10)

    # Llamar a la función para leer encuestas al iniciar
    leer_encuestas(connection, treeview)

    # Vincular el evento de selección de una fila
    treeview.bind("<ButtonRelease-1>", lambda event: seleccionar_fila(event, entry_fields, treeview))

    # Cerrar conexión al cerrar la ventana
    def on_closing():
        connection.close()
        main_window.destroy()

    main_window.protocol("WM_DELETE_WINDOW", on_closing)
    main_window.mainloop()




# Función de conexión
def connect(user, password):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='ENCUESTAS',
            user=user,
            password=password
        )
        if connection.is_connected():
            messagebox.showinfo("Conexión", "Conexión exitosa a la base de datos")
        return connection
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error: {e}")
        return None

# Función de inicio de sesión
def iniciar_sesion():
    user = user_entry.get()
    password = password_entry.get()
    connection = connect(user, password)
    if connection:
        open_main_window(connection)
    else:
        messagebox.showerror("Error", "Credenciales incorrectas. Inténtalo de nuevo.")

# Crear ventana de inicio de sesión
root = tk.Tk()
root.title("Inicio de Sesión")
root.geometry("300x200")

# Widgets de inicio de sesión
ttk.Label(root, text="Usuario").pack(pady=10)
user_entry = ttk.Entry(root)
user_entry.pack(pady=5)

ttk.Label(root, text="Contraseña").pack(pady=10)
password_entry = ttk.Entry(root, show="*")
password_entry.pack(pady=5)



ttk.Button(root, text="Iniciar sesión", command=iniciar_sesion).pack(pady=20)

root.mainloop()