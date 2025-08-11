"""Registro simples dos modelos no admin do Django."""

from django.contrib import admin

from .models import Asset, Company, Sector, Subsection

# Comentários em PT-BR explicando o propósito de cada registro
admin.site.register(Company)
admin.site.register(Sector)
admin.site.register(Subsection)
admin.site.register(Asset)
