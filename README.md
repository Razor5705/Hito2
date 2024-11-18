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

