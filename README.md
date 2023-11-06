# Proyecto Final: Cloud Computing

## Tabla de contenido
1. [Definición de la Aplicación](#definición-de-la-aplicación)
2. [Funcionalidades, Características y Arquitectura](#funcionalidades-características-y-arquitectura)
3. [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
4. [Tecnologías de Cloud Computing](#tecnologías-de-cloud-computing)

## 1. Definición de la Aplicación

### Clasificador de sentimiento para reseñas de Amazon

Esta aplicación se basa en Inteligencia Artificial y está diseñada para analizar reseñas de productos de Amazon y determinar si son positivas o negativas. Utiliza técnicas avanzadas de procesamiento de lenguaje natural y machine learning para proporcionar resultados precisos en la clasificación de sentimientos.

## 2. Funcionalidades, Características y Arquitectura

### Funcionalidades

- Los usuarios pueden ingresar reseñas de productos a través de la interfaz web para su análisis.
- La aplicación procesa las reseñas y determina si son positivas o negativas.
- Posibilidad de acceder directamente a los modelos entrenados, así como a datos y métricas relacionados.
- Despliegue de la aplicación en contenedores, como Docker, facilitando la replicación, escalabilidad y gestión del sistema.
- Capacidad de manejar grandes conjuntos de datos sin degradar el rendimiento, usando tecnologías como Apache Spark.
- La aplicación cuenta con un modelo SVM ya entrenado, lo que facilita un análisis rápido para nuevos usuarios.
- Interfaz de usuario clara y amigable que permite cargar fácilmente sus reseñas y visualizar los resultados del análisis.
- Utilización de funciones serverless, lo que significa que solo se paga por el tiempo de computación utilizado realmente.

### Características

- Estructura de datos: Los datos de las reseñas se almacenan en archivos parquet en el depósito `amazon-reviews-pds` de Azure Blob Storage. Cada línea de los archivos representa una reseña individual.

### Arquitectura

#### Arquitectura Machine Learning
- Spark Service
- Spark Master
- Workers
- Workers
- Kubernetes Cluster
- Azure Blob Storage

#### Arquitectura Aplicación Web
- Frontend
- Backend
- Almacenamiento

## 3. Ejecución de la Aplicación

- Preparación del entorno:
  - Azure Kubernetes Service
  - Azure Blob Storage
- Contenerización de la aplicación PySpark.
- Acceso a Azure Blob Storage para leer datos y guardar el modelo.
- Despliegue en AKS (Azure Kubernetes Service).
- Entrenamiento: Procesamiento de datos en AKS para entrenar el modelo SVM y guardarlo en Blob Storage.
- Backend (Serverless):
  - Creación de una función en Azure Functions para cargar el modelo entrenado desde Blob Storage y realizar predicciones.
  - Esta función actúa como una API que el frontend puede llamar para obtener predicciones.
- Frontend: Interfaz web donde los usuarios pueden ingresar reseñas.
  - Conexión de la interfaz con el backend para que cuando un usuario ingrese una reseña, se haga una llamada a la función Azure y se muestre el resultado de la clasificación.

## 4. Tecnologías de Cloud Computing

- Azure Web App for Containers
- Azure Machine Learning
- Azure Functions
- Azure Kubernetes Service (AKS)
- Azure Blob Storage

