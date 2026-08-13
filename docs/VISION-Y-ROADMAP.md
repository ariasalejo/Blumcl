Blumcl — Visión, Filosofía y Evolución del Proyecto

«Observar · Analizar · Confirmar · Actuar»

1. Propósito

Blumcl es una herramienta local orientada a la observación, análisis y gestión controlada del almacenamiento de un dispositivo, especialmente en entornos como Termux sobre Android.

El proyecto nace de una necesidad práctica: comprender qué está ocupando espacio, identificar cambios, conservar evidencia, analizar posibles problemas y permitir acciones controladas sin entregar el control del sistema a una automatización ciega.

Blumcl busca evolucionar desde una herramienta personal hacia un proyecto abierto que otras personas puedan clonar, estudiar, mejorar y utilizar.

---

2. Filosofía fundamental

Blumcl se construye alrededor de seis principios:

1. Observar antes de actuar.
2. Analizar antes de recomendar.
3. Explicar antes de ejecutar.
4. Confirmar antes de modificar.
5. Registrar después de actuar.
6. Mantener al humano en control.

La filosofía puede resumirse así:

«La IA recomienda. El código protege. El humano decide.»

---

3. IA local y control humano

La inteligencia artificial de Blumcl tiene una función de análisis y asistencia.

La IA puede:

- interpretar información;
- resumir hallazgos;
- explicar posibles causas;
- identificar patrones;
- proponer recomendaciones;
- analizar snapshots;
- responder preguntas sobre los informes.

La IA no debe tener autoridad directa para modificar archivos.

Una recomendación de la IA nunca equivale a una autorización.

La arquitectura prevista es:

Usuario
   ↓
Blumcl
   ↓
Scanner
   ↓
Evidencia
   ↓
Análisis
   ↓
IA local (opcional)
   ↓
Recomendación
   ↓
Confirmación humana
   ↓
Acción controlada
   ↓
Registro

---

4. Principio de seguridad

Blumcl no debe depender únicamente de instrucciones contenidas en un prompt para impedir acciones peligrosas.

La seguridad debe existir también en el código.

Incluso si una IA generase una respuesta como:

BORRAR /ruta/archivo

Blumcl debe interpretarla solamente como texto.

La IA no debe disponer de una vía directa para ejecutar operaciones de archivos.

Las operaciones reales deben estar controladas por módulos específicos y protegidos.

---

5. Sistema de evidencia

Un hallazgo no debe ser simplemente:

archivo grande

Debe convertirse en una unidad de evidencia.

Ejemplo:

HALLAZGO #0042

Ruta:
~/ejemplo/archivo.zip

Tamaño:
1.40 GB

Tipo:
ZIP

Detectado:
2026-08-12

Estado:
🟡 REVISAR

Motivos:
• Archivo grande
• Posible duplicado
• Existe otro archivo similar

Confianza:
87%

Acción:
NINGUNA

Esto permite que Blumcl explique por qué un elemento fue identificado y evita decisiones basadas únicamente en el tamaño del archivo.

---

6. Clasificación de elementos

Blumcl podrá clasificar los hallazgos utilizando categorías comprensibles:

🟢 PROTEGIDO
🔵 IMPORTANTE
🟡 REVISAR
🟠 POSIBLE DUPLICADO
🔴 CANDIDATO A CUARENTENA

Estas categorías representan niveles de análisis, no órdenes automáticas de eliminación.

---

7. Detección inteligente de duplicados

El sistema podrá utilizar diferentes evidencias:

- nombre;
- tamaño;
- extensión;
- hash;
- contenido;
- ubicación;
- similitud de nombres;
- relación entre archivos.

Cuando dos archivos tengan exactamente el mismo contenido, Blumcl podrá mostrar evidencia criptográfica mediante hashes.

Ejemplo:

♻️ POSIBLE DUPLICADO

Archivo A:
FIFA...zip
1.408 GB

Archivo B:
FIFA...zip
1.408 GB

SHA-256:
idéntico

Resultado:
100% de coincidencia

Recomendación:
Conservar uno y revisar el otro.

Acción:
NINGUNA

---

8. Máquina del tiempo del almacenamiento

Los snapshots representan fotografías cronológicas del sistema.

Blumcl podrá comparar diferentes momentos:

11 AGO
107.2 GB usados

        ↓

12 AGO
107.8 GB usados

CAMBIO:
+600 MB

El sistema podrá identificar:

- archivos nuevos;
- archivos desaparecidos;
- archivos modificados;
- archivos que aumentaron considerablemente;
- posibles duplicados;
- elementos enviados a cuarentena.

El objetivo es responder preguntas como:

«¿Qué cambió en mi almacenamiento?»

«¿Qué empezó a ocupar espacio recientemente?»

«¿Qué archivos crecieron?»

---

9. Sistema de cuarentena

Blumcl debe preferir una cuarentena recuperable frente a la eliminación inmediata.

La cuarentena permite mover un elemento a una ubicación controlada antes de eliminarlo definitivamente.

Cada operación podrá registrar:

