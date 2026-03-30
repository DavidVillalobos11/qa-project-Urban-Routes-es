🚕 Urban Routes - QA Automation Project
📌 Descripción del proyecto

Este proyecto consiste en la automatización de pruebas para la aplicación web Urban Routes, la cual permite a los usuarios solicitar un taxi.

El objetivo principal es validar el flujo completo de solicitud de un taxi mediante pruebas automatizadas utilizando Selenium y Python.

⚙️ Tecnologías y herramientas utilizadas
Python
Selenium WebDriver
PyCharm
Git y GitHub
🧪 Funcionalidad probada

Las pruebas automatizadas cubren el siguiente flujo:

Configuración de la dirección de origen y destino
Selección de la tarifa Comfort
Ingreso del número de teléfono
Agregado de tarjeta de crédito
Escritura de mensaje al conductor
Selección de extras (manta y pañuelos)
Selección de 2 helados
Solicitud de taxi
Espera de asignación de conductor (opcional)
▶️ Instrucciones para ejecutar las pruebas
Clonar el repositorio:
git clone git@github.com:TU_USUARIO/qa-project-Urban-Routes-es.git
Navegar al proyecto:
cd qa-project-Urban-Routes-es
Instalar dependencias (si es necesario):
pip install selenium
Ejecutar las pruebas:
python main.py
📂 Estructura del proyecto
main.py → Contiene las pruebas automatizadas
helpers.py → Función para obtener código de verificación
data.py → Datos de prueba (URL, teléfono, etc.)
