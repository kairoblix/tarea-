import json

from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect

from .models import Producto


def _producto_a_json(producto):
    return {
        "id": producto.pk,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": str(producto.precio),
        "stock": producto.stock,
    }


def _leer_datos(request):
    try:
        datos = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None, JsonResponse(
            {"error": "El cuerpo debe ser un objeto JSON válido."}, status=400
        )

    if not isinstance(datos, dict):
        return None, JsonResponse(
            {"error": "El cuerpo JSON debe ser un objeto."}, status=400
        )

    campos = ("nombre", "descripcion", "precio", "stock")
    faltantes = [campo for campo in campos if campo not in datos]
    if faltantes:
        return None, JsonResponse(
            {"error": "Faltan campos obligatorios.", "campos": faltantes},
            status=400,
        )

    return {campo: datos[campo] for campo in campos}, None


def _errores_validacion(exc):
    if hasattr(exc, "message_dict"):
        return exc.message_dict
    return {"error": exc.messages}


@method_decorator(csrf_protect, name="dispatch")
class ProductoEndpoint(View):
    """CRUD JSON mínimo de productos mediante los verbos HTTP solicitados."""

    http_method_names = ["get", "post", "put", "delete", "options"]

    def get(self, request, pk=None):
        if pk is None:
            productos = Producto.objects.all()
            return JsonResponse(
                [_producto_a_json(producto) for producto in productos],
                safe=False,
            )

        producto = get_object_or_404(Producto, pk=pk)
        return JsonResponse(_producto_a_json(producto))

    def post(self, request, pk=None):
        if pk is not None:
            return HttpResponseNotAllowed(["GET", "PUT", "DELETE"])

        datos, error = _leer_datos(request)
        if error:
            return error

        producto = Producto(**datos)
        try:
            producto.full_clean()
        except ValidationError as exc:
            return JsonResponse(_errores_validacion(exc), status=400)

        producto.save()
        return JsonResponse(_producto_a_json(producto), status=201)

    def put(self, request, pk=None):
        if pk is None:
            return HttpResponseNotAllowed(["GET", "POST"])

        producto = get_object_or_404(Producto, pk=pk)
        datos, error = _leer_datos(request)
        if error:
            return error

        for campo, valor in datos.items():
            setattr(producto, campo, valor)

        try:
            producto.full_clean()
        except ValidationError as exc:
            return JsonResponse(_errores_validacion(exc), status=400)

        producto.save()
        return JsonResponse(_producto_a_json(producto))

    def delete(self, request, pk=None):
        if pk is None:
            return HttpResponseNotAllowed(["GET", "POST"])

        producto = get_object_or_404(Producto, pk=pk)
        producto.delete()
        return HttpResponse(status=204)
