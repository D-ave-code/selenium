from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
import os
import glob
from datetime import datetime
import subprocess
import sys
import base64

app = FastAPI(title="Selenium Form API", description="API para ejecutar formulario y devolver capturas", version="1.0.0")

# Montar archivos estáticos para servir las imágenes
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "mensaje": "API de Selenium Form",
        "descripcion": "Ejecuta el formulario y devuelve las capturas de pantalla",
        "endpoints": {
            "/ejecutar": "Ejecuta el script de selenium y devuelve información",
            "/capturas": "Devuelve las últimas 2 capturas tomadas",
            "/imagen/{nombre_archivo}": "Descarga una imagen específica"
        }
    }

@app.post("/ejecutar")
async def ejecutar_formulario():
    """Ejecuta el script de selenium y devuelve el resultado con las imágenes"""
    try:
        # Ejecutar el script app.py
        result = subprocess.run([sys.executable, "app.py"], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.getcwd())
        
        # Buscar las imágenes generadas
        archivos_png = glob.glob("*.png")
        archivos_png.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Obtener las 2 más recientes
        capturas_binarias = []
        if archivos_png:
            ultimas_capturas = archivos_png[:2]
            
            for archivo in ultimas_capturas:
                try:
                    # Leer la imagen sin compresión y convertirla a base64
                    with open(archivo, "rb") as image_file:
                        image_bytes = image_file.read()
                        # Convertir directamente a base64 sin pérdida de calidad
                        image_data = base64.b64encode(image_bytes).decode('utf-8')
                    
                    # Obtener información del archivo
                    stat = os.stat(archivo)
                    
                    capturas_binarias.append({
                        "nombre": archivo,
                        "es_inicio": "_inicio_" in archivo,
                        "es_final": "_final_" in archivo,
                        "tamaño_bytes": stat.st_size,
                        "binary": {
                            "data": image_data,
                            "mimeType": "image/png",
                            "fileName": archivo,
                            "fileExtension": "png"
                        }
                    })
                except Exception as e:
                    print(f"Error al procesar imagen {archivo}: {e}")
        
        if result.returncode == 0:
            return {
                "status": "success",
                "mensaje": "Formulario ejecutado correctamente",
                "output": result.stdout,
                "capturas": capturas_binarias,
                "total_capturas": len(capturas_binarias),
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "status": "error", 
                "mensaje": "Error al ejecutar el formulario",
                "error": result.stderr,
                "capturas": capturas_binarias,
                "total_capturas": len(capturas_binarias),
                "timestamp": datetime.now().isoformat()
            }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

@app.post("/capturas")
async def obtener_capturas():
    """Devuelve información de las últimas 2 capturas tomadas con las imágenes en base64"""
    try:
        # Buscar archivos PNG en el directorio actual
        archivos_png = glob.glob("*.png")
        
        if not archivos_png:
            return {
                "mensaje": "No se encontraron capturas",
                "capturas": [],
                "total": 0
            }
        
        # Ordenar por fecha de modificación (más recientes primero)
        archivos_png.sort(key=lambda x: os.path.getmtime(x), reverse=True)
        
        # Tomar las 2 más recientes
        ultimas_capturas = archivos_png[:2]
        
        capturas_info = []
        for archivo in ultimas_capturas:
            stat = os.stat(archivo)
            
            # Leer la imagen y convertirla a base64
            with open(archivo, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
            capturas_info.append({
                "nombre": archivo,
                "tamaño_bytes": stat.st_size,
                "fecha_creacion": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                "es_inicio": "_inicio_" in archivo,
                "es_final": "_final_" in archivo,
                "binary": {
                    "data": image_data,
                    "mimeType": "image/png",
                    "fileName": archivo,
                    "fileExtension": "png"
                },
                "url_imagen": f"/imagen/{archivo}"
            })
        
        return {
            "mensaje": "Capturas encontradas",
            "capturas": capturas_info,
            "total": len(capturas_info),
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener capturas: {str(e)}")

@app.get("/imagen/{nombre_archivo}")
async def mostrar_imagen(nombre_archivo: str):
    """Devuelve una imagen como respuesta HTTP para mostrar directamente"""
    try:
        # Verificar que el archivo existe y es PNG
        if not nombre_archivo.endswith('.png'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PNG")
        
        ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
        
        if not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
        # Leer la imagen y devolverla como respuesta HTTP
        with open(ruta_archivo, "rb") as image_file:
            image_data = image_file.read()
        
        return Response(
            content=image_data,
            media_type="image/png",
            headers={"Content-Disposition": "inline"}  # inline para mostrar, no descargar
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar imagen: {str(e)}")

@app.get("/status")
async def obtener_status():
    """Devuelve el estado actual del sistema"""
    try:
        # Contar archivos PNG
        archivos_png = glob.glob("*.png")
        
        return {
            "status": "online",
            "total_capturas": len(archivos_png),
            "directorio_trabajo": os.getcwd(),
            "archivos_recientes": sorted(archivos_png, key=lambda x: os.path.getmtime(x), reverse=True)[:5],
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener status: {str(e)}")

@app.get("/binario/{nombre_archivo}")
async def obtener_binario_n8n(nombre_archivo: str):
    """Devuelve un campo binario específico para n8n"""
    try:
        # Verificar que el archivo existe y es PNG
        if not nombre_archivo.endswith('.png'):
            raise HTTPException(status_code=400, detail="Solo se permiten archivos PNG")
        
        ruta_archivo = os.path.join(os.getcwd(), nombre_archivo)
        
        if not os.path.exists(ruta_archivo):
            raise HTTPException(status_code=404, detail="Imagen no encontrada")
        
        # Leer la imagen y convertirla a base64
        with open(ruta_archivo, "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        return {
            "binary": {
                "data": image_data,
                "mimeType": "image/png",
                "fileName": nombre_archivo,
                "fileExtension": "png"
            },
            "json": {
                "nombre": nombre_archivo,
                "timestamp": datetime.now().isoformat()
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener binario: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("[INFO] Iniciando API de Selenium Form...")
    print("[INFO] Endpoints disponibles:")
    print("   - GET  /: Información general")
    print("   - POST /ejecutar: Ejecutar formulario selenium")
    print("   - GET  /capturas: Obtener últimas 2 capturas (con binary fields)")
    print("   - GET  /imagen/{nombre}: Mostrar imagen específica")
    print("   - GET  /binario/{nombre}: Obtener binary field para n8n")
    print("   - GET  /status: Estado del sistema")
    print("\n[INFO] La API estará disponible en: http://localhost:8000")
    print("[INFO] Documentación interactiva en: http://localhost:8000/docs")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
