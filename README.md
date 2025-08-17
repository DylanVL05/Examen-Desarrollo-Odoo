# Módulo Odoo - Dimensional Sales (Qty from L×A×H)

Este módulo extiende **Odoo Sales** para calcular automáticamente la **cantidad** (`product_uom_qty`) de una línea de pedido a partir de sus dimensiones: **Largo × Ancho × Alto**.  
Además, añade estos campos a la interfaz y al reporte PDF de la orden de venta.

---

-----------------------------------------------------------------------------
## 📦 Requerimientos

- **Docker** y **Docker Compose** instalados (Docker Desktop si es Win).
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

    Parar la ejecucion actual del test se hace luego de levantar el docker (ya sea win o linux) prepare un script que se debe ejecutar luego de tener el container up , dicho script ejecuta las pruebas de forma aislada en una base momentanea para hacer el test lo completa y luego cierra

    1. **Si se ejecuta en Linux se debe ejecutar** "run_test.sh"
       ```bash
        sudo ./run_test.sh

    
    2. **Si se ejecuta en windows se debe ejecutar** "run_test.ps1"
   
    - Abres powershell como administrador
    -vas a cd C:\ruta\a\proyecto-ExamenOdoo
    - Y ejecutas .\run_tests.ps1

      

   


## Notas importantes del modulo

📖 Manejo de Unidades de Medida (UoM)

El cálculo de cantidad se realiza como: 
   "Cantidad = Largo × Ancho × Alto"  (interpretado en metros cubicos si las dimensiones estan en metros)
      

      -En caso de que el producto posee una UoM distinta no se realiza conversion automatica, en este caso hay 2 opciones:

      1.Configurar la unidad de medida base

      2.Agregar en el modulo la capacidad de conversion utilizando
      product_uom._compute_quantity(...)




    





