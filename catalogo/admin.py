from django.contrib import admin
from .models import Categoria, Juego, Pedido

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio_clp', 'stock', 'disponible')
    list_filter = ('categoria', 'disponible')
    search_fields = ('nombre',)

    @admin.display(description='Precio')
    def precio_clp(self, obj):
        return f"${obj.precio:,}".replace(",", ".")

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'juego', 'nombre_cliente', 'cantidad', 'fecha_hora')
    list_filter = ('juego',)
    search_fields = ('nombre_cliente', 'correo')