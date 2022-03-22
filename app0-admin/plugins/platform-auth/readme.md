# Platform-auth

Plugin de validación de usuario. Representa un plugin válido para autenticación de usario via JWT para la plataforma HOPEIT.PY

Posibles respuestas del api /internal/api/login

* Status 404: si el login no logra validar o si el request fue efectuado desde un host no permitido en la lista de hosts permitidos para el request.

```
{
    "msg": "access not allow for localhost"
}
```
* Status 200: si el usuario esta activo y es válido se devuelve un JSON con la siguietne signatura:

```
{
    "id": 9999,
    "username": "LastName, FirstName",
    "email": "username@domain.tld"
}
```