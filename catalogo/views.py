from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import Juego, Categoria, Pedido
from .forms import PedidoForm

def inicio(request):
    juegos = Juego.objects.filter(disponible=True)
    categorias = Categoria.objects.all()
    query = request.GET.get('q', '')
    cat_id = request.GET.get('categoria', '')

    if query:
        juegos = juegos.filter(nombre__icontains=query)
    if cat_id:
        juegos = juegos.filter(categoria_id=cat_id)

    return render(request, 'catalogo/inicio.html', {
        'juegos': juegos,
        'categorias': categorias,
        'query': query,
        'cat_seleccionada': cat_id,
    })

def detalle_juego(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id, disponible=True)

    if request.method == 'POST' and juego.stock > 0:
        form = PedidoForm(request.POST, juego=juego)
        if form.is_valid():
            with transaction.atomic():
                pedido = form.save(commit=False)
                pedido.juego = juego
                pedido.save()
                juego.stock -= pedido.cantidad
                juego.save()
            return redirect('comprobante', codigo=pedido.codigo)
    else:
        form = PedidoForm(juego=juego)

    return render(request, 'catalogo/detalle.html', {'juego': juego, 'form': form})

def comprobante(request, codigo):
    pedido = get_object_or_404(Pedido, codigo=codigo)
    return render(request, 'catalogo/comprobante.html', {'pedido': pedido})