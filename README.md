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
   La base de datos debe ser creada previamente utilizando el archivo `db_schema.sql`.

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
│   └── db_schema.sql        # Script SQL para crear la base de datos
│
├── README.md                # Este archivo con la documentación
└── requirements.txt         # Dependencias necesarias para ejecutar el proyecto

```


### b. **Ejemplos de Uso**
Incluye capturas de pantalla o GIFs mostrando cómo funciona la aplicación:
```markdown
## Ejemplo de Uso
### Pantalla principal
![Pantalla principal](recursos/capturas/pantalla_principal.png)

### Gráfico de barras
![Gráfico de barras](recursos/capturas/grafico_barras.png)


```
# Funciones
## Operaciones CRUD
### Crear Encuesta: 
Inserta nuevos registros en la base de datos utilizando los datos introducidos por el usuario.
### Leer Encuestas: 
Muestra todas las encuestas almacenadas en un Treeview.
### Actualizar Encuesta: 
Modifica los datos de un registro existente seleccionado en el Treeview.
### Eliminar Encuesta: 
Elimina un registro seleccionado y actualiza la tabla visualizada.
## Filtros y Consultas:
### Alta Frecuencia: 
Muestra registros con consumo semanal mayor a 10 bebidas.
### Pérdida de Control: 
Filtra encuestas donde el usuario ha perdido el control más de tres veces.
### Problemas de Salud: 
Analiza encuestas con problemas frecuentes como tensión alta y dolores de cabeza.
## Exportación a Excel
### Genera un archivo Excel con todos los datos mostrados en el Treeview.

# Gráficos
## Gráficos de Barras: C
onsumo semanal por edad.
## Gráficos de Líneas: 
Pérdidas de control por edad.
## Gráficos Circulares: 
Proporción de problemas de salud relacionados con el consumo de alcohol.


Capturas de Pantalla
```markdown

[Pantalla principal](recursos/pantalla_principal.jpg)

Ejemplo de Gráficos:
[Graficos]
[Barras]
(Recursos/Grafico_Barras.png)

[Lineas]
(Recursos/Grafico_Lineas.png)

[Grafico Circular]
(Recursos/Grafico_Circular.png)

```
Instrucciones de Uso
# 1º Clonar el repositorio:

```
git clone <URL-del-repositorio>
cd Hito2

```
# 2º Instalar dependencias:
```
pip install -r requirements.txt
```

# 3º Configurar la base de datos:

Ejecutar encuestas.sql en MySQL para crear la tabla.
Actualizar las credenciales de conexión en BD.py o conexion.py.

# 4º Ejecutar la aplicación:

```
python BD.py
```
# 5º Operaciones disponibles:

Registrar: Completar los campos y presionar "Crear Encuesta".
Actualizar: Seleccionar un registro en el Treeview, modificar los campos y presionar "Actualizar Encuesta".
Eliminar: Seleccionar un registro en el Treeview y presionar "Eliminar Encuesta".
Exportar: Presionar "Exportar a Excel" para guardar los datos.

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











