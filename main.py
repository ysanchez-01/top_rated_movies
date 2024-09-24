import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import openai


# Cargar los datos desde el repositorio de GitHub
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ysanchez-01/top_rated_movies/refs/heads/main/Top_Rated_Movies.csv"
    df = pd.read_csv(url)
    df['release_date'] = pd.to_datetime(
        df['release_date'], errors='coerce')  # Convertir a formato datetime
    df['year'] = df['release_date'].dt.year  # Extraer el año de lanzamiento
    df['month'] = df['release_date'].dt.month  # Extraer el mes de lanzamiento
    return df


df = load_data()

# Título del tablero
st.title("Tablero de Películas")

# Mostrar el total de películas
st.header("Total de películas")
st.write(f"El total de películas es: {df.shape[0]}")

# Gráfico de la distribución de votos
st.header("Distribución de los votos (vote_average)")
plt.figure(figsize=(10, 6))
sns.histplot(df['vote_average'], bins=20, kde=True)
plt.xlabel("Promedio de votos")
plt.ylabel("Frecuencia")
plt.title("Distribución de los votos")
st.pyplot(plt)

# Filtro por año
st.header("Filtrar lanzamientos por año")
years = df['year'].dropna().unique().tolist()
selected_year = st.selectbox("Selecciona el año", sorted(years))

filtered_df = df[df['year'] == selected_year]

# Gráfico de lanzamientos por mes y año
st.header(f"Lanzamientos en el año {selected_year}")
release_counts = filtered_df.groupby('month').size()

plt.figure(figsize=(10, 6))
release_counts.plot(kind='bar')
plt.xlabel("Mes")
plt.ylabel("Cantidad de lanzamientos")
plt.title(f"Lanzamientos por mes en {selected_year}")
st.pyplot(plt)

# Gráfico general de lanzamientos por mes y año
st.header("Lanzamientos por mes y año (todos los años)")
monthly_releases = df.groupby(['year', 'month']).size().unstack().fillna(0)

plt.figure(figsize=(12, 8))
sns.heatmap(monthly_releases, cmap="Blues", linewidths=0.5, annot=False)
plt.xlabel("Mes")
plt.ylabel("Año")
plt.title("Lanzamientos por mes y año")
st.pyplot(plt)

#pip install streamlit pandas seaborn matplotlib

client = openai.OpenAI(api_key=openai_api_key)


def obtener_respuesta(prompt):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Ajusta el modelo según lo que necesites
        messages=[
            {
                "role":
                "system",
                "content":
                """
            Eres un financiero que trabaja para la aseguradora patito, eres experto en el área de solvencia,
            entonces vas a responder todo desde la perspectiva de la aseguradora. Contesta siempre en español
            en un máximo de 50 palabras.
            """
            },  #Solo podemos personalizar la parte de content
            {
                "role": "user",
                "content": prompt
            }
        ])
    output = response.choices[0].message.content
    return output


prompt_user = st.text_area("Ingresa tu pregunta:")

# Obtener y mostrar el resultado
output_modleo = obtener_respuesta(prompt_user)

st.write(output_modleo)
