# 🔐 BLUMCL — Principios de Seguridad

## Objetivo

Blumcl debe priorizar la seguridad y la transparencia.

## Reglas

1. El análisis debe ser independiente de la limpieza.
2. Las operaciones destructivas requieren confirmación.
3. No deben almacenarse contraseñas.
4. No deben almacenarse claves privadas.
5. Los informes pueden contener información privada.
6. Los informes personales no deben publicarse automáticamente.
7. Los archivos críticos deben protegerse.
8. Las acciones deben poder explicarse al usuario.
9. Los errores deben registrarse.
10. Los cambios importantes deben documentarse.

## Modelo

```text
OBSERVAR
   ↓
EVALUAR
   ↓
EXPLICAR
   ↓
CONFIRMAR
   ↓
ACTUAR
```

## Principio de mínima intervención

Blumcl debe realizar la menor modificación necesaria
para cumplir la acción aprobada.
