import os
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Assign movie images from media/movie/images/ directory to movies in database"

    def handle(self, *args, **kwargs):
        # 📁 Ruta base donde se encuentran las imágenes de las películas
        images_base_dir = 'media/movie/images/'
        
        # ✅ Verificar si el directorio existe
        if not os.path.exists(images_base_dir):
            self.stderr.write(f"Directory '{images_base_dir}' not found.")
            return

        updated_count = 0
        movie_images = {}

        # 📖 Primero, recopilamos todos los archivos de imagen disponibles
        for filename in os.listdir(images_base_dir):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                # Extraemos el título de la película del nombre del archivo
                # Asumimos que el nombre del archivo es como "Título de la Película.jpg"
                title = os.path.splitext(filename)[0].replace('_', ' ').strip()
                movie_images[title] = os.path.join('movie/images/', filename)

        # 🎬 Recorremos todas las películas en la base de datos
        for movie in Movie.objects.all():
            # Buscamos una imagen que coincida con el título de la película
            matching_image = None
            
            # 1. Busqueda exacta primero
            if movie.title in movie_images:
                matching_image = movie_images[movie.title]
            else:
                # 2. Si no encontramos exacto, buscamos aproximado (ignorando mayúsculas)
                for img_title, img_path in movie_images.items():
                    if img_title.lower() == movie.title.lower():
                        matching_image = img_path
                        break
            
            if matching_image:
                try:
                    # Actualizamos la imagen de la película
                    movie.image = matching_image
                    movie.save()
                    updated_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Updated image for: {movie.title}"))
                except Exception as e:
                    self.stderr.write(f"Failed to update {movie.title}: {str(e)}")
            else:
                self.stdout.write(f"No image found for: {movie.title}")

        # ✅ Resultado final
        self.stdout.write(self.style.SUCCESS(
            f"Finished updating images for {updated_count} out of {Movie.objects.count()} movies."
        ))