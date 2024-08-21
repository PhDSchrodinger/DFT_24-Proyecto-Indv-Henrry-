from fastapi import FastAPI, HTTPException
import pandas as pd
import json
from pandas import json_normalize
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


#Esto es en la terminal o en render
# crear entorno virtual:  python -m venv env
#ejecutarlo o activarlo: .\env\Scripts\activate
# ejecutar la FastAPI: uvicorn main:app --reload

# Activar el entorno virtual: .\venv\Scripts\activate
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World, I am Alain"}

# Cargar el dataset
df_Movies_Dc_release_month = pd.read_csv('Movies/Movies_Dc_release_month.csv')

# Convertir todas las cadenas a minúsculas

# Diccionario para mapear meses en español a números
meses = {
    "enero": 1,
    "febrero": 2,
    "marzo": 3,
    "abril": 4,
    "mayo": 5,
    "junio": 6,
    "julio": 7,
    "agosto": 8,
    "septiembre": 9,
    "octubre": 10,
    "noviembre": 11,
    "diciembre": 12
}

##### F1
#### def cantidad_filmaciones_mes( Mes ): 
        # Se ingresa un mes en idioma Español. Debe devolver la cantidad de películas que
        #fueron estrenadas en el mes consultado en la totalidad del dataset.
            ##         Ejemplo de retorno: X cantidad de películas fueron estrenadas en el 
            ##          mes de X
@app.get("/peliculas/{mes}")
def cantidad_de_filmaciones_al_mes(mes: str):
    df_Movies_Dc_release_month = pd.read_csv('Movies/Movies_Dc_release_month.csv')
    mes = mes.lower()  # Convertir el parámetro a minúsculas
    if mes not in meses:
        raise HTTPException(status_code=400, detail="Mes no valido")
    
    mes_numero = meses[mes]

    # Asegurarse de que la columna 'release_month' contiene solo valores numéricos entre 1 y 12
    df_Movies_Dc_release_month['release_month'] = pd.to_numeric(df_Movies_Dc_release_month['release_month'], errors='coerce')
    df_Movies_Dc_release_month = df_Movies_Dc_release_month[df_Movies_Dc_release_month['release_month'].between(1, 12)]

    # Filtrar las películas por el mes dado
    peliculas_en_mes = df_Movies_Dc_release_month[df_Movies_Dc_release_month['release_month'] == mes_numero]
    
    # Contar las filas que corresponden al mes dado
    cantidad_de_filmaciones_al_mes = peliculas_en_mes.shape[0]
    
    return {"mensaje": f"{cantidad_de_filmaciones_al_mes} cantidad de películas fueron estrenadas en el mes de: {mes}"}

##### F2
####   def cantidad_filmaciones_dia( Dia ): Se ingresa un día en idioma Español. 
        # Debe devolver la cantidad de películas que fueron estrenadas en día consultado 
        # en la totalidad del dataset.
            #   Ejemplo de retorno: X cantidad de películas fueron estrenadas en los días X
@app.get("/peliculas/dia/{dia}")
def cantidad_filmaciones_dia(dia: str):
    # Diccionario para traducir los días de la semana al español
    dias_semana_esp = {
        'monday': 'lunes',
        'tuesday': 'martes',
        'wednesday': 'miércoles',
        'thursday': 'jueves',
        'friday': 'viernes',
        'saturday': 'sábado',
        'sunday': 'domingo'
    }
    # Diccionario para traducir los días de la semana al ingles
    dias_semana_ing = {
        'lunes': 'monday',
        'martes': 'tuesday',
        'miércoles': 'wednesday',
        'jueves': 'thursday',
        'viernes': 'friday',
        'sábado': 'saturday',
        'domingo': 'sunday'
    }
    # Leer el dataset
    df_movies = pd.read_csv('Movies/release_title_df.csv')
    # Convertir la columna 'release_date' a formato fecha
    df_movies['release_date'] = pd.to_datetime(df_movies['release_date'], errors='coerce')

    # Crear una nueva columna 'day_of_week' que indique el día de la semana
    df_movies['day_of_week'] = df_movies['release_date'].dt.day_name().str.lower()

    # Convertir el día a minúsculas
    dia = dia.lower()
    # Traducir el día al ingles
    dia = dias_semana_ing.get(dia, dia)
    # Filtrar las películas lanzadas en el dia elejido
    peliculas_en_el_día = df_movies[df_movies['day_of_week'] == dia]

        
    # Contar las filas que corresponden al día dado
    cantidad_peliculas_en_el_dia = peliculas_en_el_día.shape[0]
    # Traducir el día al español
    dia = dias_semana_esp.get(dia, dia)
    return {"mensaje": f"{cantidad_peliculas_en_el_dia} cantidad de películas fueron estrenadas en el día {dia}"}
