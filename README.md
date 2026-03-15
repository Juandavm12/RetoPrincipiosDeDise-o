# Motor de Reglas de Reembolsos Medicos

Motor de reglas de reembolsos medicos construido en Python que procesa solicitudes de reembolso a traves de reglas de negocio configurables y una maquina de estados bien definida. El proyecto esta disenado como una muestra arquitectonica de codigo limpio y principios de diseno de software.

---

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Vision General de la Arquitectura](#vision-general-de-la-arquitectura)
- [Modelo de Dominio](#modelo-de-dominio)
- [Principios de Diseno](#principios-de-diseno)
- [Maquina de Estados](#maquina-de-estados)
- [Reglas de Negocio](#reglas-de-negocio)
- [Politicas por Tipo](#politicas-por-tipo)

---

## Estructura del Proyecto

```
project/
|-- domain/                 # Entidades y objetos de valor
|   |-- solicitud.py        # SolicitudReembolso (raiz del agregado)
|   |-- paciente.py         # Entidad Paciente
|   |-- prestador.py        # Entidad Prestador
|   |-- documento.py        # Entidad DocumentoAdjunto
|   |-- hallazgo_regla.py   # Objeto de valor HallazgoRegla
|   |-- resultado_accion.py # Objeto de valor ResultadoAccion
|   |-- resultado_evaluacion.py # Objeto de valor ResultadoEvaluacion
|
|-- enums/                  # Tipos enumerados
|   |-- tipo_solicitud.py   # Tipos de solicitud (Medicamento, Urgencias, etc.)
|   |-- accion_solicitud.py # Acciones (Enviar, Aprobar, Rechazar, etc.)
|   |-- decision_evaluacion.py # Resultados de evaluacion (Aprobable, Rechazable)
|
|-- policies/               # Implementaciones de estrategia por tipo de solicitud
|   |-- politica_tipo_solicitud.py  # IPoliticaTipoSolicitud (interfaz)
|   |-- medicamento_policy.py       # Politica de medicamentos
|   |-- procedimiento_policy.py     # Politica de procedimientos ambulatorios
|   |-- urgencias_policy.py         # Politica de urgencias
|   |-- examen_policy.py            # Politica de examenes diagnosticos
|
|-- ports/                  # Puertos abstractos (arquitectura hexagonal)
|   |-- clock.py            # IClock
|   |-- prestador_catalog.py        # IPrestadorHabilitadoCatalog
|   |-- tipo_solicitud_provider.py  # ITipoSolicitudProvider
|
|-- rules/                  # Evaluadores de reglas de negocio
|   |-- regla_evaluacion.py          # ReglaEvaluacion (base abstracta)
|   |-- regla_consistencia_datos.py  # Validacion de consistencia de datos
|   |-- regla_documentacion.py       # Verificacion de documentacion minima
|   |-- regla_monto_maximo.py        # Control de monto maximo
|   |-- regla_prestador_habilitado.py # Verificacion de prestador habilitado
|   |-- regla_ventana_tiempo.py      # Validacion de ventana de 60 dias
|
|-- services/               # Servicios de capa de aplicacion
|   |-- motor_reglas_facade.py     # MotorReglasFacade (punto de entrada)
|   |-- evaluador_solicitudes.py   # Orquestador de evaluacion de reglas
|   |-- ejecutor_acciones.py       # Manejador de ejecucion de acciones
|
|-- states/                 # Patron de estado para el ciclo de vida
    |-- estado_solicitud.py   # IEstadoSolicitud (interfaz)
    |-- draft_state.py        # Borrador (estado inicial)
    |-- submitted_state.py    # Enviada
    |-- under_review_state.py # En revision
    |-- approved_state.py     # Aprobada (terminal)
    |-- rejected_state.py     # Rechazada (terminal)
```

---

## Vision General de la Arquitectura

El sistema sigue una arquitectura organizada en capas claramente separadas:

```
+----------------------------------------------+
|            Capa de Aplicacion                 |
|   MotorReglasFacade (punto de entrada)        |
|   EvaluadorSolicitudes | EjecutorAcciones     |
+----------------------------------------------+
        |               |               |
+-------v---+   +-------v---+   +-------v--------+
|  Reglas   |   |  Estados  |   |  Politicas     |
| (Logica   |   | (Control  |   | (Estrategias   |
|  negocio) |   |  de ciclo |   |  por tipo)     |
|           |   |  de vida) |   |                |
+-----------+   +-----------+   +----------------+
        |
+-------v-----------+
|   Puertos          |  Interfaces abstractas para
|   IClock           |  dependencias externas
|   IPrestador...    |
|   ITipoSolicitud.. |
+--------------------+
        |
+-------v-----------+
|   Dominio          |  Entidades y Objetos de Valor
|   SolicitudReembolso, Paciente,               |
|   Prestador, DocumentoAdjunto, ...            |
+--------------------+

    Enums (transversales): TipoSolicitud, AccionSolicitud, DecisionEvaluacion
```

**Decisiones arquitectonicas clave:**

- Las **entidades de dominio** contienen datos e identidad, pero ninguna preocupacion de infraestructura.
- Los **puertos** (`ports/`) definen contratos abstractos para dependencias externas (reloj, catalogos), permitiendo que el dominio permanezca agnostico a la infraestructura.
- Los **servicios** orquestan casos de uso componiendo reglas, estados y politicas mediante inyeccion de dependencias.
- Todas las dependencias fluyen **hacia adentro**, hacia el dominio -- las capas externas dependen de abstracciones internas, nunca al reves.

---

## Modelo de Dominio

| Clase | Tipo | Descripcion |
|-------|------|-------------|
| `SolicitudReembolso` | Raiz del Agregado | Entidad central que representa una solicitud de reembolso. Contiene referencias al paciente, prestador, documentos, estado actual y resultado de evaluacion. |
| `Paciente` | Entidad | El paciente que solicita el reembolso. |
| `Prestador` | Entidad | El prestador de servicios de salud. |
| `DocumentoAdjunto` | Entidad | Un documento adjunto (factura, orden medica, etc.). |
| `HallazgoRegla` | Objeto de Valor | Un hallazgo o problema detectado durante la evaluacion de reglas. |
| `ResultadoAccion` | Objeto de Valor | El resultado (exito/fallo) de ejecutar una accion. |
| `ResultadoEvaluacion` | Objeto de Valor | Resultado consolidado de todas las evaluaciones de reglas, que contiene una decision y una lista de hallazgos. |

---

## Principios de Diseno

### SOLID

| Principio | Como se Aplica |
|-----------|----------------|
| **Responsabilidad Unica (SRP)** | Cada clase tiene exactamente una razon para cambiar. Los objetos de dominio contienen datos, las reglas validan un solo aspecto cada una, los estados gestionan sus propias transiciones y los servicios orquestan. |
| **Abierto/Cerrado (OCP)** | Se pueden agregar nuevos tipos de solicitud, reglas, estados o politicas creando una nueva clase que implemente la interfaz correspondiente -- no se necesita modificar codigo existente. |
| **Sustitucion de Liskov (LSP)** | Todos los estados concretos son intercambiables a traves de `IEstadoSolicitud`; todas las reglas a traves de `ReglaEvaluacion`; todas las politicas a traves de `IPoliticaTipoSolicitud`. Sustituir cualquier implementacion preserva el comportamiento correcto. |
| **Segregacion de Interfaces (ISP)** | Las interfaces son minimas y enfocadas. `IClock` expone un unico metodo `today()`; `IPrestadorHabilitadoCatalog` expone un unico metodo `estaHabilitado()`. Ningun cliente se ve forzado a depender de metodos que no utiliza. |
| **Inversion de Dependencias (DIP)** | Los modulos de alto nivel (servicios, reglas) dependen de abstracciones definidas en `ports/` y clases base abstractas, no de implementaciones concretas. La direccion de dependencia siempre apunta hacia el dominio. |

### Principios Adicionales

| Principio | Como se Aplica |
|-----------|----------------|
| **DRY (No te Repitas)** | Los contratos comunes se definen una sola vez en interfaces abstractas y se reutilizan en todas las implementaciones. Los valores de enumeracion estan centralizados en el paquete `enums/`. |
| **KISS (Mantenlo Simple)** | Las clases son deliberadamente simples. Los objetos de valor contienen unicamente datos y un metodo de representacion. Las politicas retornan valores escalares directos sin logica innecesaria. |
| **YAGNI (No lo vas a Necesitar)** | No existe codigo especulativo. Los estados terminales (`ApprovedState`, `RejectedState`) tienen conjuntos de acciones vacios e implementaciones minimas -- nada mas alla de lo requerido. |

### GRASP

| Principio | Como se Aplica |
|-----------|----------------|
| **Alta Cohesion** | Cada modulo agrupa unicamente responsabilidades estrechamente relacionadas (ej. todas las clases de estado en `states/`, todas las reglas en `rules/`). |
| **Bajo Acoplamiento** | El dominio tiene cero dependencias de infraestructura. Las reglas dependen de puertos abstractos, no de servicios concretos. |
| **Creador** | Los objetos son creados por las clases que poseen la informacion necesaria para inicializarlos (ej. `UnderReviewState` crea `ApprovedState`/`RejectedState`). |
| **Polimorfismo** | Reglas, estados y politicas aprovechan el despacho polimorfico para eliminar logica condicional. |
| **Controlador** | `MotorReglasFacade` actua como el controlador coordinador de todos los casos de uso. |

---

## Maquina de Estados

La solicitud sigue un ciclo de vida bien definido:

```
  BORRADOR ──[ENVIAR]──> ENVIADA ──[INICIAR_REVISION]──> EN_REVISION
                                                              |
                                                    [EVALUAR]  (permanece en EN_REVISION)
                                                    [APROBAR] ──> APROBADA  (terminal)
                                                    [RECHAZAR] ──> RECHAZADA (terminal)
```

- **BORRADOR**: Estado inicial. La unica accion permitida es `ENVIAR`.
- **ENVIADA**: En espera de asignacion de revision. La unica accion permitida es `INICIAR_REVISION`.
- **EN_REVISION**: Fase activa de evaluacion. Soporta `EVALUAR`, `APROBAR` y `RECHAZAR`.
  - `APROBAR` requiere que la decision de evaluacion sea `APROBABLE`.
  - `RECHAZAR` requiere que la decision de evaluacion sea `RECHAZABLE`.
- **APROBADA / RECHAZADA**: Estados terminales sin acciones adicionales permitidas.

---

## Reglas de Negocio

El `EvaluadorSolicitudes` ejecuta todas las reglas registradas contra una solicitud. Si alguna regla produce un hallazgo (`HallazgoRegla`), la decision es `RECHAZABLE`; de lo contrario es `APROBABLE`.

| Regla | Validacion | Dependencia Externa |
|-------|-----------|---------------------|
| `ReglaConsistenciaDatos` | Verifica que existan paciente, prestador, tipo y monto > 0 | Ninguna |
| `ReglaDocumentacionMinima` | Verifica que todos los documentos requeridos por la politica del tipo esten adjuntos | `ITipoSolicitudProvider` |
| `ReglaMontoMaximo` | Verifica que el monto solicitado no exceda el maximo de la politica del tipo | `ITipoSolicitudProvider` |
| `ReglaPrestadorHabilitado` | Verifica que el prestador de salud este activo/habilitado | `IPrestadorHabilitadoCatalog` |
| `ReglaVentanaTiempo` | Verifica que la fecha del evento este dentro de los 60 dias desde hoy | `IClock` |

Agregar una nueva regla solo requiere crear una clase que extienda `ReglaEvaluacion` e inyectarla en el evaluador -- no es necesario modificar reglas ni servicios existentes.

---

## Politicas por Tipo

Cada tipo de solicitud define sus propios documentos requeridos y monto maximo reembolsable:

| Tipo | Documentos Requeridos | Monto Maximo |
|------|-----------------------|--------------|
| Medicamento | FORMULA_MEDICA, FACTURA | $800.000 |
| Procedimiento Ambulatorio | ORDEN_MEDICA, FACTURA | $2.500.000 |
| Urgencias | HISTORIA_CLINICA_URGENCIAS, FACTURA | $3.500.000 |
| Examen Diagnostico | ORDEN_MEDICA, RESULTADO_EXAMEN, FACTURA | $1.200.000 |

Agregar un nuevo tipo de solicitud requiere crear una nueva clase de politica que implemente `IPoliticaTipoSolicitud` y registrarla en el `ITipoSolicitudProvider` -- cumpliendo completamente con el Principio Abierto/Cerrado.
