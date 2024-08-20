# DFT_24-Proyecto-Indv-Henrry-
Proyecto Individual de Data Science Analizando un DataSet para empresas de  streaming de peliculas

¡Claro! Aquí tienes un ejemplo de README para tu proyecto individual de MLOps:

---

# Proyecto Individual Nº1: Machine Learning Operations (MLOps)

## Introducción

¡Bienvenidos al primer proyecto individual de la etapa de Labs! En este proyecto, te colocarás en el rol de un MLOps Engineer en una start-up que provee servicios de agregación de plataformas de streaming. Tu objetivo es desarrollar un sistema de recomendación que no solo funcione bien, sino que también esté listo para ser desplegado en un entorno de producción.

## Contexto

El ciclo de vida de un proyecto de Machine Learning abarca desde el tratamiento y recolección de datos hasta el entrenamiento y mantenimiento de los modelos a medida que llegan nuevos datos. En este proyecto, trabajarás como Data Scientist en una start-up y tu misión será crear un sistema de recomendación para un servicio de streaming, partiendo desde datos que están en crudo y requieren un procesamiento significativo.

### Problemas a Resolver

- **Datos desordenados:** Los datos están anidados, sin transformar, y carecen de procesos automatizados para su actualización.
- **Falta de madurez en los datos:** Los datos presentan valores nulos y formatos inconsistentes que deben ser corregidos para poder utilizarlos en un modelo de Machine Learning.
- **Creación de un MVP:** Debes trabajar rápido para entregar un Producto Mínimo Viable (MVP) en las próximas semanas.

## Propuesta de Trabajo

### 1. Transformaciones de Datos

Para construir el MVP, se realizaron las siguientes transformaciones:

- **Desanidamiento de datos:** Columnas como `belongs_to_collection`, `production_companies`, entre otras, fueron desanidadas para facilitar su uso.
- **Manejo de valores nulos:** Los valores nulos en las columnas `revenue` y `budget` fueron reemplazados por `0`. Los valores nulos en la columna `release_date` fueron eliminados.
- **Formato de fechas:** Las fechas en la columna `release_date` fueron convertidas al formato `AAAA-mm-dd`, y se creó una nueva columna `release_year` que extrae el año de la fecha de estreno.
- **Retorno de inversión:** Se añadió una columna `return` que calcula el retorno de inversión como `revenue / budget`. Si no hay datos disponibles, el valor se establece en `0`.
- **Eliminación de columnas innecesarias:** Se eliminaron las columnas `video`, `imdb_id`, `adult`, `original_title`, `poster_path`, y `homepage`.

### 2. Desarrollo de la API

La API fue desarrollada utilizando el framework **FastAPI** y cuenta con los siguientes endpoints:

- **`/cantidad_filmaciones_mes/{mes}`**: Devuelve la cantidad de películas estrenadas en un mes dado (en español).
- **`/cantidad_filmaciones_dia/{dia}`**: Devuelve la cantidad de películas estrenadas en un día específico (en español).
- **`/score_titulo/{titulo}`**: Devuelve el título, año de estreno y el score de la película solicitada.
- **`/votos_titulo/{titulo}`**: Devuelve el título, cantidad de votos y el promedio de votaciones para una película, siempre que tenga al menos 2000 valoraciones.
- **`/get_actor/{nombre_actor}`**: Devuelve el éxito de un actor medido a través del retorno, cantidad de películas en las que ha participado y el promedio de retorno.
- **`/get_director/{nombre_director}`**: Devuelve el éxito de un director, el nombre de cada película, la fecha de lanzamiento, el retorno individual, costo y ganancia de la misma.

### 3. Despliegue

La API fue desplegada utilizando **Render** (o la plataforma elegida), permitiendo que sea accesible desde la web para su consumo.

### 4. Análisis Exploratorio de Datos (EDA)

Se realizó un análisis exploratorio de los datos para investigar relaciones entre las variables, detectar outliers y patrones interesantes. Este análisis incluyó:

- **Nube de palabras:** Para visualizar las palabras más frecuentes en los títulos de las películas, lo que podría ser útil para el sistema de recomendación.
- **Gráficas de distribución:** Para entender la distribución de variables como `budget`, `revenue`, y `release_year`.

### 5. Sistema de Recomendación

Se desarrolló un sistema de recomendación que, dado el título de una película, devuelve una lista de 5 películas similares basadas en la similitud de puntuación. Esta función se desplegó como un endpoint adicional en la API.

- **`/recomendacion/{titulo}`**: Devuelve una lista de 5 películas similares al título ingresado.

### 6. Video Demostrativo

Se creó un video demostrativo de menos de 7 minutos que muestra el funcionamiento de las consultas requeridas en la API y una breve explicación del modelo de Machine Learning utilizado para el sistema de recomendación.

## Estructura del Proyecto

```
/project
│
├── /data/               # Contiene los datasets originales
│   ├── movies_dataset.csv
│   └── credits.csv
│
├── /notebooks/          # Notebooks para limpieza de datos y EDA
│   ├── data_cleaning.ipynb
│   └── eda.ipynb
│
├── /app/                # Código de la API
│   ├── main.py
│   ├── models.py
│   └── requirements.txt
│
├── /models/             # Modelos entrenados
│   └── recommendation_model.pkl
│
├── README.md            # Este archivo
├── video_demo.mp4       # Video demostrativo del proyecto
└── .gitignore           # Archivos y directorios a ignorar por Git
```

## Requisitos

- **Python 3.x**
- **FastAPI**
- **pandas**
- **scikit-learn**

## Instrucciones para Ejecutar

1. Clona este repositorio.
2. Instala las dependencias con `pip install -r requirements.txt`.
3. Ejecuta la API con el comando `uvicorn app.main:app --reload`.
4. Accede a `http://127.0.0.1:8000` para probar los endpoints.

## Conclusión

Este proyecto abarca desde la limpieza y transformación de datos hasta el desarrollo y despliegue de un sistema de recomendación basado en Machine Learning. ¡Espero que lo disfruten tanto como yo disfruté desarrollarlo!

---

Este README cubre los puntos clave de tu proyecto y sigue las mejores prácticas para documentar trabajos en GitHub. ¡Éxito con tu proyecto!
