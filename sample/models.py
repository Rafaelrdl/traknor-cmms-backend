from django.db import models


class SampleModel(models.Model):
    """Modelo simples usado apenas para testes de isolamento."""
    name = models.CharField(max_length=100)

    def __str__(self) -> str:  # pragma: no cover
        return self.name
