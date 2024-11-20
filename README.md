# Sistema de Gestión de Encuestas sobre Consumo de Alcohol

## Descripción
Este proyecto es una aplicación en Python con interfaz gráfica (Tkinter) para gestionar encuestas relacionadas con el consumo de alcohol y sus efectos. La aplicación permite realizar operaciones CRUD, analizar datos y visualizar gráficos relacionados con los resultados de las encuestas.

---

## Características
- **Operaciones CRUD**: Crear, leer, actualizar y eliminar encuestas.
- **Gráficos estadísticos**: Visualización de datos en gráficos de barras, líneas y circulares.
- **Filtros de datos**: Análisis de alta frecuencia de consumo, pérdida de control, y problemas de salud.
- **Exportación de datos**: Posibilidad de exportar resultados a Excel o PDF (opcional).
- **Interfaz gráfica**: Fácil de usar gracias a Tkinter.

---

## Requisitos
1. **Software necesario:**
   - Python 3.11 o superior
   - MySQL Server
   - Librerías de Python:
     - `mysql-connector-python`
     - `tkinter` (incluida por defecto en Python)
     - `matplotlib`

2. **Base de datos:**
   La base de datos debe ser creada previamente utilizando el archivo `encuestas.sql`.

[https://github.com/Razor5705/Hito2/blob/main/Recursos/encuestas.sql]

---

## Estructura del Proyecto
```plaintext
Hito2/
│
├── codigo_fuente/
│   ├── BD.py                # Código principal de la aplicación
│   ├── conexion.py          # Módulo para gestionar la conexión con MySQL
│   └── graficos.py          # Funciones para la visualización de gráficos
│
├── recursos/
│   ├── capturas/            # Capturas de pantalla de la aplicación
│   └── encuestas.sql        # Script SQL para crear la base de datos
│
├── README.md                # Este archivo con la documentación
└── requirements.txt         # Dependencias necesarias para ejecutar el proyecto

```

# Funciones
## Operaciones CRUD

### Conectar a la Base de Datos:
Explica cómo se conecta la aplicación con la base de datos MySQL.

```python

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
```

### Crear Encuesta: 
Inserta nuevos registros en la base de datos utilizando los datos introducidos por el usuario.

```python

def crear_encuesta(connection, entry_fields, treeview):
    cursor = connection.cursor()
    values = tuple(field.get() for field in entry_fields)
    query = """INSERT INTO ENCUESTA (edad, Sexo, BebidasSemana, CervezasSemana, BebidasFinSemana, 
               BebidasDestiladasSemana, VinosSemana, PerdidasControl, DiversionDependenciaAlcohol, 
               ProblemasDigestivos, TensionAlta, DolorCabeza)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    cursor.execute(query, values)
    connection.commit()
    messagebox.showinfo("Crear Encuesta", "Encuesta creada exitosamente")
    leer_encuestas(connection, treeview)


```

### Leer Encuestas: 
Muestra todas las encuestas almacenadas en un Treeview.

``` python
def leer_encuestas(connection, tree):
    limpiar_treeview(tree)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM ENCUESTA")
    encuestas = cursor.fetchall()
    for encuesta in encuestas:
        tree.insert("", "end", values=encuesta)


```

### Actualizar Encuesta: 
Modifica los datos de un registro existente seleccionado en el Treeview.

``` python
def actualizar_encuesta(connection, entry_fields, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Debe seleccionar una encuesta para actualizar.")
        return
    id_encuesta = tree.item(selected_item[0])['values'][0]
    values = tuple(field.get().strip() for field in entry_fields)
    values += (id_encuesta,)
    query = """
        UPDATE ENCUESTA 
        SET edad=%s, Sexo=%s, BebidasSemana=%s, CervezasSemana=%s, BebidasFinSemana=%s,
            BebidasDestiladasSemana=%s, VinosSemana=%s, PerdidasControl=%s, 
            DiversionDependenciaAlcohol=%s, ProblemasDigestivos=%s, TensionAlta=%s, 
            DolorCabeza=%s 
        WHERE idEncuesta=%s
    """
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    leer_encuestas(connection, tree)
```


### Eliminar Encuesta: 
Elimina un registro seleccionado y actualiza la tabla visualizada.

```
def eliminar_encuesta(connection, tree):
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Error", "Debe seleccionar una encuesta para eliminar.")
        return
    id_encuesta = tree.item(selected_item)["values"][0]
    cursor = connection.cursor()
    cursor.execute("DELETE FROM ENCUESTA WHERE idEncuesta = %s", (id_encuesta,))
    connection.commit()
    leer_encuestas(connection, tree)
```

## Filtros y Consultas:
### Alta Frecuencia: 
Muestra registros con consumo semanal mayor a 10 bebidas.

``` sql
SELECT Edad, BebidasSemana FROM ENCUESTA WHERE BebidasSemana > 10

```
### Pérdida de Control: 
Filtra encuestas donde el usuario ha perdido el control más de tres veces.

``` sql

SELECT Edad, PerdidasControl FROM ENCUESTA WHERE PerdidasControl > 3 order by edad ASC

```

### Problemas de Salud: 
Analiza encuestas con problemas frecuentes como tensión alta y dolores de cabeza.

``` sql

SELECT edad, TensionAlta, 
        DolorCabeza FROM ENCUESTA WHERE TensionAlta =
          'Si' OR DolorCabeza IN ('A menudo', 'Muy a menudo')

```

## Exportación a Excel
### Genera un archivo Excel con todos los datos mostrados en el Treeview.

---

```python
def exportar_excel(tree):
    datos = [tree.item(row)["values"] for row in tree.get_children()]
    df = pd.DataFrame(datos, columns=["ID", "Edad", "Sexo", "BebidasSemana", 
                                      "CervezasSemana", "BebidasFinSemana", 
                                      "BebidasDestiladasSemana", "VinosSemana", 
                                      "PerdidasControl", "DiversionDependenciaAlcohol", 
                                      "ProblemasDigestivos", "TensionAlta", "DolorCabeza"])
    df.to_excel("reporte_encuestas.xlsx", index=False)
    messagebox.showinfo("Exportar", "Datos exportados a Excel correctamente")
```

---

# Gráficos
## Gráficos de Barras: 
Consumo semanal por edad.

``` python

def visualizar_grafico(filtro, connection):
    if filtro == "Alta Frecuencia":
        query = "SELECT Edad, BebidasSemana FROM ENCUESTA WHERE BebidasSemana > 10"
        cursor.execute(query)
        datos = cursor.fetchall()
        edades, consumo = zip(*datos)
        plt.bar(edades, consumo)
        plt.xlabel("Edad")
        plt.ylabel("Bebidas por Semana")
        plt.title("Alta Frecuencia de Consumo de Alcohol")
        plt.show()


```



## Gráficos de Líneas: 
Pérdidas de control por edad.

``` python

elif filtro == "Perdida de Control":
        query = "SELECT Edad, PerdidasControl FROM ENCUESTA WHERE PerdidasControl > 3 order by edad ASC"
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
        plt.show()

```
## Gráficos Circulares: 
Proporción de problemas de salud relacionados con el consumo de alcohol.

``` python

elif filtro == "Problemas de Salud":
        # Filtrar por la edad y problemas de salud (TensiónAlta y DolorCabeza)
        query = """SELECT edad, TensionAlta, 
        DolorCabeza FROM ENCUESTA WHERE TensionAlta =
          'Si' OR DolorCabeza IN ('A menudo', 'Muy a menudo')"""
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
```

``` markdown
El codigo va seguido debido que todo está en una sola función
```
---

Capturas de Pantalla
```markdown

[Pantalla principal][(Recursos/pantalla_principal.jpg)](https://github.com/Razor5705/Hito2/blob/main/Recursos/pantalla_principal.jpg.png)

Ejemplo de Gráficos:
[Graficos]
[Barras][(Recursos/Grafico_Barras.png)](https://github.com/Razor5705/Hito2/blob/main/Recursos/Grafico_Barras.png)

[Lineas][(Recursos/Grafico_Lineas.png)](https://github.com/Razor5705/Hito2/blob/main/Recursos/Grafico_Lineas.png)

[Grafico Circular][(Recursos/Grafico_Circular.png)](https://github.com/Razor5705/Hito2/blob/main/Recursos/Grafico_Circular.png)

```

---

Instrucciones de Uso
# 1º Clonar el repositorio:

```
git clone [<URL-del-repositorio>](https://github.com/Razor5705/Hito2.git)
cd Hito2

```
# 2º Instalar dependencias:
```
pip install -r requirements.txt
```

# 3º Configurar la base de datos:

Ejecutar encuestas.sql en MySQL para crear la tabla.
Actualizar las credenciales de conexión en BD.py o conexion.py.

```sql
CREATE DATABASE ENCUESTAS;
USE ENCUESTAS;

CREATE TABLE ENCUESTA (
    idEncuesta INT AUTO_INCREMENT PRIMARY KEY,
    edad INT NOT NULL,
    Sexo VARCHAR(10) NOT NULL,
    BebidasSemana INT NOT NULL,
    CervezasSemana INT NOT NULL,
    BebidasFinSemana INT NOT NULL,
    BebidasDestiladasSemana INT NOT NULL,
    VinosSemana INT NOT NULL,
    PerdidasControl INT NOT NULL,
    DiversionDependenciaAlcohol VARCHAR(10) NOT NULL,
    ProblemasDigestivos VARCHAR(10) NOT NULL,
    TensionAlta VARCHAR(10) NOT NULL,
    DolorCabeza VARCHAR(10) NOT NULL
);

```


# 4º Ejecutar la aplicación:

```
python BD.py
```
# 5º Operaciones disponibles:

Mostrar:
Lee las encuestas nuevamente si no se actualiza la lista
Registrar: 
Completar los campos y presionar "Crear Encuesta".
Actualizar: 
Seleccionar un registro en el Treeview, modificar los campos y presionar "Actualizar Encuesta".
Eliminar: 
Seleccionar un registro en el Treeview y presionar "Eliminar Encuesta".
Exportar: 
Presionar "Exportar a Excel" para guardar los datos.
Alta Frecuencia:
Muestra el filtro en un grafico de barras
Perdidas de Control:
Muestra este filtro en un gráfico de líneas
Problemas de Salud:
Muestra este filtro en un gráfico circular

---

Referencias

World Health Organization (WHO):
https://www.who.int/
TkDocs:
https://www.tkdocs.com/
MySQL Documentation:
https://dev.mysql.com/
Matplotlib Documentation:
https://matplotlib.org/
Guía de Git y GitHub:
https://www.freecodecamp.org/espanol/news/guia-para-principiantes-de-git-y-github/

---









