from flask import Flask, render_template
import pandas as pd
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

catalogos = {
    "alarmas": "ALARMAS.xlsx",
    "control_acceso": "CONTROL DE ACCESO.xlsx",
    "deteccion_incendios": "DETECCION DE INCENDIO.xlsx",
    "energia": "ENERGIA.xlsx",
    "redes": "REDES.xlsx",
    "telemetria": "TELEMETRIA.xlsx",
    "videovigilancia": "VIDEOVIGILANCIA.xlsx"
}

imagenes = {
    "alarmas": "Alarmas",
    "control_acceso": "Control de Acceso",
    "deteccion_incendios": "Deteccion de Incendio",
    "energia": "Energia",
    "redes": "Redes",
    "telemetria": "Telemetria",
    "videovigilancia": "Videovigilancia"
}

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/catalogo/<tipo>")
def catalogo(tipo):

    archivo = catalogos.get(tipo)
    carpeta_img = imagenes.get(tipo)

    ruta_excel = os.path.join(BASE_DIR, "catalogos", archivo)

    df = pd.read_excel(ruta_excel)

    # 🔥 LIMPIEZA DE COLUMNAS
    df.columns = df.columns.str.strip().str.lower()

    productos = df.to_dict(orient="records")

    for p in productos:

        # 🔥 MAPEO DE PRECIOS (AQUI ESTA LA CLAVE)
        p["precio"] = p.get("costo unitario", 0)
        p["final"] = p.get("costo neto", 0)
        p["stock"] = int(p.get("stock", 0))
        p["marca"] = p.get("marca", "")
        p["estado"] = p.get("estado", "")

        modelo = str(p.get("modelo","")).strip()

        carpeta = os.path.join(BASE_DIR,"static","img",carpeta_img)

        for f in os.listdir(carpeta):
            if f.split(".")[0].lower() == modelo.lower():
                p["imagen"] = f"/static/img/{carpeta_img}/{f}"
                break

    return render_template("catalogo.html", productos=productos, titulo=tipo.upper())

if __name__ == "__main__":
    app.run(debug=True)