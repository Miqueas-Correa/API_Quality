# 🚀 API Quality

**API Robusta para el Procesamiento y Análisis de Calidad de Audio e Imágenes**

API RESTful desarrollada en Python/Flask que procesa y analiza archivos multimedia (audio e imágenes) para evaluar su calidad técnica. Diseñada para integrarse con aplicaciones frontend y sistemas de gestión de contenido, ofreciendo endpoints especializados para análisis de audio y validación de imágenes.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [🔧 Funcionalidades](#-funcionalidades)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [🚀 Cómo Levantar la API](#-cómo-levantar-la-api)
  - [Ejecución Local](#ejecución-local)
  - [Usando Docker](#usando-docker)
  - [Despliegue en Render](#despliegue-en-render)
- [📡 Endpoints y Uso](#-endpoints-y-uso)
- [🧪 Pruebas](#-pruebas)
- [👨‍💻 Desarrollado por](#-desarrollado-por)
- [🔗 Enlaces Utiles](#-enlaces-utiles)
- [📄 Licencia y Derechos](#-licencia-y-derechos)
- [📅 Información de Lanzamiento](#-información-de-lanzamiento)

---

## 📖 Descripción

**API Quality** es un servicio backend diseñado para procesar archivos multimedia (audio e imágenes) y evaluar su calidad técnica mediante algoritmos especializados. La API recibe archivos a través de solicitudes HTTP POST, los procesa de manera asincrónica y devuelve métricas detalladas sobre la calidad del contenido.

### ¿Qué hace?

- **Procesamiento de Audio**: Analiza archivos de audio (WAV, MP3) extrayendo características como ruido de fondo, frecuencia de muestreo, canales y duración. Aplica filtros de reducción de ruido y genera visualizaciones espectrales.
- **Validación de Imágenes**: Recibe imágenes (PNG, JPG) y evalúa su calidad según parámetros como resolución, formato, tamaño y análisis espectral. Incluye detección de características visuales y validación de integridad.
- **Gestión de Archivos**: Maneja la carga segura de archivos, validación de tipos MIME, límites de tamaño (50MB por defecto), y almacenamiento temporal para procesamiento.
- **API RESTful**: Ofrece endpoints claros y documentados para integración con clientes web, móviles o sistemas automatizados.

### ¿Cómo funciona?

1. **Recepción**: El cliente envía un archivo multimedia mediante `multipart/form-data` a un endpoint específico (`/audio` o `/image`).
2. **Validación**: La API valida el tipo de archivo, tamaño máximo (configurable), y autenticación si está habilitada.
3. **Procesamiento**: 
   - Los archivos se guardan temporalmente en el servidor.
   - Se aplican algoritmos de análisis (espectrogramas, detección de ruido, métricas de calidad).
   - Se generan visualizaciones (gráficos espectrales) y métricas numéricas.
4. **Respuesta**: Retorna un JSON con:
   - Estado de la operación (`success`/`error`)
   - Métricas de calidad (SNR, frecuencia, resolución, etc.)
   - Rutas a archivos generados (visualizaciones, reportes)
   - Timestamp y metadatos del procesamiento

---

## 🔧 Funcionalidades

| Módulo | Descripción | Formatos Soportados |
|--------|-------------|---------------------|
| **Audio Processor** | Análisis de calidad de audio, reducción de ruido, espectrogramas | WAV, MP3, OGG |
| **Image Validator** | Validación de resolución, formato, integridad de imágenes | PNG, JPG, JPEG |
| **File Upload** | Carga segura con validación de tamaño y tipo |Todos los archivos binarios|
| **CORS Enabled** | Compatible con peticiones cross-origin desde cualquier dominio | Configurable |

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje**: Python 3.13+
- **Framework**: Flask 3.1.3
- **Servidor WSGI**: Gunicorn 25.3.0
- **Procesamiento Audio**: pydub, noisereduce, scipy, librosa (implícito)
- **Procesamiento Imágenes**: OpenCV, Pillow, matplotlib
- **CORS**: flask-cors
- **Contenedorización**: Docker
- **Despliegue**: Render (PaaS)

---

## 🚀 Cómo Levantar la API

### Ejecución Local

1. **Clonar repositorio**
   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd API_Quality
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv venv
   .venv\Scripts\Activate.ps1  # Windows
   # o source venv/bin/activate  # Linux/Mac
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno** (opcional)
   Crear un archivo `.env` basado en `.env.example` si existe.

5. **Ejecutar en desarrollo**
   ```bash
   python src/app.py
   ```
   La API estará disponible en `http://localhost:5000`

### Usando Docker

1. **Construir imagen**
   ```bash
   docker build -t api-quality .
   ```

2. **Ejecutar contenedor**
   ```bash
   docker run -p 5000:5000 api-quality
   ```

3. **Con docker-compose** (si existe `docker-compose.yml`)
   ```bash
   docker-compose up
   ```

### Despliegue en Render

La API está desplegada automáticamente en Render. Cada push a la rama principal reconstruye y despliega la aplicación.

**URL de producción**: https://api-quality.onrender.com/

---

## 📡 Endpoints y Uso

### GET `/`
Endpoint de salud de la API.
```json
{
  "message": "API funcionando"
}
```

### POST `/audio`
Procesa archivos de audio.

**Request**:
```bash
curl -X POST https://api-quality.onrender.com/audio \
  -F "file=@audio.wav" \
  -F "options=reduce_noise"
```

**Response**:
```json
{
  "success": true,
  "sample_rate": 44100,
  "channels": 2,
  "duration": 45.2,
  "noise_reduction_applied": true,
  "spectral_plot": "/uploads/spectrogram_123.png",
  "processed_file": "/uploads/processed_audio.wav"
}
```

### POST `/image`
Valida y analiza imágenes.

**Request**:
```bash
curl -X POST https://api-quality.onrender.com/image \
  -F "file=@imagen.jpg" \
  -F "resolution_check=true"
```

**Response**:
```json
{
  "success": true,
  "format": "JPEG",
  "resolution": "1920x1080",
  "size_bytes": 245760,
  "quality_score": 0.92,
  "issues": []
}
```

---

## 🧪 Pruebas

### Colección de Postman
Puedes encontrar la colección completa de endpoints aquí:
**[🔗 Postman Collection - Pendiente de subir]()**

_(Espacio para agregar la URL una vez subida la colección)_

---

## 👨‍💻 Desarrollado por

### Brenda Yañez
**[🔗 Portfolio - Pendiente]()**
*Backend & Audio Processing*

### Miqueas Correa
**[🔗 Portfolio - Pendiente]()**
*Frontend & Image Analysis*

---

## 🔗 Enlaces Utiles

| Recurso | URL |
|---------|-----|
| 🌐 **Web Frontend** | **[🔗 Pendiente]()** - Aplicación web que consume esta API |
| 📡 **API en producción** | https://api-quality.onrender.com/ |
| 🧪 **Pruebas Postman** | **[🔗 Pendiente]()** - Colección de endpoints para testing |
| 📦 **Repositorio** | **[🔗 Pendiente]()** - Código fuente |

---

## 📄 Licencia y Derechos

Todos los derechos reservados © 2026.

Este software es propiedad intelectual de **Brenda Yañez** y **Miqueas Correa**. Queda prohibida su distribución, modificación o uso comercial sin autorización expresa de los autores.

---

## 📅 Información de Lanzamiento

| Campo | Valor |
|-------|-------|
| **Versión Actual** | 1.0.0 |
| **Fecha de Lanzamiento** | [Pendiente de asignar] |
| **Ambiente** | Producción |
| **URL Base** | https://api-quality.onrender.com/ |
| **Estado** | ✅ Activo |

---

**Última actualización**: 2026-04-26
