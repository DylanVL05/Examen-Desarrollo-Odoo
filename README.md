# Módulo Odoo - Dimensional Sales (Qty from L×A×H)

Este módulo extiende **Odoo Sales** para calcular automáticamente la **cantidad** (`product_uom_qty`) de una línea de pedido a partir de sus dimensiones: **Largo × Ancho × Alto**.  
Además, añade estos campos a la interfaz y al reporte PDF de la orden de venta.

---

-----------------------------------------------------------------------------
## 📦 Requerimientos

- **Docker** y **Docker Compose** instalados.
- **Puerto 8069** libre en la máquina local.
- **Internet** para descargar imágenes de Docker.
- No se necesita instalación previa de Odoo o PostgreSQL.  

---

-----------------------------------------------------------------------------
## ⚙️ Instalación y ejecución (Pasos)

1. **Clonar el repositorio** o descargar el proyecto.
   
2. **Ubicarse en la carpeta raíz** del proyecto (`Examen-Desarrollo-Odoo`):
   ```bash
   cd proyecto-ExamenOdoo

3. **Levantar Odoo y PostgreSQL**
 - Se levantan el contenedor con los servicios mediante el comando: 
    ```bash
    docker compose up 

- Quedaria listo en http://localhost:8069 con las credencias admin admin 
  
- Ahi ya se puede entrar, activar el modo developer en settings y activar luego 
el sales para a continuacion activar el modulo " Dimensional Sales (Qty from L×A×H)" 

-----------------------------------------------------------------------------

## Correr la prueba o test  

    Parar la ejecucion actual del Test prepare un YAML llamado "docker-compose.test.yml" 
    para pruebas aparte para evitar choque de puertos o algun problema 

    Pasos: 

1. **Ubicarse en la carpeta raíz** del proyecto (`proyecto-ExamenOdoo`):
   ```bash
   cd proyecto-ExamenOdoo


2. **Ejecutar las pruebas** directamente en consola y cierra proceso al finalizar:
 ```bash
    docker compose -f docker-compose_test.yml up --abort-on-container-exit


        


