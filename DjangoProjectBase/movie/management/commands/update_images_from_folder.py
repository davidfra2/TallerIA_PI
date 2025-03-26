import os
import requests
from openai import OpenAI
from django.core.management.base import BaseCommand
from movie.models import Movie
from dotenv import load_dotenv

class Command(BaseCommand):
    help = "Import images from a folder and update movie image field"

    def handle(self, *args, **kwargs):
        # ✅ Cargar variables de entorno
        load_dotenv('../openAI.env')

        # ✅ Obtener API key de OpenAI
        api_key = os.getenv('openai_apikey')
        if not api_key:
            self.stderr.write("Error: 'openai_apikey' no está definido en openAI.env")
            return

        # ✅ Inicializar cliente de OpenAI
        client = OpenAI(api_key=api_key)

        # ✅ Carpeta donde están almacenadas las imágenes
        images_folder = 'media/movie/images/'
        os.makedirs(images_folder, exist_ok=True)

        # ✅ Obtener todas las películas de la base de datos
        movies = Movie.objects.all()
        self.stdout.write(f"Se encontraron {movies.count()} películas.")

        for movie in movies:
            try:
                # ✅ Buscar imagen en la carpeta
                image_filename = f"m_{movie.title}.png"
                image_path_full = os.path.join(images_folder, image_filename)
                
                if os.path.exists(image_path_full):
                    # ✅ Si la imagen existe, actualizar la base de datos
                    movie.image = os.path.join('movie/images', image_filename)
                    movie.save()
                    self.stdout.write(self.style.SUCCESS(f"Imagen importada y actualizada para: {movie.title}"))
                else:
                    self.stderr.write(f"No se encontró imagen para {movie.title}")
            except Exception as e:
                self.stderr.write(f"Error al actualizar {movie.title}: {e}")

        self.stdout.write(self.style.SUCCESS("Proceso completado."))