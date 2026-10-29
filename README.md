# Taller: peticiones HTTP en Django

**Autor:** Kenneth García  
**Repositorio:** [github.com/kairoblix/tarea-](https://github.com/kairoblix/tarea-)

## Propósito

Este proyecto independiente implementa un endpoint JSON para administrar
productos con Django nativo. No depende de otro proyecto ni instala Django REST
Framework o bibliotecas externas.

## Métodos HTTP y CRUD

| Método | Ruta | Operación CRUD | Resultado |
| --- | --- | --- | --- |
| `GET` | `/api/productos/` | Read | Lista JSON de productos (`200`). |
| `GET` | `/api/productos/{id}/` | Read | Un producto (`200`) o `404`. |
| `POST` | `/api/productos/` | Create | Crea el producto (`201`). |
| `PUT` | `/api/productos/{id}/` | Update | Reemplaza todos los campos (`200`) o `404`. |
| `DELETE` | `/api/productos/{id}/` | Delete | Elimina el producto (`204`) o devuelve `404`. |

El modelo `Producto` contiene `nombre`, `descripcion`, `precio` y `stock`. `PUT`
reemplaza los cuatro campos; las modificaciones parciales normalmente usan
`PATCH`, que no hace parte de este taller.

### Ejemplo de JSON

```json
{
  "nombre": "Cuaderno",
  "descripcion": "Cuaderno de 100 hojas",
  "precio": "12500.00",
  "stock": 12
}
```

Las peticiones con JSON inválido, campos faltantes o valores que no superan la
validación del modelo reciben `400 Bad Request`. Un método no permitido recibe
`405 Method Not Allowed`.

## Componentes de Django utilizados

- `django.views.View`: clase base; `dispatch()` deriva cada petición al método
  `get()`, `post()`, `put()` o `delete()` correspondiente.
- `django.urls.path` y `include`: registran rutas de la aplicación y las conectan
  al URLconf del proyecto. `ProductoEndpoint.as_view()` adapta la clase para la
  resolución de URLs.
- `django.http.JsonResponse`: serializa datos JSON y asigna el tipo de contenido
  apropiado. `HttpResponse` responde `204` sin cuerpo y `HttpResponseNotAllowed`
  responde `405`.
- `django.shortcuts.get_object_or_404`: busca por identificador y genera un `404`
  cuando el producto no existe.
- `django.core.exceptions.ValidationError`: comunica errores de validación del
  modelo. `full_clean()` verifica cada instancia antes de guardarla.
- `django.utils.decorators.method_decorator` y
  `django.views.decorators.csrf.csrf_protect`: aplican protección CSRF al despacho
  de la vista basada en clase.
- `json.loads`: biblioteca estándar de Python para decodificar el cuerpo JSON.
- `Producto.objects.all()`, `save()` y `delete()`: operaciones del ORM de Django
  para consultar, crear, actualizar y borrar registros.

## Ejecución local

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

La base SQLite se crea localmente al ejecutar las migraciones y está excluida del
control de versiones. El endpoint queda disponible en `http://127.0.0.1:8000/api/productos/`.
Las operaciones `POST`, `PUT` y `DELETE` exigen un token CSRF. No se desactivó
esta protección; la aplicación de demostración tampoco implementa autenticación
ni autorización de usuarios, así que debe configurarse antes de exponer datos
reales.

## Fuentes oficiales

- [Vistas basadas en clases](https://docs.djangoproject.com/en/6.1/topics/class-based-views/)
- [Objetos de petición y respuesta](https://docs.djangoproject.com/en/6.1/ref/request-response/)
- [Atajos de Django](https://docs.djangoproject.com/en/6.1/topics/http/shortcuts/)
- [Protección CSRF](https://docs.djangoproject.com/en/6.1/howto/csrf/)
- [Seguridad en Django](https://docs.djangoproject.com/en/6.1/topics/security/)