##### F3
###  def score_titulo( titulo_de_la_filmación ): 
    # Se ingresa el título de una filmación esperando como respuesta el título, 
    # el año de estreno y el score.
        # Ejemplo de retorno: La película X fue estrenada en el año X con un score/popularidad de X
@app.get("/peliculas/titulo_estreno_score/{titulo_de_la_filmacion}")
# Función para obtener el score de una película por título
def score_titulo(titulo_de_la_filmacion):
    # Leer el dataset
    df_movies = pd.read_csv('Movies/release_title_df.csv')
    # Convertir la columna 'release_date' a formato fecha
    df_movies['release_date'] = pd.to_datetime(df_movies['release_date'], errors='coerce')
    # Convertir la columna 'original_title' a minúsculas
    #df_movies['original_title'] = df_movies['original_title'].str.lower()
    # Filtrar la película por título
    pelicula = df_movies[df_movies['original_title'].str.lower() == titulo_de_la_filmacion.lower()]

    # Verificar si la película existe
    if not pelicula.empty:
        # Obtener el título, año de estreno y score
        titulo = pelicula.iloc[0]['original_title']
        anio_estreno = pelicula.iloc[0]['release_date'].year
        score = pelicula.iloc[0]['vote_average']  # el score es = vote_average

        # Formatear el mensaje
        mensaje = f"La película {titulo} fue estrenada en el año {anio_estreno} con un score/popularidad de {score}"
    else:
        # Película no encontrada
        mensaje = f"No se encontró la película con el título {titulo_de_la_filmacion}"

    return {"mensaje": mensaje}


##### F4
###    def votos_titulo( titulo_de_la_filmación ): Se ingresa el título de una 
    # filmación esperando como respuesta el título, la cantidad de votos y el valor promedio 
    # de las votaciones. La misma variable deberá de contar con al menos 2000 valoraciones, 
    # caso contrario, debemos contar con un mensaje avisando que no cumple esta condición y que
    #  por ende, no se devuelve ningun valor.
        # Ejemplo de retorno: La película X fue estrenada en el año X. 
        # La misma cuenta con un total de X valoraciones, con un promedio de X

@app.get("/peliculas/titulo_votos/{titulo_de_la_filmacion}")
def votos_titulo(titulo_de_la_filmacion):
    # Leer el dataset
    df_movies = pd.read_csv('Movies/release_title_df.csv')
    # Convertir la columna 'release_date' a formato fecha
    df_movies['release_date'] = pd.to_datetime(df_movies['release_date'], errors='coerce')
    # Convertir la columna 'original_title' a minúsculas
    df_movies['original_title'] = df_movies['original_title'].str.lower()

    # Filtrar la película por título
    pelicula = df_movies[df_movies['original_title'] == titulo_de_la_filmacion.lower()]

    # Verificar si la película existe
    if not pelicula.empty:
        # Obtener la cantidad de votos
        cantidad_votos = pelicula.iloc[0]['vote_count']
        
        # Verificar si tiene al menos 2000 valoraciones
        if cantidad_votos >= 2000:
            # Obtener el título, año de estreno y promedio de votaciones
            titulo = pelicula.iloc[0]['original_title']
            anio_estreno = pelicula.iloc[0]['release_date'].year
            promedio_votaciones = pelicula.iloc[0]['vote_average']

            # Formatear el mensaje
            mensaje = (f"La película {titulo} fue estrenada en el año {anio_estreno}. "
                       f"La misma cuenta con un total de {cantidad_votos} valoraciones, "
                       f"con un promedio de {promedio_votaciones}")
        else:
            # No cumple con la cantidad mínima de valoraciones
            mensaje = (f"La película {titulo_de_la_filmacion} no cumple con la cantidad mínima "
                       f"de 2000 valoraciones, por ende, no se devuelve ningún valor.")
    else:
        # Película no encontrada
        mensaje = f"No se encontró la película con el título {titulo_de_la_filmacion}"

    return {"mensaje": mensaje}


