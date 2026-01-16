# PC Service Hub

API para gestionar clientes, tickets de servicio, equipos e inventario para un negocio de armado/mantenimiento de PCs.

## Ejecución
Se puede ejecutar localmente o acceder a una url para visualizar su funcionamiento

### Ejecución local
Para ejecutar de manera local se deben seguir los siguientes pasos:

- #### Requisitos para ejecución local
Se deben contar con los siguientes requisitos para ejecutar localmente la API:
- Docker Desktop
- Crear un archivo .env en la raiz y añadir las variables de entorno (dichas variables estan presentes en el .env.example)

- ### Pasos a seguir para la ejecución local
- Abrir un Powershell en la raiz del proyecto y ejecutar el siguiente comando: docker compose up --build
- Dirigirse a su navegador (puede haber problemas de compatibilidad con algunos, de preferencia usar Chrome) e ir a la siguiente direccion [pc-hub-api](http://localhost:8000/docs)
- Si quiere ejecutar migraciones locales usar: alembic upgrade head

### Ejecución en Azure
La API se subio a la nube de Azure:
URL: [pc-hub-api](https://pchub-api-dagon-a7hac2c5esffc9cx.centralus-01.azurewebsites.net/docs)

## Uso
Si quieres probar el funcionamiento, es importante ir a /docs (en los links dados anteriormente ya esta dirigo a /docs) y debería aparecer lo siguiente en pantalla:
[pc-hub-image1](docs/images/pc-hub1.png)