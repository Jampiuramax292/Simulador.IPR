# Simulador IPR (Streamlit)

Aplicación web para analizar la curva IPR usando modelos de Vogel (reservorio saturado) y Darcy (sub-saturado).

## Estructura mínima para despliegue

- `ipr_streamlit.py`: aplicación principal de Streamlit.
- `requirements.txt`: dependencias para instalación automática.
- `runtime.txt`: versión de Python para Streamlit Cloud.
- `.streamlit/config.toml`: configuración del servidor.

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run ipr_streamlit.py
```

## Subir a GitHub

1. Crea un repositorio nuevo en GitHub.
2. Sube el contenido de esta carpeta (`PRODUTION PYTHON`).
3. Verifica que estén en la raíz: `ipr_streamlit.py` y `requirements.txt`.

## Desplegar en Streamlit Cloud

1. Ve a [https://share.streamlit.io](https://share.streamlit.io).
2. Conecta tu cuenta de GitHub.
3. Selecciona tu repositorio y rama.
4. En **Main file path** usa: `ipr_streamlit.py`.
5. Pulsa **Deploy**.

## Notas

- Evita nombrar el archivo principal como `streamlit.py`, porque puede causar conflictos de importación.