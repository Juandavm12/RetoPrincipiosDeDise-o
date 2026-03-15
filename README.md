# Motor de Reglas de Reembolsos Medicos

A domain-driven **Medical Reimbursement Rules Engine** built in Python that processes reimbursement requests (_solicitudes de reembolso_) through configurable business rules and a well-defined state machine. The project is designed as an architectural showcase of clean code, design patterns, and software design principles.

---

## Table of Contents

- [Project Structure](#project-structure)
- [Architecture Overview](#architecture-overview)
- [Domain Model](#domain-model)
- [Design Patterns](#design-patterns)
- [Design Principles](#design-principles)
- [State Machine](#state-machine)
- [Business Rules](#business-rules)
- [Type Policies](#type-policies)

---

## Project Structure

```
project/
|-- domain/                 # Entities and value objects
|   |-- solicitud.py        # SolicitudReembolso (aggregate root)
|   |-- paciente.py         # Paciente entity
|   |-- prestador.py        # Prestador entity
|   |-- documento.py        # DocumentoAdjunto entity
|   |-- hallazgo_regla.py   # HallazgoRegla value object
|   |-- resultado_accion.py # ResultadoAccion value object
|   |-- resultado_evaluacion.py # ResultadoEvaluacion value object
|
|-- enums/                  # Enumeration types
|   |-- tipo_solicitud.py   # Request types (Medicamento, Urgencias, etc.)
|   |-- accion_solicitud.py # Actions (Submit, Approve, Reject, etc.)
|   |-- decision_evaluacion.py # Evaluation outcomes (Aprobable, Rechazable)
|
|-- policies/               # Strategy implementations per request type
|   |-- politica_tipo_solicitud.py  # IPoliticaTipoSolicitud (interface)
|   |-- medicamento_policy.py       # Medication policy
|   |-- procedimiento_policy.py     # Outpatient procedure policy
|   |-- urgencias_policy.py         # Emergency policy
|   |-- examen_policy.py            # Diagnostic exam policy
|
|-- ports/                  # Abstract ports (hexagonal architecture)
|   |-- clock.py            # IClock
|   |-- prestador_catalog.py        # IPrestadorHabilitadoCatalog
|   |-- tipo_solicitud_provider.py  # ITipoSolicitudProvider
|
|-- rules/                  # Business rule evaluators
|   |-- regla_evaluacion.py          # ReglaEvaluacion (abstract base)
|   |-- regla_consistencia_datos.py  # Data consistency validation
|   |-- regla_documentacion.py       # Minimum documentation check
|   |-- regla_monto_maximo.py        # Maximum amount enforcement
|   |-- regla_prestador_habilitado.py # Provider enablement check
|   |-- regla_ventana_tiempo.py      # 60-day time window validation
|
|-- services/               # Application-layer services
|   |-- motor_reglas_facade.py     # MotorReglasFacade (entry point)
|   |-- evaluador_solicitudes.py   # Rule evaluation orchestrator
|   |-- ejecutor_acciones.py       # Action execution handler
|
|-- states/                 # State pattern for request lifecycle
    |-- estado_solicitud.py   # IEstadoSolicitud (interface)
    |-- draft_state.py        # Draft (initial state)
    |-- submitted_state.py    # Submitted
    |-- under_review_state.py # Under Review
    |-- approved_state.py     # Approved (terminal)
    |-- rejected_state.py     # Rejected (terminal)
```

---

## Architecture Overview

The system follows a **Hexagonal Architecture (Ports & Adapters)** organized in clearly separated layers:

```
+----------------------------------------------+
|              Application Layer                |
|   MotorReglasFacade (Facade entry point)      |
|   EvaluadorSolicitudes | EjecutorAcciones     |
+----------------------------------------------+
        |               |               |
+-------v---+   +-------v---+   +-------v--------+
|   Rules   |   |   States  |   |   Policies     |
| (Business |   | (Lifecycle|   | (Type-specific  |
|  logic)   |   |  control) |   |  strategies)    |
+-----------+   +-----------+   +----------------+
        |
+-------v-----------+
|   Ports            |  Abstract interfaces for
|   IClock           |  external dependencies
|   IPrestador...    |
|   ITipoSolicitud.. |
+--------------------+
        |
+-------v-----------+
|   Domain           |  Entities & Value Objects
|   SolicitudReembolso, Paciente,               |
|   Prestador, DocumentoAdjunto, ...            |
+--------------------+

    Enums (cross-cutting): TipoSolicitud, AccionSolicitud, DecisionEvaluacion
```

**Key architectural decisions:**

- **Domain entities** hold data and identity but no infrastructure concerns.
- **Ports** (`ports/`) define abstract contracts for external dependencies (clock, catalogs), allowing the domain to remain infrastructure-agnostic.
- **Services** orchestrate use cases by composing rules, states, and policies through dependency injection.
- All dependencies flow **inward** toward the domain -- outer layers depend on inner abstractions, never the reverse.

---

## Domain Model

| Class | Type | Description |
|-------|------|-------------|
| `SolicitudReembolso` | Aggregate Root | Central entity representing a reimbursement request. Holds references to patient, provider, documents, current state, and evaluation result. |
| `Paciente` | Entity | The patient requesting the reimbursement. |
| `Prestador` | Entity | The healthcare provider. |
| `DocumentoAdjunto` | Entity | An attached document (invoice, medical order, etc.). |
| `HallazgoRegla` | Value Object | A finding/issue detected during rule evaluation. |
| `ResultadoAccion` | Value Object | The outcome (success/failure) of executing an action. |
| `ResultadoEvaluacion` | Value Object | Consolidated result of all rule evaluations, carrying a decision and a list of findings. |

---

## Design Patterns

### State Pattern (`states/`)

The request lifecycle is modeled as a finite state machine. Each state is a class implementing `IEstadoSolicitud`, which controls:
- Which actions are permitted in that state.
- The transition logic to the next state.

`SolicitudReembolso` delegates behavior to its current `estadoActual`, and states return the next state object on transition -- the request never manages its own transitions directly.

### Strategy Pattern (`policies/`)

Each request type (medication, emergency, outpatient procedure, diagnostic exam) has different business rules for required documents and maximum reimbursable amounts. Rather than encoding these differences in conditionals, each type has its own **policy** class implementing `IPoliticaTipoSolicitud`. Rules query the appropriate policy at evaluation time via `ITipoSolicitudProvider`.

### Facade Pattern (`services/motor_reglas_facade.py`)

`MotorReglasFacade` provides a unified, simplified interface for clients to interact with the rules engine. It coordinates the `EvaluadorSolicitudes` (rule evaluation) and `EjecutorAcciones` (state transitions), shielding consumers from the internal complexity.

### Dependency Injection

All services and rules receive their dependencies through constructor parameters. Rules that need external data (clock, provider catalog, policy provider) receive abstract ports -- never concrete implementations. This makes every component independently testable and replaceable.

---

## Design Principles

### SOLID

| Principle | How It Is Applied |
|-----------|-------------------|
| **Single Responsibility (SRP)** | Each class has exactly one reason to change. Domain objects hold data, rules validate one aspect each, states manage their own transitions, and services orchestrate. |
| **Open/Closed (OCP)** | New request types, rules, states, or policies can be added by creating a new class that implements the relevant interface -- no existing code needs modification. |
| **Liskov Substitution (LSP)** | All concrete states are interchangeable through `IEstadoSolicitud`; all rules through `ReglaEvaluacion`; all policies through `IPoliticaTipoSolicitud`. Substituting any implementation preserves correct behavior. |
| **Interface Segregation (ISP)** | Interfaces are minimal and focused. `IClock` exposes a single `today()` method; `IPrestadorHabilitadoCatalog` exposes a single `estaHabilitado()` method. No client is forced to depend on methods it does not use. |
| **Dependency Inversion (DIP)** | High-level modules (services, rules) depend on abstractions defined in `ports/` and abstract base classes, not on concrete implementations. The direction of dependency always points toward the domain. |

### Additional Principles

| Principle | How It Is Applied |
|-----------|-------------------|
| **DRY (Don't Repeat Yourself)** | Common contracts are defined once in abstract interfaces and reused across all implementations. Enumeration values are centralized in the `enums/` package. |
| **KISS (Keep It Simple, Stupid)** | Classes are deliberately simple. Value objects contain only data and a representation method. Policies return direct scalar values with no unnecessary logic. |
| **YAGNI (You Aren't Gonna Need It)** | No speculative code exists. Terminal states (`ApprovedState`, `RejectedState`) have empty action sets and minimal implementations -- nothing beyond what is required. |

### GRASP

| Principle | How It Is Applied |
|-----------|-------------------|
| **High Cohesion** | Each module groups only closely related responsibilities (e.g., all state classes in `states/`, all rules in `rules/`). |
| **Low Coupling** | The domain has zero dependencies on infrastructure. Rules depend on abstract ports, not concrete services. |
| **Creator** | Objects are created by the classes that have the information needed to initialize them (e.g., `UnderReviewState` creates `ApprovedState`/`RejectedState`). |
| **Polymorphism** | Rules, states, and policies all leverage polymorphic dispatch to eliminate conditional logic. |
| **Controller** | `MotorReglasFacade` acts as the coordinating controller for all use cases. |

---

## State Machine

The request follows a well-defined lifecycle:

```
  DRAFT ──[SUBMIT]──> SUBMITTED ──[START_REVIEW]──> UNDER_REVIEW
                                                        |
                                              [EVALUATE]  (stays in UNDER_REVIEW)
                                              [APPROVE] ──> APPROVED  (terminal)
                                              [REJECT]  ──> REJECTED  (terminal)
```

- **DRAFT**: Initial state. The only allowed action is `SUBMIT`.
- **SUBMITTED**: Awaiting review assignment. The only allowed action is `START_REVIEW`.
- **UNDER_REVIEW**: Active evaluation phase. Supports `EVALUATE`, `APPROVE`, and `REJECT`.
  - `APPROVE` requires the evaluation decision to be `APROBABLE`.
  - `REJECT` requires the evaluation decision to be `RECHAZABLE`.
- **APPROVED / REJECTED**: Terminal states with no further actions allowed.

---

## Business Rules

The `EvaluadorSolicitudes` runs all registered rules against a request. If any rule produces a finding (`HallazgoRegla`), the decision is `RECHAZABLE`; otherwise it is `APROBABLE`.

| Rule | Validation | External Dependency |
|------|-----------|---------------------|
| `ReglaConsistenciaDatos` | Patient, provider, type, and amount > 0 are present | None |
| `ReglaDocumentacionMinima` | All documents required by the type policy are attached | `ITipoSolicitudProvider` |
| `ReglaMontoMaximo` | Requested amount does not exceed the type policy maximum | `ITipoSolicitudProvider` |
| `ReglaPrestadorHabilitado` | Healthcare provider is active/enabled | `IPrestadorHabilitadoCatalog` |
| `ReglaVentanaTiempo` | Event date is within 60 days of today | `IClock` |

Adding a new rule requires only creating a class that extends `ReglaEvaluacion` and injecting it into the evaluator -- no existing rules or services need to change.

---

## Type Policies

Each request type defines its own required documents and maximum reimbursable amount:

| Type | Required Documents | Max Amount |
|------|--------------------|------------|
| Medicamento | FORMULA_MEDICA, FACTURA | $800,000 |
| Procedimiento Ambulatorio | ORDEN_MEDICA, FACTURA | $2,500,000 |
| Urgencias | HISTORIA_CLINICA_URGENCIAS, FACTURA | $3,500,000 |
| Examen Diagnostico | ORDEN_MEDICA, RESULTADO_EXAMEN, FACTURA | $1,200,000 |

Adding a new request type requires creating a new policy class implementing `IPoliticaTipoSolicitud` and registering it with the `ITipoSolicitudProvider` -- fully adhering to the Open/Closed Principle.
