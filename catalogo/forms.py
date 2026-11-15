from django import forms
from .models import Pedido

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['nombre_cliente', 'correo', 'telefono', 'cantidad']
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.juego = kwargs.pop('juego', None)
        super().__init__(*args, **kwargs)

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        if cantidad is None or cantidad < 1 or cantidad > 5:
            raise forms.ValidationError("La cantidad debe estar entre 1 y 5 unidades.")
        if self.juego and cantidad > self.juego.stock:
            raise forms.ValidationError(f"Stock insuficiente. Solo quedan {self.juego.stock} unidades disponibles.")
        return cantidad