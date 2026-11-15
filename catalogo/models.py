import uuid
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre

class Juego(models.Model):
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='juegos')
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='juegos/')
    precio = models.PositiveIntegerField()
    cantidad_jugadores = models.CharField(max_length=50, help_text="Ej: 2 a 4 jugadores")
    edad_minima = models.PositiveIntegerField()
    stock = models.PositiveIntegerField(default=0)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} (${self.precio:,})".replace(",", ".")

class Pedido(models.Model):
    codigo = models.CharField(max_length=12, unique=True, editable=False)
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE, related_name='pedidos')
    nombre_cliente = models.CharField(max_length=150)
    correo = models.EmailField()
    telefono = models.CharField(max_length=20)
    cantidad = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    fecha_hora = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = uuid.uuid4().hex[:8].upper()
        super().save(*args, **kwargs)

    @property
    def total(self):
        return self.juego.precio * self.cantidad

    def __str__(self):
        return f"Pedido {self.codigo} - {self.nombre_cliente}"