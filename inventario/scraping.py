import requests
from .models import Producto

URL_OKWU = "https://okwu.cl/collections/labiales/products.json"

def scrapear_productos():
    try:
        response = requests.get(URL_OKWU, timeout=10)
        response.raise_for_status()
        data = response.json()

        if "products" not in data:
            raise ValueError("Estructura inesperada del JSON")

        Producto.objects.all().delete()

        for p in data["products"]:
            variantes = p.get("variants", [])
            imagenes = p.get("images", [])

            precio = variantes[0]["price"] if variantes else 0
            precio_comparacion = variantes[0].get("compare_at_price")
            disponible = variantes[0].get("available", False) if variantes else False
            nombres_variantes = ", ".join(v["title"] for v in variantes)
            imagen = imagenes[0]["src"] if imagenes else ""

            Producto.objects.create(
                nombre=p["title"],
                precio_regular=precio,
                precio_oferta=precio_comparacion,
                variantes=nombres_variantes,
                url_imagen=imagen,
                disponible=disponible,
            )

        return Producto.objects.all()

    except requests.exceptions.ConnectionError:
        print("Error: no se pudo conectar a okwu.cl")
        return Producto.objects.all()
    except Exception as e:
        print(f"Error en scraping: {e}")
        return Producto.objects.all()