##### F5
### def get_actor( nombre_actor ): Se ingresa el nombre de un actor que se encuentre dentro de 
    ## un dataset debiendo devolver el éxito del mismo medido a través del retorno. Además, 
    ## la cantidad de películas que en las que ha participado y el promedio de retorno. 
    ## La definición no deberá considerar directores.
      # Ejemplo de retorno: El actor X ha participado de X cantidad de filmaciones, 
      # el mismo ha conseguido un retorno de X con un promedio de X por filmación
@app.get("/actor/{nombre_actor}")
def get_actor(nombre_actor: str):
    # Leer el dataset
    cast_df = pd.read_csv('Movies/cast.csv')
    df_movies = pd.read_csv('Movies/movies_dataset.csv')
    """
    TRate de ejecutar la transformación en la función pero parece es muy lenta mejor cree el archivo
    csv ya con la transformación desanidado y luego lo uelvo aqui dataframe.
    # Convertir la columna 'cast' de JSON a una lista de diccionarios
    credits['cast'] = credits['cast'].apply(ast.literal_eval)

    # Expandir la lista de diccionarios en un DataFrame separado
    cast_df = pd.json_normalize(credits['cast'].explode())"""
    
    # Filtrar las películas por el nombre del actor
    peliculas_actor = cast_df[cast_df['name'].str.contains(nombre_actor, case=False, na=False)]
    
    # Verificar si el actor ha participado en alguna película
    if not peliculas_actor.empty:
        # Calcular la cantidad de películas
        cantidad_peliculas = len(peliculas_actor)
        
        # Calcular el retorno total y el promedio de retorno
        retorno_total = peliculas_actor['revenue'].sum()
        promedio_retorno = peliculas_actor['revenue'].mean()
        
        # Formatear el mensaje
        mensaje = (f"El actor {nombre_actor} ha participado de {cantidad_peliculas} cantidad de filmaciones, "
                   f"el mismo ha conseguido un retorno de {retorno_total} con un promedio de {promedio_retorno} por filmación")
    else:
        # Actor no encontrado
        mensaje = f"No se encontró al actor {nombre_actor} en el dataset"

    return {"mensaje": mensaje}


##### F7  falta el F6
#### def recomendacion( titulo ): Se ingresa el nombre de una 
    ### película y te recomienda las similares en una lista de 5 valores.

    


# Combinar los datasets en uno solo
df1 = pd.read_csv('Movies/df1.csv')
df2 = pd.read_csv('Movies/cast.csv')
df = pd.concat([df1, df2])

# Seleccionar las columnas relevantes
df = df[['title', 'overview']]

# Llenar valores nulos en la columna 'overview'
df['overview'] = df['overview'].fillna('')

# Eliminar filas sin título de película
df = df.dropna(subset=['title'])

# Ver el número de películas después de eliminar filas sin título
num_peliculas = len(df)
print(f"El número de películas es: {num_peliculas}")

# Reducir el tamaño del conjunto de datos
df = df.sample(n=3000, random_state=42)
print(df.head())

# Vectorización de los títulos y descripciones
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(df['title'] + " " + df['overview'])

# Verificar que la matriz TF-IDF es dispersa
print(type(tfidf_matrix))  # Debería imprimir <class 'scipy.sparse.csr.csr_matrix'>

# Cálculo de la similitud del coseno
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

#Ruta de la API para la recomendación
@app.get("/peli/{titulo}")
# Función de recomendación
def recomendacion(titulo:str):
    # Normalizar el título de entrada
    titulo = titulo.strip().lower()
    
    # Normalizar los títulos en el DataFrame
    df['title_normalized'] = df['title'].str.strip().str.lower()
    
    # Verificar si el título existe en el DataFrame
    if titulo not in df['title_normalized'].values:
        return f"No se encontró la película con el título '{titulo}'"
    
    # Obtener el índice de la película que coincide con el título
    idx = df[df['title_normalized'] == titulo].index[0]
    
    # Obtener las puntuaciones de similitud de todas las películas con esa película
    sim_scores = list(enumerate(cosine_sim[idx]))
    
    # Ordenar las películas basadas en las puntuaciones de similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtener los índices de las 5 películas más similares
    sim_scores = sim_scores[1:6]
    
    # Obtener los títulos de las películas más similares
    movie_indices = [i[0] for i in sim_scores]
    recomendaciones = df['title'].iloc[movie_indices].tolist()
    
    return{"Recomendaciones": recomendaciones}
