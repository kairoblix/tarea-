from django.urls import path

from .views import ProductoEndpoint


app_name = "peticiones"

urlpatterns = [
    path("productos/", ProductoEndpoint.as_view(), name="producto-lista"),
    path("productos/<int:pk>/", ProductoEndpoint.as_view(), name="producto-detalle"),
]
