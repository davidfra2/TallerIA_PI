import numpy as np
from django.core.management.base import BaseCommand
from movie.models import Movie

class Command(BaseCommand):
    help = "Validate stored embeddings for all movies"

    def handle(self, *args, **kwargs):
        movies = Movie.objects.all()
        if not movies.exists():
            self.stderr.write(self.style.ERROR("No movies found in the database."))
            return

        self.stdout.write(self.style.SUCCESS(f"Validating embeddings for {movies.count()} movies..."))

        for movie in movies:
            if movie.emb:
                embedding_vector = np.frombuffer(movie.emb, dtype=np.float32)
                self.stdout.write(f"🎬 {movie.title}: {embedding_vector[:5]}")  # Muestra los primeros 5 valores
            else:
                self.stderr.write(self.style.WARNING(f"⚠️ No embedding stored for {movie.title}"))

        self.stdout.write(self.style.SUCCESS("✅ Embedding validation completed."))
