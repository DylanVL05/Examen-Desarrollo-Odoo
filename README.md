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




## 📌 Suposiciones y Decisiones

### Suposiciones

El cálculo automático de cantidad (product_uom_qty) aplica a líneas de pedido en ventas y se basa en las dimensiones ingresadas (Largo, Ancho y Alto)

Los usuarios deben ingresar siempre valores positivos , de no ingresar dimensiones aparecera una excepcion 

El modulo esta pensado para escenarios donde los productos se cotizan por volumen o medida ( ejem materiales de construccion)

Las unidades de las dimensiones están expresadas en metros (m) y se asume que el resultado (L×A×H) equivale a la cantidad en metros cúbicos.

EL reporte de PDF  solo esconde cantidad en el saleorder ya que en la factura se debe dar otra vista heredada de otro QWEB , 

El reporte PDF de venta se hereda del estándar de Odoo y se modifica únicamente para añadir las columnas de dimensiones y ocultar la columna estándar de “Cantidad”

### Decisiones 

Como ambiente lo trabajé en un Docker Compose y se desarrolló en Ubuntu Linux en Visual Studio Code.

Se heredó el modelo sale.order.line para no tocar la lógica del core.

Para correr los test hice 2 scripts, uno en Shell y otro en PowerShell, para compatibilidad del test de integración tanto en Windows como en Linux.

Opté por usar una BD momentánea a la hora de hacer los test de integración para no ensuciar la principal; esta se crea y se elimina luego de pasar los test.

## Alcance del modulo 
    
Cálculo automático de cantidad en líneas de venta a partir de L×A×H.

Vistas actualizadas (formulario, árbol y reporte PDF) que incluyen dimensiones.

Validaciones básicas en la captura de datos (dimensiones > 0).

Compatibilidad con Odoo 18.0 y PostgreSQL 16, probado en contenedor Docker.

## Posibles mejoras

Agregar la función de conversión.

Integrar un cálculo con el módulo del inventario para que el stock se controle según el volumen calculado.

Extender la cobertura de los test.


## 👤 Autor
- **Dylan Venegas Lopez**  


