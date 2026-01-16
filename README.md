# PC Service Hub (PC Hub Backend)

API REST para gestionar **clientes**, **tickets de servicio**, **equipos** e **inventario** para un negocio de armado/mantenimiento de PCs.

## Tech stack

* **Backend:** FastAPI, SQLAlchemy
* **DB:** PostgreSQL
* **Migraciones:** Alembic
* **Auth:** JWT + roles (admin / tech / client)
* **Dev:** Docker + Docker Compose
* **Azure:** App Service (containers), Azure Database for PostgreSQL (Flexible Server), Azure Container Registry (ACR), Key Vault (secrets), Application Insights (availability)

## Demo

* **Azure (Swagger /docs):** [https://pchub-api-dagon-a7hac2c5esffc9cx.centralus-01.azurewebsites.net/docs](https://pchub-api-dagon-a7hac2c5esffc9cx.centralus-01.azurewebsites.net/docs)
* **Local (Swagger /docs):** [http://localhost:8000/docs](http://localhost:8000/docs)

## Arquitectura (alto nivel)

* Cliente (Swagger/HTTP) → **App Service** (contenedor FastAPI)
* **ACR** almacena la imagen Docker; la Web App hace *pull* con **Managed Identity** (rol **AcrPull**)
* **PostgreSQL Flexible Server** como base de datos administrada
* **Key Vault** para secretos (referencias desde App Service)
* **Application Insights** (Availability test) para monitoreo básico

## Ejecución

### Requisitos (local)

* Docker Desktop
* Crear un archivo `.env` en la **raíz** del repo (usa `.env.example` como plantilla)

### Ejecución local (Docker Compose)

1. Abre PowerShell en la raíz del proyecto y ejecuta:

```bash
docker compose up --build
```

2. Abre Swagger:

* [http://localhost:8000/docs](http://localhost:8000/docs)

### Migraciones (local)

Si estás usando Docker Compose, una forma segura de aplicar migraciones desde el contenedor es:

docker compose run --rm api alembic upgrade head


> Si quieres correr migraciones: si tienes un venv con Alembic instalado y `DATABASE_URL` configurada, puedes usar `alembic upgrade head`.

---

## Variables de entorno

En local puedes definirlas en `.env`. En Azure se configuran como **Variables de entorno** y/o **Key Vault references**.

- DATABASE_URL=postgresql+psycopg2://user:pass@host:5432/pchub
- SECRET_KEY=cualquier_combinación_largo_de_texto
- ACCESS_TOKEN_EXPIRE_MINUTES=30
- WEBSITES_PORT=8000

---

## Uso (Swagger)

Entra a `/docs` y deberías ver el panel de Swagger.

![Swagger UI](docs/images/pc-hub1.png)

---

## Autenticación y roles

### Endpoints de auth

* `POST /auths/register`
* `POST /auths/login`
* `GET /auths/me`

![Authorize](docs/images/pc-hub-auth.png)

Si creaste la cuenta y luego iniciaste sesión, recuerda volver a presionar **Authorize** para que Swagger guarde el token:

![Authorize 2](docs/images/pc-hub-auth2.png)

### Roles

* **admin:** acceso completo
* **tech:** acceso a la mayoría de funcionalidades (típicamente Create/Read)
* **client:** login y lectura de sus tickets (según reglas del backend)

---

## Funcionalidades

### Resumen por módulo

* **Tickets:** CRUD
* **Clients:** CRUD
* **Inventory:** CRUD
* **Inventory movements:** Create/Read (auditoría de movimientos)
* **Devices:** CRUD

### Permisos (resumen)


| Recurso             |       admin     |           tech          |     client     |
| ------------------- | ------------:   | ---------------------:  | -------------: |
| Auth (`/auths/*`)   |   Create/Read   |      Create/Read        |  Create/Read   |
| Tickets             |       CRUD      |      Create/Read        |     (Read)     |
| Clients             |       CRUD      |      Create/Read        |       No       |
| Inventory           |       CRUD      |      Create/Read        |       No       |
| Inventory movements |   Create/Read   |      Create/Read        |       No       |
| Devices             |       CRUD      |      Create/Read        |       No       |

---

## CRUDs (detalles)

### Tickets

Roles: **admin**, **tech**, **client** (con restricciones)

* **Create:** `device_id` (opcional), `client_id` (opcional), `title`, `description` (opcional), `priority` (low/medium/high), `service_type` (repair/maintenance/diagnostic/build/upgrade), `estimated_cost` (opcional)
* **Read:** lista y por id; el rol **client** puede ver su lista de tickets (según reglas)
* **Update:** campos opcionales + `final_cost`, `status` (new/in_progress/waiting_parts/cancelled/ready/delivered)
* **Delete:** por id (normalmente solo admin)

### Clients

Roles: **admin**, **tech**

* **Read:** lista y por id
* **Create:** `user_id`, `first_name`, `last_name`, `rfc`, `email`, `phone_number` (opcional), `street_adress`, `interior_number` (opcional), `outer_number`, `postal_code`, `city`, `state`
* **Update/Delete:** por id

### Inventory

Roles: **admin**, **tech**

* **Create:** `name`, `category` (other/cpu/motherboard/ram/gpu/storage/psu/case/cooling/thermal/cables_adapters/peripherals/networking/tools/consumables/replacement_parts), `brand` (opcional), `description` (opcional), `location` (opcional), `stock` (opcional), `unit_cost` (opcional), `unit_price` (opcional)
* **Read:** lista y por id
* **Update/Delete:** por id

#### Inventory movements (auditoría)

Tabla intermedia entre **tickets** e **inventory** para registrar entradas/salidas/ajustes.

* **Create:** `inventory_id` (opcional), `ticket_id` (opcional), `movement_type` (in/out/adjustment), `adjustment_direction` (increase/decrease), `quantity`, `reason` (purchase/sell/used_in_ticket/returned/damaged/correction/other), `description` (opcional), `unit_cost` (opcional), `unit_price` (opcional)
* **Read:** lista y por id

### Devices

Roles: **admin**, **tech**

* **Create:** `device_type` (laptop/pc/all_in_one/other), `brand`, `model`, `notes` (opcional)
* **Read:** lista y por id
* **Update/Delete:** por id

---

## Deploy en Azure

Servicios usados:

* **Azure App Service (Linux, container)**
* **Azure Container Registry (ACR)**
* **Azure Database for PostgreSQL – Flexible Server**
* **Azure Key Vault** (secret references en App Service)
* **Application Insights** (Availability test)

---