ID
Ruta original
Ruta de cuarentena
Fecha
Tamaño
Hash
Motivo
Snapshot asociado
Resultado

Esto permitirá recuperar archivos y reconstruir qué ocurrió.

---

10. Zonas protegidas

Blumcl debe proteger automáticamente componentes críticos.

Ejemplos:

~/.ssh
~/.gnupg
~/.termux
~/Blumcl
~/Ciberseguridad
~/blumcl_papelera

También deberán protegerse determinados tipos de archivos sensibles, como claves y credenciales.

El objetivo es impedir que una limpieza accidental pueda afectar componentes críticos del usuario o del propio sistema.

---

11. Autodiagnóstico

El módulo de autodiagnóstico deberá comprobar el estado de Blumcl.

Entre otros elementos:

✓ Python
✓ Scanner
✓ Cleaner
✓ Snapshots
✓ Reports
✓ Configuración
✓ Permisos
✓ Espacio disponible
✓ IA local
✓ Modelo
✓ Dependencias

El resultado debe distinguir entre:

- información;
- advertencias;
- errores;
- problemas críticos.

---

12. Dashboard e informes

Blumcl deberá producir informes HTML completamente utilizables de forma local.

El dashboard podrá incluir:

- almacenamiento utilizado;
- evolución temporal;
- archivos grandes;
- duplicados;
- hallazgos;
- estado de la IA;
- salud del sistema;
- cuarentena;
- recomendaciones;
- historial de operaciones.

La información deberá ser comprensible incluso para una persona que no conozca el código.

---

13. Auditoría

Las operaciones importantes deberán generar registros.

Ejemplo:

2026-08-12 10:36

USUARIO CONFIRMÓ

Operación:
QUARANTINE

Origen:
~/.cache

Destino:
~/blumcl_papelera/...

Resultado:
SUCCESS

La auditoría permite comprender qué ocurrió y cuándo.

---

14. Privacidad

Blumcl debe mantener una filosofía local y orientada a la privacidad.

La IA local permite analizar información sin necesidad de enviar las consultas del usuario a un servicio remoto.

Cuando una funcionalidad no necesite Internet, deberá poder funcionar sin conexión.

La privacidad no debe depender solamente de una promesa en el README: debe reflejarse en la arquitectura.

---

15. Documentación como parte del software

La documentación no será un elemento secundario.

Debe evolucionar junto con el código.

La estructura prevista incluye:

docs/
├── architecture.md
├── installation.md
├── configuration.md
├── scanner.md
├── snapshots.md
├── quarantine.md
├── local-ai.md
├── security-model.md
├── troubleshooting.md
└── development.md

También se mantendrán documentos principales:

README.md
CHANGELOG.md
CONTRIBUTING.md
SECURITY.md
CODE_OF_CONDUCT.md
ROADMAP.md
LICENSE

---

16. Evolución prevista

v0.5.1 — Base funcional

Estado actual del proyecto.

Incluye:

- scanner;
- snapshots;
- informes;
- comparación;
- historial;
- IA local;
- cuarentena;
- configuración;
- zonas protegidas.

v0.5.2 — Blumcl Seguro

Prioridad:

- robustez de IA;
- manejo de timeouts;
- validación de rutas;
- protección del modelo;
- separación estricta entre IA y acciones;
- mejora de cuarentena;
- corrección de navegación;
- pruebas de seguridad.

v0.6.0 — Evidencia

- sistema avanzado de hallazgos;
- clasificación;
- hashes;
- detección de duplicados;
- explicación de resultados.

v0.7.0 — Máquina del Tiempo

- evolución del almacenamiento;
- comparación avanzada;
- crecimiento de archivos;
- historial visual;
- análisis temporal.

v0.8.0 — Dashboard avanzado

- informes HTML mejorados;
- gráficos;
- indicadores;
- salud del sistema;
- análisis histórico.

v0.9.0 — Auditoría y endurecimiento

- registros;
- pruebas;
- validaciones;
- revisión de seguridad;
- documentación completa.

v1.0.0 — Blumcl público

Objetivo:

«Un proyecto local, documentado, reproducible, seguro y comprensible que cualquier persona pueda clonar, instalar, estudiar y mejorar.»

---

17. Visión final

Blumcl no pretende ser solamente un limpiador.

Pretende convertirse en una herramienta de comprensión del sistema.

Su objetivo es ayudar al usuario a responder:

«¿Qué tengo?»

«¿Qué cambió?»

«¿Qué ocupa espacio?»

«¿Qué parece importante?»

«¿Qué podría ser un duplicado?»

«¿Qué está protegido?»

«¿Qué recomienda la IA?»

«¿Qué evidencia respalda esa recomendación?»

«¿Qué acción quiero realizar?»

Y finalmente:

«¿Quiero confirmarla?»

La decisión final pertenece al usuario.

---

18. Principio de Blumcl

«Observar antes de actuar.

Analizar antes de recomendar.

Explicar antes de ejecutar.

Confirmar antes de modificar.

Registrar después de actuar.

La IA recomienda. El código protege. El humano decide.»

🐘 BLUMCL

Observar · Analizar · Confirmar · Actuar
