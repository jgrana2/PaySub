# ¡Bienvenido a PaySub!

Simple. Directo. Suscripciones Hechas Correctamente.

## ¿Qué es PaySub?
PaySub es una plataforma diseñada para permitir a creadores configurar y gestionar sus propios paquetes de suscripción, simplificando el proceso de monetización de contenido o servicios. Este repositorio contiene el código del proyecto PaySub, que es una solución de código abierto para la creación y gestión de suscripciones.

### ¡Comienza a utilizar PaySub para manejar tus clientes!

Si prefieres evitar la configuración y mantenimiento de la infraestructura, tenemos una solución perfecta para ti. PaySub ofrece una versión alojada en la nube, lo que te permite empezar a gestionar tus clientes de inmediato sin preocupaciones técnicas adicionales.

Visita **[www.paysub.app](http://www.paysub.app)** y descubre cómo nuestra aplicación en la nube puede simplificar la administración de tus clientes y suscripciones. Con PaySub cloud-hosted, puedes enfocarte completamente en tu negocio mientras nosotros nos encargamos del resto.

### Instrucciones para Ejecutar el Proyecto

Para poner en marcha tu propia instancia de PaySub, sigue los siguientes pasos:

#### Requisitos previos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

- Node.js (Recomendamos la versión LTS).
- Python 3.9.
- Una cuenta en Appwrite Cloud.
- Git para clonar el repositorio.

### Configuración de Appwrite para el Frontend

PaySub utiliza Appwrite Cloud como una solución backend serverless. Para configurarlo:

1. Asegúrate de tener una cuenta en [Appwrite Cloud](https://appwrite.io/) y de haber creado un proyecto.

2. Obtiene los ID's necesarios para las colecciones, buckets y la base de datos de tu proyecto de Appwrite. Serán utilizados en el archivo de configuración que crearás a continuación.

3. En la carpeta `src/lib` del proyecto frontend de SvelteKit, necesitarás crear un archivo de configuración llamado `config.js`. Este archivo debe contener la información de configuración de tu proyecto Appwrite de la siguiente manera:

   🚨 **Aviso Importante**: Asegúrate de que este archivo esté bien protegido y **NO** sea rastreado por el control de versiones (como Git). Debes agregar `config.js` al archivo `.gitignore` para prevenir que se suba al repositorio remoto.

```javascript
// src/lib/config.js
// Asegúrate de que este archivo está en .gitignore y no es rastreado por el control de versiones.

export const config = {
    SUBSCRIPTIONS_COLLECTION_ID: 'tu_appwrite_id_para_suscripciones',
    SUBSCRIBERS_COLLECTION_ID: 'tu_appwrite_id_para_suscriptores',
    CARDS_COLLECTION_ID: 'tu_appwrite_id_para_tarjetas',
    IMAGES_BUCKET_ID: 'tu_appwrite_id_para_imagenes',
    DATABASE_ID: 'tu_appwrite_id_para_base_de_datos',
    ACCESS_TOKENS_COLLECTION_ID: 'tu_appwrite_id_para_tokens_de_acceso'
};
```

4. Recuerda reemplazar `'tu_appwrite_id_para_xxx'` con los ID's específicos obtenidos desde tu consola de Appwrite.

Una vez hayas creado y configurado el archivo `config.js`, el proyecto frontend debería ser capaz de comunicarse con Appwrite y realizar operaciones como almacenar suscripciones, manejar suscriptores y gestionar imágenes y tarjetas.

Procede con el resto de la instalación y ejecución del frontend como se describió anteriormente en este documento.

#### Pasos de Instalación para el Frontend

La carpeta `frontend` contiene un proyecto de SvelteKit. Para ejecutarlo:

1. Navega a la carpeta `frontend`:
   ```sh
   cd frontend
   ```
   
2. Instala las dependencias de Node.js utilizando `npm`:
   ```sh
   npm install
   ```

3. Inicia el servidor de desarrollo de SvelteKit:
   ```sh
   npm run dev
   ```
   El proyecto frontend ahora estará disponible en `http://localhost:3000`.

### Configuración de Variables de Entorno para el Backend

Para el backend del sistema PaySub, es fundamental configurar las siguientes variables de entorno. Estas variables permitirán que la aplicación se autentique y comunique con Appwrite Cloud:

```plaintext
APPWRITE_API_KEY=your_appwrite_api_key
PROJECT_ID=your_appwrite_project_id
DATABASE_ID=your_appwrite_database_id
CARDS_COLLECTION_ID=your_appwrite_cards_collection_id
SUBSCRIPTIONS_COLLECTION_ID=your_appwrite_subscriptions_collection_id
SUBSCRIBERS_COLLECTION_ID=your_appwrite_subscribers_collection_id
ACCESS_TOKENS_COLLECTION_ID=your_appwrite_access_tokens_collection_id
IMAGES_BUCKET_ID=your_appwrite_images_bucket_id
ENCRYPTION_KEY=your_encryption_key
```

Sigue los pasos a continuación para configurar estas variables en tu entorno local o servidor:

1. Abre tu terminal favorita o accede al panel de configuración de variables de entorno de tu servicio de hosting.
   
2. Define cada variable de entorno utilizando los comandos adecuados o a través de la interfaz proporcionada por tu servicio de hospedaje.
   
3. Asegúrate de reemplazar `your_appwrite_xxx` con los valores reales que correspondan a las propiedades de tu proyecto en Appwrite y `your_encryption_key` con una clave de cifrado segura generada por ti.

   🚨 **Aviso Importante**: Maneja estas claves con cuidado y nunca las expongas públicamente. Si estás usando un sistema de control de versiones, no incluyas estas claves en tus archivos de configuración que se rastrean. En su lugar, utiliza variables de entorno del sistema o configúralas directamente en tu plataforma de despliegue.

Una vez establecidas, estas variables permiten que tu backend interactúe correctamente con Appwrite, llevando a cabo operaciones como la gestión de colecciones de datos, almacenamiento de imágenes, autenticación y más.

#### Pasos de Instalación para el Backend

La carpeta `backend` contiene un proyecto de Python 3.9. Para ejecutarlo:

1. Navega a la carpeta `backend`:
   ```sh
   cd backend
   ```
   
2. Crea un entorno virtual de Python:
   ```sh
   python -m venv env
   ```

3. Activa el entorno virtual:
   - En Windows:
     ```sh
     .\env\Scripts\activate
     ```
   - En Unix o MacOS:
     ```sh
     source env/bin/activate
     ```

4. Instala las dependencias del proyecto con `pip`:
   ```sh
   pip install -r requirements.txt
   ```

5. Inicia el servidor de la API:
   ```sh
   python APIServer.py
   ```
   Asegúrate de que el servidor frontend está configurado para comunicarse con este servidor backend.

### Contribuyendo

PaySub es un proyecto de código abierto y animamos a los desarrolladores a contribuir. Para empezar:

1. Fork el repositorio.
2. Crea una nueva rama para cada característica o mejora.
3. Envía tus cambios con un pull request detallado.

¡Todas las contribuciones son bienvenidas!

## Registro e Inicio de Sesión

¿Nuevo en PaySub? Puedes comenzar registrándote en la plataforma y siguiendo los pasos para configurar tu perfil y suscripciones.

### Soporte

Si experimentas problemas técnicos o tienes preguntas, puedes obtener ayuda poniéndote en contacto a través del email de soporte proporcionado en la sección de soporte del sitio web oficial.

## Únete a PaySub Hoy

Con PaySub, lanzar un negocio basado en suscripciones es fácil y directo. No esperes más para monetizar tu contenido o servicios. ¡Empieza hoy mismo con PaySub!

---

Esperamos que disfrutes utilizando PaySub tanto como nosotros disfrutamos creándolo. ¡Te deseamos éxito en tu emprendimiento!

¡Feliz suscripción! 🌟