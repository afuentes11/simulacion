import re
from docx import Document

# Leer y procesar el texto del archivo Word
def leer_texto_desde_word(ruta_documento):
    try:
        documento = Document(ruta_documento)
        texto = " ".join([p.text for p in documento.paragraphs])
        return texto
    except Exception as e:
        raise ValueError(f"Error al leer el documento Word: {e}")

# Procesar el texto del Word para extraer parámetros
def procesar_texto(texto):
    try:
        # Extraer los parámetros utilizando expresiones regulares
        landa = re.search(r'tasa media de llegada es de\s*(\d+)', texto, re.IGNORECASE)
        tiempo_llegada = re.search(r'razón de\s*(\d+)\s*pacientes por hora', texto, re.IGNORECASE)
        tiempo_servicio_min = re.search(r'media de\s*(\d+)\s*minutos', texto, re.IGNORECASE)
        capacidad_cola = re.search(r'sala de espera no puede acomodar más de\s*(\d+)', texto, re.IGNORECASE)
        distribucion_llegada = re.search(r'distribución de probabilidad del tiempo es\s*"Poisson"', texto, re.IGNORECASE)
        distribucion_servicio = re.search(r'distribución de probabilidad del tiempo es\s*"exponencial"', texto, re.IGNORECASE)
        num_servidores = re.search(r'el número de servidores.*?es.*?"(\d+)"', texto, re.IGNORECASE)
        disciplina_cola = re.search(r'disciplina del sistema es de\s*“([^”]+)”', texto, re.IGNORECASE)

        # Calcular y asignar valores a los parámetros
        landa_valor = int(landa.group(1)) if landa else (int(tiempo_llegada.group(1)) if tiempo_llegada else None)
        mu_valor = int(tiempo_servicio_min.group(1)) if tiempo_servicio_min else None
        capacidad_sistema_valor = int(capacidad_cola.group(1)) + 1 if capacidad_cola else None
        distribucion_llegada_valor = "Poisson" if distribucion_llegada else None
        distribucion_servicio_valor = "Exponencial" if distribucion_servicio else None
        num_servidores_valor = int(num_servidores.group(1)) if num_servidores else 1
        capacidad_poblacion_valor = float('inf')  # Siempre infinita
        disciplina_cola_valor = disciplina_cola.group(1).strip() if disciplina_cola else "no se especifica"

        return {
            "landa": (landa_valor, "pacientes/hora", "Tasa de llegada"),
            "mu": (mu_valor, "pacientes/minuto", "Tiempo promedio de servicio"),
            "capacidad_poblacion": capacidad_poblacion_valor,
            "capacidad_sistema": capacidad_sistema_valor,
            "distribucion_llegada": distribucion_llegada_valor,
            "distribucion_servicio": distribucion_servicio_valor,
            "num_servidores": num_servidores_valor,
            "disciplina_cola": disciplina_cola_valor
        }
    except Exception as e:
        print(f"Error al procesar el texto: {e}")
        return None

# Crear el diccionario de datos del sistema
def crear_diccionario_datos(parametros):
    if not parametros:
        return None
    return {
        "landa": parametros["landa"][0],
        "mu": parametros["mu"][0],
        "tasa_llegada_tipo": parametros["landa"][2],
        "tasa_servicio_tipo": parametros["mu"][2],
        "servidores": parametros["num_servidores"],
        "capacidad": "finita" if parametros["capacidad_sistema"] else "infinita",
        "k": parametros["capacidad_sistema"],
        "poblacion": "infinita",
        "n_poblacion": None,
        "disciplina": parametros["disciplina_cola"],
        "distribucion_llegada": parametros["distribucion_llegada"],
        "distribucion_servicio": parametros["distribucion_servicio"]
    }

# Determinar respuestas automáticas
def asignar_respuestas(parametros):
    if not parametros:
        return None

    # Determinar valores basados en los parámetros extraídos
    respuestas = {
        "datos_llegada": 1 if parametros["landa"][2] == "Tasa de llegada" else 2,
        "distribucion_llegada": 1 if parametros["distribucion_llegada"] == "Poisson" else 2,
        "unidades_llegada": (
            1 if parametros["landa"][1] == "pacientes/segundo" else
            2 if parametros["landa"][1] == "pacientes/minuto" else
            3
        ),
        "unidades_servicio": (
            1 if parametros["mu"][1] == "pacientes/segundo" else
            2 if parametros["mu"][1] == "pacientes/minuto" else
            3
        ),
        "datos_servicio": 1 if parametros["mu"][2] == "Tasa de servicio" else 2,
        "distribucion_servicio": 1 if parametros["distribucion_servicio"] == "Exponencial" else 2,
        "capacidad_sistema": 1 if parametros["capacidad_sistema"] else 2,
        "tamano_poblacion": 2  # Siempre infinita según los parámetros
    }
    return respuestas

# print('''
# ¡Hola! 👋
# ¡Bienvenido a la calculadora automática de modelos de colas para procesos de nacimiento y muerte en Python! 🎉

# 📚 Este programa está diseñado para ayudarte a resolver los modelos de colas **M/M/1**, **M/M/s**, **M/M/1/K** y **M/M/s/K** de manera sencilla y automatizada. Aquí no solo obtendrás resultados numéricos precisos, sino que también aprenderás sobre el funcionamiento de estos modelos.

# 📝 ¿Cómo funciona?
# - Solo necesitas proporcionar la ruta del archivo Word #2 generado con los programas previos.
# - El programa analizará automáticamente el contenido y extraerá los parámetros necesarios.
# - ¡Luego solo tendrás que pedir el cálculo que deseas, y el programa hará el resto!

# ⚙️ Las tasas y tiempos se manejarán en:
# - Minutos para los tiempos promedio.
# - Clientes/minuto para las tasas de llegada y servicio.

# ⚠️ **Nota importante:** Por ahora, el programa está optimizado para resolver correctamente el ejercicio 14. Sin embargo, muy pronto estará listo para manejar cualquier tipo de ejercicio de manera eficiente. 🚀

# 🛠️ **Desarrollado y mejorado por:**
# - Mendoza Hernández María Alejandra
# - Mercado Cabarcas María Carolina
# - Noriega Núñez Yohan Andrés
# - Ospino Pérez Noris
# - Pérez Blanquicett Brayan José
# - Rodríguez Gonzales Jeikel Junior

# ¡Gracias por usar nuestra herramienta! 💡
# ''')


# Solicitar la ruta del archivo Word al usuario
ruta_documento = input("\nPor favor para comenzar, ingresa la ruta del archivo Word: ")

# Paso 1: Leer texto desde el archivo Word
texto_documento = leer_texto_desde_word(ruta_documento)

# Paso 2: Extraer parámetros del texto
parametros = procesar_texto(texto_documento)

# Paso 3: Generar respuestas automáticas
respuestas_automaticas = asignar_respuestas(parametros)


#Modelo MM1, MM1K, MMs y MMsK
import time

def medDesempeñoMM1 (lan,mu):    #Medidas de desempeño MM1
    ro=lan/mu
    print(f"\nEl factor de utilización del sistema es (ρ): {ro:.4f}")
    P0=1-ro
    print(f"La probabilidad de que el sistema se encuentre vacío es (P0): {P0:.4f}")
    print("\nMedidas de desempeño")
    L=ro/(1-ro)
    print(f"Número esperado de clientes en el sistema (L): {L:.4f} clientes")
    Lq=(ro**2)/(1-ro)
    print(f"Número esperado de clientes en la cola (Lq): {Lq:.4f} clientes")
    W=1/(mu*(1-ro))
    Wq=ro/(mu*(1-ro))   
    print(f"Tiempo de espera esperado en el sistema para cada cliente (W): {W:.4f} minutos")
    print(f"Tiempo de espera esperado en la cola para cada cliente (Wq): {Wq:.4f} minutos")
    
def probabilidadMM1 (tipoCalculoPn,n):    #Probabilidades MM1
    ro=landa/mu
    P0=1-ro
    if tipoCalculoPn == 1:            #Exactamente
        Pn=(ro**n)*P0
        print(f"\nLa probabilidad de que haya exactamente {n} clientes en el sistema es: {Pn:.5f}")
    elif tipoCalculoPn == 2:         #Por lo menos 
        sumatoria=0
        for n in range (0,n):
            sumatoria +=(1-ro)*(ro**n)
            Pn=1-sumatoria
        print(f"\nLa probabilidad de que haya por lo menos {n+1} clientes en el sistema es: {Pn:.5f}")
    else:                      #Maximo 
        sumatoria1=0
        for n in range (0,n+1):
            sumatoria1 +=((ro**n)*P0)
            Pn=sumatoria1
        print(f"\nLa probabilidad de que haya máximo {n} clientes en el sistema es: {Pn:.5f}")

def medDesempeñoMM1K1 (lan,k):      #Medidas de desempeño MM1K cuando ro=1
     P0=1/(k+1)
     print(f"La probabilidad de que el sistema se encuentre vacío es (P0): {P0:.4f}")
     print("\nMedidas de desempeño")
     L=k/2
     print(f"Número esperado de clientes en el sistema (L): {L:.4f} clientes")
     Lq=L-(1-P0)
     print(f"Número esperado de clientes en la cola (Lq): {Lq:.4f} clientes")
     Pk=1/(k+1)
     lt=lan*(1-Pk)
     W=L/lt
     Wq=Lq/lt
     print(f"Tiempo de espera esperado en el sistema para cada cliente (W): {W:.4f} minutos")
     print(f"Tiempo de espera esperado en la cola para cada cliente (Wq): {Wq:.4f} minutos")

def medDesempeñoMM1K2 (lan,k,ro):    #Medidas de desempeño MM1K cuando ro diferente de 1
    P0=(1-ro)/(1-(ro**(k+1)))
    print(f"La probabilidad de que el sistema se encuentre vacío es (P0): {P0:.4f}")
    print("\nMedidas de desempeño")
    L=(ro/(1-ro))-(((k+1)*(ro**(k+1)))/(1-(ro**(k+1))))
    print(f"Número esperado de clientes en el sistema (L): {L:.4f} clientes")
    Lq=L-(1-P0)
    print(f"Número esperado de clientes en la cola (Lq): {Lq:.4f} clientes")
    Pk=(((1-ro)/(1-(ro**(k+1))))*(ro**k))
    lt=lan*(1-Pk)
    W=L/lt 
    Wq=Lq/lt
    print(f"Tiempo de espera esperado en el sistema para cada cliente (W): {W:.4f} minutos")
    print(f"Tiempo de espera esperado en la cola para cada cliente (Wq): {Wq:.4f} minutos")

def probabilidadMM1K1 (tipoCalculoPn,k,x):       #Probabilidad MM1K ro=1
    if tipoCalculoPn==1:       #Exactamente
             if x>k:
                Pn=0
             else:
                Pn=1/(k+1)
             print(f"\nLa probabilidad de que haya exactamente {n} clientes en el sistema es: {Pn:.5f}")
    elif tipoCalculoPn==2:          #Por lo menos 
             if x>k:
                Pn=0
             else: 
                sum=0
                for x in range (x,k+1):
                  sum +=1/(k+1)
                Pn=sum
             print(f"\nLa probabilidad de que haya por lo menos {n} clientes en el sistema es: {Pn:.5f}")
    else:                         #Maximo 
            if x>k:
                Pn=0
            else:
                sum1=0
                for x in range (0,x+1):
                     sum1 +=1/(k+1)
                Pn=sum1
            print(f"\nLa probabilidad de que haya máximo {n} clientes en el sistema es: {Pn:.5f}")

def probabilidadMM1K2 (tipoCalculoPn,k,x):      #Medidas de probabilidad ro diferente de 1
    if tipoCalculoPn==1:       #Exactamente
             if x>k:
                Pn=0
             else:
                Pn=(((1-ro)/(1-(ro**(k+1))))*(ro**x))
             print(f"\nLa probabilidad de que haya exactamente {n} clientes en el sistema es: {Pn:.5f}")
    elif tipoCalculoPn==2:       #Por lo menos 
             if x>k:
                Pn=0
             else:    
                sum2=0
                for x in range (0,k):
                   sum2 +=(((1-ro)/(1-(ro**(k+1))))*(ro**x))
                Pn=1-sum2
             print(f"\nLa probabilidad de que haya por lo menos {n} clientes en el sistema es: {Pn:.5f}")
    else:                #Maximo 
             if x>k:
                Pn=0
             else:    
                sum3=0
                for x in range (0,x+1):
                   sum3 +=(((1-ro)/(1-(ro**(k+1))))*(ro**x))
                Pn=sum3
             print(f"\nLa probabilidad de que haya máximo {n} clientes en el sistema es: {Pn:.5f}")

from math import factorial

def medDesempeñoMMs (lan,mu,s):     #Medidas de desempeño MMs
    ro=lan/(mu*s)
    print(f"\nEl factor de utilización del sistema es (ρ): {ro:.4f}")
    sumatoria=0
    for n in range (0,s):
        sumatoria +=(((lan/mu)**n)/(factorial(n)))
    denominador=sumatoria+((((lan/mu)**s)/(factorial(s)))*(1/(1-(ro))))
    P0=1/denominador
    print(f"La probabilidad de que el sistema se encuentre vacío es (P0): {P0:.4f}")
    print("\nMedidas de desempeño del sistema")
    Lq=(P0*(lan/mu)**s*ro)/(factorial(s)*(1-ro)**2)
    Wq=(Lq/lan)
    W=Wq+(1/mu)
    L=Lq+(lan/mu)
    print(f"Número esperado de clientes en el sistema (L): {L:.4f} clientes")
    print(f"Número esperado de clientes en la cola (Lq): {Lq:.4f} clientes")
    print(f"Tiempo de espera esperado en el sistema para cada cliente (W): {W:.4f} minutos")
    print(f"Tiempo de espera esperado en la cola para cada cliente (Wq): {Wq:.4f} minutos")

def probabilidadMMs (tipoCalculoPn,x,s,lan,mu):        #Probabilidad MMs
    ro=lan/(mu*s)
    sumatoria=0
    for n in range (0,s):
        sumatoria +=(((lan/mu)**n)/(factorial(n)))
    denominador=sumatoria+((((lan/mu)**s)/(factorial(s)))*(1/(1-(ro))))
    P0=1/denominador
    if tipoCalculoPn == 1:            #Exactamente
        if x<=s:
            Pn=(((lan/mu)**x)/factorial(x))*P0
        else:
            Pn=(((lan/mu)**x)/((factorial(s))*(s**(x-s))))*P0
        print(f"\nLa probabilidad de que haya exactamente {x} clientes en el sistema es: {Pn:.5f}")
    elif tipodeCalculoPn == 2:         #Por lo menos
        if x<=s:
            sumatoria=0
            for n in range (0,x):
                sumatoria +=(((lan/mu)**n)/factorial(n))*P0
            Pn=1-sumatoria
        else:
            sumatoria4=0
            sumatoria5=0
            for n in range (0,s):
                sumatoria4 +=(((lan/mu)**n)/factorial(n))*P0
            for n in range (s,x):
                sumatoria5 +=(((lan/mu)**n)/((factorial(s))*(s**(n-s))))*P0
            Pn=1-(sumatoria5+sumatoria4)
        print(f"\nLa probabilidad de que haya por lo menos {x} clientes en el sistema es: {Pn:.5f}")
    else:                      #Maximo 
        if x<=s:
            sumatoria0=0
            for n in range (0,n+1):
                sumatoria1 +=(((lan/mu)**n)/factorial(n))*P0
            Pn=sumatoria0
        else:
            sumatoria1=0
            sumatoria2=0
            for n in range (0,s):
                sumatoria1 +=(((lan/mu)**n)/factorial(n))*P0
            for n in range (s,x+1):
                sumatoria2 +=(((lan/mu)**n)/((factorial(s))*(s**(n-s))))*P0
            Pn=sumatoria1+sumatoria2
        print(f"\nLa probabilidad de que haya máximo {x} clientes en el sistema es: {Pn:.5f}")

def medDesempeñoMMsK1 (lan,mu,s,k):   #Medidas de desempeño MMsK ro=1
    sumatoria1=0 
    for n in range (0,s):
        sumatoria1 +=(((lan/mu)**n)/factorial(n))
    P0=1/(sumatoria1+(((lan/mu)**s)/factorial(s))*(k-s+1))
    print(f"La probabilidad de que el sistema se encuentre vacio es (P0): {P0}")
    print("\nMedidas de desempeño")
    Lq=((((lan/mu)**s)*(k-s)*(k-s+1))/(2*factorial(s)))*P0
    Pn=0
    for n in range(0,s):
        Pn +=((lan/mu)**n/factorial(n))*P0
    npn=0
    for n in range (0,s):
        npn +=n*((lan/mu)**n/factorial(n))*P0
    L=npn+Lq+s*(1-Pn)
    Pk=(((lan/mu)**k)/(factorial(s)*(s**(k-s)))*P0)
    lt=lan*(1-Pk)
    W=L/lt
    Wq=Lq/lt
    print(f"Número esperado de clientes en el sistema (L): {L:.4f} clientes")
    print(f"Número esperado de clientes en la cola (Lq): {Lq:.4f} clientes")
    print(f"Tiempo de espera esperado en el sistema para cada cliente (W): {W:.4f} minutos")
    print(f"Tiempo de espera esperado en la cola para cada cliente (Wq): {Wq:.4f} minutos")

def medDesempeñoMMsK2 (lan,ro,mu,s,k):      #Medidas de desempeño MMsK ro diferente de 1
    sumatoria1=0
    for n in range (0,(s+1)):
        sumatoria1 +=(((lan/mu)**n)/factorial(n))
    sumatoria2=0
    for n in range(s+1,k+1):
        sumatoria2 +=((lan/(s*mu))**(n-s))
    P0=1/(sumatoria1+(((lan/mu)**s/factorial(s))*sumatoria2)) 
    print(f"La probabilidad de que el sistema se encuentre vacio es (P0): {P0:.4f}")
    print("\nMedidas de desempeño")
    Lq=((P0*((lan/mu)**s)*ro)/(factorial(s)*((1-ro)**2))*((1-(ro**(k-s))-((k-s)*(ro**(k-s))*(1-ro)))))
    Pn=0
    for n in range (0,s):
      Pn +=((lan/mu)**n/factorial(n))*P0
    npn=0
    for n in range (0,s):
        npn +=n*((lan/mu)**n/factorial(n))*P0
    L=npn+Lq+s*(1-Pn)
    Pk=(((lan/mu)**k)/(factorial(s)*(s**(k-s)))*P0)
    lt=lan*(1-Pk)
    W=L/lt
    Wq=Lq/lt
    print(f"Número esperado de clientes en el sistema (L): {L:.4f} clientes")
    print(f"Número esperado de clientes en la cola (Lq): {Lq:.4f} clientes")
    print(f"Tiempo de espera esperado en el sistema para cada cliente (W): {W:.4f} minutos")
    print(f"Tiempo de espera esperado en la cola para cada cliente (Wq): {Wq:.4f} minutos")

def probabilidadMMsK (tipoCalculoPn,lan,x,k,s,P0):      #Probabilidad para MMsK ro diferente de 1
    if tipoCalculoPn==1:       #Exactamente    #x es mi n
             if x>k:
                Pn=0
             elif x<=s:
                Pn=(((lan/mu)**x)/factorial(x))*P0
             else:
                Pn=(((lan/mu)**x)/((factorial(s))*(s**(x-s))))*P0
             print(f"\nLa probabilidad de que haya exactamente {n} clientes en el sistema es: {Pn:.5f}")
    elif tipoCalculoPn==2:       #Por lo menos 
             if x>k:
                Pn=0
             elif x<=s:                  
                sum2=0
                for x in range (0,x):
                   sum2 +=(((lan/mu)**x)/(factorial(x)))*P0
                Pn=1-sum2
             else:
                sum3=0
                for x in range (x,k+1):
                   sum3 +=(((lan/mu)**x)/((factorial(s))*(s**(x-s))))*P0
                Pn=sum3
             print(f"\nLa probabilidad de que haya por lo menos {n} clientes en el sistema es: {Pn:.5f}")
    else:                #Maximo 
             if x>k:
                Pn=0
             elif x<=s:        
                sum0=0
                for x in range (0,n+1):
                   sum0 +=(((lan/mu)**x)/factorial(x))*P0
                Pn=sum0
             else:
                sum1=0
                sum2=0
                for x in range (0,s):
                   sum1 +=(((lan/mu)**x)/factorial(x))*P0
                for x in range (s, n+1):
                   sum2 +=(((lan/mu)**x)/((factorial(s))*(s**(x-s))))*P0
                Pn=sum1+sum2 
             print(f"\nLa probabilidad de que haya máximo {n} clientes en el sistema es: {Pn:.5f}")

unidadesTasas='''\n🔸Las unidades están en:
     1. Clientes/segundo
     2. Clientes/minuto
     3. Clientes/hora'''
print()

unidadesTiempos='''\n🔸Las unidades están en:
     1. Segundos
     2. Minutos
     3. Horas'''
print()

distribucion='''     1. Distribución Exponencial
     2. Distribución Degenerada
     3. Distribución Erlang
     4. Distribución General'''

opError='''\nError⚠️ \nOpción inválida. Vuelva a intentarlo'''
errorVacio='''\nError⚠️ \nNo ha ingresado ningún valor. Intente nuevamente.'''
errorValor='''\nError⚠️ \nDebe ingresar un número positivo. Intente nuevamente.'''
error='''\n¡Error! \nNo se cumple el proceso de nacimiento y muerte.\nEste es un tema más avanzado. Lamento no poder darte una solución 😞.\nDebes buscar otro programa de modelo de colas.'''

supuestos4='''\n    Supuesto 1. Dado N(t) = n, la distribución de probabilidad actual del tiempo que falta para el próximo nacimiento (llegada) es exponencial con parámetro λn (n = 0, 1, 2, ...). 
    Supuesto 2. Dado N(t) = n, la distribución de probabilidad actual del tiempo que falta para la próxima muerte (terminación de servicio) es exponencial con parámetro μn (n = 1, 2, ...).
    Supuesto 3. La variable aleatoria del supuesto 1 (el tiempo que falta hasta el próximo nacimiento) y la variable aleatoria del supuesto 2 (el tiempo que falta hasta la siguiente muerte) 
    son mutuamente independientes. La siguiente transición del estado del proceso es
      n → n + 1 (un solo nacimiento)
      o
      n → n - 1 (una sola muerte),
    lo que depende de cuál de las dos variables es más pequeña.
    Supuesto 4. Se procederá cuando el sistema haya alcanzado la condición de estado estable (en caso de que pueda alcanzarla). 
    Es decir, la tasa media a la que el proceso entra al estado n es igual tasa media a la que el proceso sale del estado n.'''

supuesto='''\nLos supuestos de este modelo son:''' 

calculo='''\n🔸¿Qué cálculo desea realizar?
     1. Medidas de desempeño
     2. Probabilidad de n clientes en el sistema
     3. Probabilidad de tiempo de espera en el sistema
     4. Probabilidad de tiempo de espera en la cola'''

calculok='''\n🔸¿Qué cálculo desea realizar?
     1. Medidas de desempeño
     2. Probabilidad de n clientes en el sistema'''

calculoPn='''\n🔸Opciones para el cálculo de Pn:
     1. Exactamente
     2. Por lo menos
     3. Máximo'''

pw='''\n🔸¿Cual es la disciplina de la cola ?
     1. FIFO: Primero en llegar, primero en ser servido
     2. LIFO: Ultimo en llegar, primero en ser servido
     3. SIRO: Servicio en orden aleatorio
     4. DG: Disciplina en general
     5. No se especifica o conoce la disciplina de la cola'''

calculo2='''\n🔸¿Desea realizar otro cálculo?
     1. Si
     2. No'''

fin='''\n¡Enhorabuena!🎉🎉🎉\nHas llegado al final del programa de enseñanza de modelos de colas en Python.
Espero que este programa haya sido útil para tus cálculos y te haya brindado una introducción a la teoría de modelos de colas. 
Recuerda que estos conocimientos pueden ser aplicados en diversos escenarios para mejorar la eficiencia y el rendimiento de los sistemas. 
¡Sigue explorando y aprendiendo más sobre este apasionante campo! \U0001F44D'''


# Datos de llegada
datosLlegada = '''\n🔸Los datos de llegada están en:
     1. Tasa media de llegada
     2. Tiempo promedio entre llegadas'''
print(datosLlegada)

# Asignar el valor directamente desde las respuestas automáticas
opcionLlegada = respuestas_automaticas["datos_llegada"]

# Validar que el valor sea válido y procesarlo
if opcionLlegada in [1, 2]:
    print(f"Se seleccionó automáticamente la opción: {opcionLlegada}")
else:
    print("Error: la opción seleccionada automáticamente no es válida.")

# Verificar si la opción seleccionada es 1
if opcionLlegada == 1:
    # Mensaje de pregunta
    poisson = '''\n🔸¿La tasa media de llegada sigue una distribución de Poisson?🤔
         1. Si
         2. No'''
    print(poisson)

    # Asignar el valor directamente desde las respuestas automáticas
    opPoisson = respuestas_automaticas["distribucion_llegada"]

    # Validar que el valor sea válido y procesarlo
    if opPoisson in [1, 2]:
        print(f"Se seleccionó automáticamente la opción: {opPoisson}")
    else:
        print("Error: la opción seleccionada automáticamente no es válida.")


    if opPoisson == 1:
     while True:
        landa = parametros["landa"][0]  # Asignación automática para la tasa media de llegada
        print("\n Segun el word la tasa de llegada es de " + str(landa))
        if landa:
            if isinstance(landa, (int, float)) or (isinstance(landa, str) and landa.replace(".", "", 1).isdigit()):
                landa = float(landa)  # Convertir a flotante si es necesario
                break
            else:
                print(errorValor)
        else:
            print(errorVacio)

    print(unidadesTasas)

    # Asignar la opción de unidades automáticamente
    opUnidTasasl = respuestas_automaticas["unidades_llegada"]

    # Validar la opción seleccionada
    if opUnidTasasl in [1, 2, 3]:
        print(f"Se seleccionó automáticamente la opción: {opUnidTasasl}")
    else:
        print(opError)
        exit(opError)

    # Convertir la tasa de llegada según la unidad seleccionada
    if opUnidTasasl == 1:  # Clientes/segundo -> Clientes/minuto
        landa = landa * 60
    elif opUnidTasasl == 3:  # Clientes/hora -> Clientes/minuto
        landa = landa / 60

    elif opPoisson != 1:     # type: ignore # added condition, was else before, which is incorrect based on the comment
        #DISTRIBUCION DE PROBABILIDAD LLEGADA

        print("\n🔸¿Qué distribución de probabilidad sigue el tiempo promedio entre llegadas?🤔")
        print(distribucion)
        while True:
            opdistrLlegada = input("Digite la opción: ")
            if opdistrLlegada:
                if opdistrLlegada.isdigit():
                    opdistrLlegada = int(opdistrLlegada)
                    if opdistrLlegada in [1, 2, 3, 4]: # simplified condition
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)
else:
    
    print("\n🔸¿Qué distribución de probabilidad sigue el tiempo promedio entre llegadas?🤔")
    print(distribucion)
    while True:
        opdistrLlegada=input("Digite la opción: ")
        if opdistrLlegada:
            if opdistrLlegada.isdigit():
                opdistrLlegada=int(opdistrLlegada)
                if opdistrLlegada==1 or opdistrLlegada==2 or opdistrLlegada==3 or opdistrLlegada==4:
                    break
                else: 
                    print(opError)
            else:
                print(errorValor)       
        else:
                print(errorVacio)    
    if opdistrLlegada ==1:
         while True:
            landa=input("Ingrese el tiempo promedio entre llegadas (1/λ): ")
            if landa:
                if landa.replace(".","",1).isdigit():
                    landa=float(landa)
                    landa=1/landa
                    break
                else:
                    print(errorValor)       
            else:
                print(errorVacio) 
         print(unidadesTiempos)
         while True:
            opUnidTiemposl=input("Digite la opción: ")
            if opUnidTiemposl:
                if opUnidTiemposl.isdigit():
                    opUnidTiemposl=int(opUnidTiemposl)
                    if opUnidTiemposl==1 or opUnidTiemposl==2 or opUnidTiemposl==3:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                    print(errorVacio)      
         if opUnidTiemposl==1:
              landa=landa*60
         elif opUnidTiemposl==3:
              landa=landa/60
    else:
         exit(error)

# Mensaje de pregunta inicial para datos de servicio
datosServicio = '''\n🔸Los datos de servicio están en:
     1. Tasa media de servicio
     2. Tiempo promedio de servicio'''
print(datosServicio)

# Asignación automática para datos de servicio
opcionServicio = respuestas_automaticas["datos_servicio"]

# Validar la opción seleccionada automáticamente
if opcionServicio in [1, 2]:
    print(f"Se seleccionó automáticamente la opción: {opcionServicio}")
else:
    print(opError)
    exit(opError)

if opcionServicio == 1:  # Tasa media de servicio
    poissonSer = '''\n🔸¿La tasa media de servicio sigue una distribución de Poisson?🤔
     1. Sí
     2. No'''
    print(poissonSer)

    # Asignación automática para distribución de servicio
    opcion = respuestas_automaticas["distribucion_servicio"]

    # Validar la opción seleccionada automáticamente
    if opcion in [1, 2]:
        print(f"Se seleccionó automáticamente la opción: {opcion}")
    else:
        print(opError)
        exit(opError)

    if opcion == 1:  # Distribución de Poisson
        mu = parametros["mu"][0]  # Tasa media de servicio automática
        print(f"\nSegún el análisis, la tasa media de servicio (μ) es: {mu} {parametros['mu'][1]}")

        print(unidadesTasas)

        # Asignación automática de unidades de la tasa
        opUnidTasass = respuestas_automaticas["unidades_llegada"]

        # Validar la opción seleccionada
        if opUnidTasass in [1, 2, 3]:
            print(f"Se seleccionó automáticamente la opción: {opUnidTasass}")
        else:
            print(opError)
            exit(opError)

        # Convertir la tasa de servicio según la unidad seleccionada
        if opUnidTasass == 1:  # Clientes/segundo -> Clientes/minuto
            mu = mu * 60
        elif opUnidTasass == 3:  # Clientes/hora -> Clientes/minuto
            mu = mu / 60
    else:
        print(error)
        exit(error)

else:  # Tiempo promedio de servicio
    print("\n🔸¿Qué distribución de probabilidad sigue el tiempo promedio de servicio?🤔")
    print(distribucion)

    # Asignación automática para distribución del tiempo de servicio
    opdistrServicio = respuestas_automaticas["distribucion_servicio"]

    # Validar la opción seleccionada automáticamente
    if opdistrServicio in [1, 2, 3, 4]:
        print(f"Se seleccionó automáticamente la opción: {opdistrServicio}")
    else:
        print(opError)
        exit(opError)

    if opdistrServicio == 1:  # Distribución exponencial
        mu = parametros["mu"][0]  # Tiempo promedio de servicio automático
        print(f"\nSegún el análisis, el tiempo promedio de servicio (1/μ) es: {mu} ")
        mu=1/mu
        print(unidadesTiempos)

        # Asignación automática de unidades del tiempo
        opUnidTiemposs = respuestas_automaticas["unidades_servicio"]

        # Validar la opción seleccionada
        if opUnidTiemposs in [1, 2, 3]:
            print(f"Se seleccionó automáticamente la opción: {opUnidTiemposs}")
        else:
            print(opError)
            exit(opError)

        # Convertir el tiempo promedio según la unidad seleccionada
        if opUnidTiemposs == 1:  # Segundos -> Minutos
            mu = mu * 60
        elif opUnidTiemposs == 3:  # Horas -> Minutos
            mu = mu / 60
    else:
        print(error)
        exit(error)

# Supuestos finales
print(f"\nSe cumple con el proceso de nacimiento y muerte, por lo tanto se tienen los siguientes 4 supuestos: \n{supuestos4}")

# Recuperar el número de servidores de los parámetros
s = parametros.get("num_servidores", None)

# Validar el número de servidores desde los parámetros
if s is None or not isinstance(s, int) or s < 1:
    print("No se encontró un valor válido en los parámetros. Solicitaré el valor manualmente.")
    while True:
        s = input("\nIngrese el número de servidores: ")
        if s:
            if s.isdigit():
                s = int(s)
                if s >= 1:
                    break
                else:
                    print("El número de servidores debe ser al menos 1.")
            else:
                print("Error: Debe ingresar un número entero válido.")
        else:
            print("Error: No puede dejar el campo vacío.")
else:
    print(f"El número de servidores se seleccionó automáticamente como: {s}")

# Salida final del número de servidores
print(f"Número de servidores configurado: {s}")


print(f"\n     Supuesto 5. s = {s}")
if s == 1:
    print("\nDe acuerdo a los datos suministrados hasta el momento, es posible obtener una solución y podemos estar ante el modelo M/M/1 o M/M/1/K ✔️ \n \nMás adelante se preguntará por la disciplina de la cola \n \nPero por ahora, !Continuemos!🫡")
else:
    print("\nDe acuerdo a los datos suministrados hasta el momento, es posible obtener una solución y podemos estar ante el modelo M/M/s o M/M/s/K ✔ \n \nMás adelante se preguntará por la disciplina de la cola \n \nPero por ahora !Continuemos!🫡")

# Asignación automática para la capacidad del sistema
opCapacidad = 1 if parametros["capacidad_sistema"] != float('inf') else 2

# Validar la opción de capacidad asignada automáticamente
if opCapacidad in [1, 2]:
    print(f"El sistema tiene capacidad seleccionada automáticamente como: {'Finita' if opCapacidad == 1 else 'Infinita'}")
else:
    print("Error: no se pudo determinar la capacidad automáticamente.")
    capacidad = '''\n🔸El sistema tiene capacidad:
         1. Finita
         2. Infinita'''
    print(capacidad)
    while True:
        opCapacidad = input("Digite la opción: ")
        if opCapacidad:
            if opCapacidad.isdigit():
                opCapacidad = int(opCapacidad)
                if opCapacidad in [1, 2]:
                    break
                else:
                    print(opError)
            else:
                print(errorValor)
        else:
            print(errorVacio)

# Procesar el valor de K si la capacidad es finita
if opCapacidad == 1:
    # Asignar automáticamente la capacidad del sistema desde parámetros
    k = parametros.get("capacidad_sistema", None)

    # Validar K, solicitarlo manualmente si no es válido
    if k is None or not isinstance(k, int) or k < 1:
        print("No se encontró un valor válido para K en los parámetros. Solicitaré el valor manualmente.")
        while True:
            k = input("\nIngrese la capacidad del sistema (K): ")
            if k:
                if k.isdigit():
                    k = int(k)
                    break
                else:
                    print(errorValor)
            else:
                print(errorVacio)
    else:
        print(f"La capacidad del sistema (K) se seleccionó automáticamente como: {k}")

    # Determinar y mostrar los supuestos en base a K y el número de servidores
    if s == 1:
        print(f"\n     Supuesto 6. El sistema es de capacidad finita, con K = {k}\n"
              f"     Supuesto 7. La tasa media de llegadas depende del número de clientes en el sistema.")
    else:
        print(f"\n     Supuesto 6. El sistema es de capacidad finita, con K = {k}\n"
              f"     Supuesto 7. La tasa media de llegadas depende del número de clientes en el sistema.\n"
              f"     Supuesto 8. La tasa media de servicio depende del número de clientes en el sistema.")
else:
    print("\n     Supuesto 6. El sistema es de capacidad infinita.")


if opCapacidad == 2:
    # Calcular el valor de ρ
    ro1 = landa / (mu * s)

    # Validar si el sistema cumple con los supuestos de estabilidad
    if ro1 >= 1:
        if s != 1:
            print("\n     Supuesto 6. La tasa media de llegadas no depende del número de clientes en el sistema.\n"
                  "     Supuesto 7. La tasa media de servicio depende del número de clientes en el sistema.\n"
                  "     ¡Error! No se cumple con el supuesto 8. ρ<1.\n"
                  "     Vuelva a intentarlo.")
        else:
            print("\n     Supuesto 6. La tasa media de llegadas no depende del número de clientes en el sistema.\n"
                  "     ¡Error! No se cumple con el supuesto 7 de ρ<1. Por lo tanto el ejercicio no se puede resolver, "
                  "ya que el sistema no alcanzará la condición de estado estable.\n\n     Vuelva a intentarlo.")
        time.sleep(3)
        exit()
    else:
        # Determinación automática de la población
        poblacion_op = 1 if parametros.get("poblacion_tamano", float('inf')) != float('inf') else 2

        if poblacion_op not in [1, 2]:
            print("Error al determinar automáticamente el tamaño de la población. Solicitaré el valor manualmente.")
            poblacion = '''\n🔸El tamaño de la población es:
            1. Finita
            2. Infinita'''
            print(poblacion)
            while True:
                poblacion_op = input("Digite la opción: ")
                if poblacion_op and poblacion_op.isdigit() and int(poblacion_op) in [1, 2]:
                    poblacion_op = int(poblacion_op)
                    break
                else:
                    print("\nError⚠️ \nOpción inválida. Vuelva a intentarlo")

        # Procesar según el tamaño de la población
        if poblacion_op == 1:
            # Obtener el tamaño de la población automáticamente o solicitarlo
            p = parametros.get("poblacion_tamano", None)
            if not isinstance(p, int) or p < 1:
                print("No se encontró un valor válido para la población finita. Solicitaré el valor manualmente.")
                while True:
                    p = input("\nIngrese el tamaño de la población (N): ")
                    if p.isdigit():
                        p = int(p)
                        break
                    else:
                        print("\nError⚠️ \nValor inválido. Vuelva a intentarlo.")

            print(f"\n    Supuesto. El sistema tiene población finita con N = {p}.")
            print("\nEste modelo cumple con el proceso nacimiento y muerte, pero no está programado en este software.\n")
            time.sleep(3)
            exit()
        else:
            if s == 1:
                print("\n     Supuesto 6. La tasa media de llegadas no depende del número de clientes en el sistema.\n"
                      "     Supuesto 7. ρ<1.")
            else:
                print("\n     Supuesto 6. La tasa media de llegadas no depende del número de clientes en el sistema.\n"
                      "     Supuesto 7. La tasa media de servicio depende del número de clientes en el sistema.\n"
                      "     Supuesto 8. ρ<1.")

# Pregunta sobre la disciplina de la cola
print(pw)

# Selección automática o manual de la disciplina de la cola
disciplina = parametros.get("disciplina_cola", 5)  # Asumir 5 si no se especifica

# Si no se especifica disciplina, se asigna 5
if disciplina not in [1, 2, 3, 4]:
    
    disciplina = 5  # Valor predeterminado

# Determinación de los supuestos en función de la disciplina y el número de servidores
if disciplina == 1:
    print(f"\n Supuesto {'8' if s == 1 else '9'}. La disciplina de la cola es FIFO.")
elif disciplina == 2:
    print(f"\n Supuesto {'8' if s == 1 else '9'}. La disciplina de la cola es LIFO.")
elif disciplina == 3:
    print(f"\n Supuesto {'8' if s == 1 else '9'}. La disciplina de la cola es SIRO.")
elif disciplina == 4:
    print(f"\n Supuesto {'8' if s == 1 else '9'}. La disciplina de la cola es Disciplina General.")

# Determinación del modelo y los supuestos según las condiciones
# Los valores de `opCapacidad`, `s`, `k` y `supuestos4` se deben definir previamente en el código
if opCapacidad == 1 and s == 1:
    print("\n¡Enhorabuena!\nEl modelo que se adecua a estos supuestos es el Modelo M/M/1/K ✅")
    print("Los supuestos de este modelo son:")
    print(supuestos4)  # Supuestos 1 a 4 comunes
    print(f"    Supuesto 5. s = {s}")
    print(f"    Supuesto 6. El sistema es de capacidad finita, con K = {k}")
    print("    Supuesto 7. La tasa media de llegadas depende del número de clientes en el sistema.")
    if disciplina == 1:
        print("    Supuesto 8. La disciplina de la cola es FIFO.")
    elif disciplina == 2:
        print("    Supuesto 8. La disciplina de la cola es LIFO.")
    elif disciplina == 3:
        print("    Supuesto 8. La disciplina de la cola es SIRO.")
    elif disciplina == 4:
        print("    Supuesto 8. La disciplina de la cola es Disciplina General.")

elif opCapacidad == 1 and s != 1:
    print("\n¡Enhorabuena!\nEl modelo que se adecua a estos supuestos es el Modelo M/M/s/K ✅")
    print("Los supuestos de este modelo son:")
    print(supuestos4)  # Supuestos 1 a 4 comunes
    print(f"    Supuesto 5. s = {s}")
    print(f"    Supuesto 6. El sistema es de capacidad finita, con K = {k}")
    print("    Supuesto 7. La tasa media de llegadas depende del número de clientes en el sistema.")
    print("    Supuesto 8. La tasa media de servicio depende del número de clientes en el sistema.")
    if disciplina == 1:
        print("    Supuesto 9. La disciplina de la cola es FIFO.")
    elif disciplina == 2:
        print("    Supuesto 9. La disciplina de la cola es LIFO.")
    elif disciplina == 3:
        print("    Supuesto 9. La disciplina de la cola es SIRO.")
    elif disciplina == 4:
        print("    Supuesto 9. La disciplina de la cola es Disciplina General.")

elif opCapacidad == 2 and s == 1:
    print("\n¡Enhorabuena!\nEl modelo que se adecua a estos supuestos es el Modelo M/M/1 ✅")
    print("Los supuestos de este modelo son:")
    print(supuestos4)  # Supuestos 1 a 4 comunes
    print(f"    Supuesto 5. s = {s}")
    print("    Supuesto 6. La tasa media de llegadas no depende del número de clientes en el sistema.")
    print("    Supuesto 7. ρ<1.")
    if disciplina == 1:
        print("    Supuesto 8. La disciplina de la cola es FIFO.")
    elif disciplina == 2:
        print("    Supuesto 8. La disciplina de la cola es LIFO.")
    elif disciplina == 3:
        print("    Supuesto 8. La disciplina de la cola es SIRO.")
    elif disciplina == 4:
        print("    Supuesto 8. La disciplina de la cola es Disciplina General.")

elif opCapacidad == 2 and s != 1:
    print("\n¡Enhorabuena!\nEl modelo que se adecua a estos supuestos es el Modelo M/M/s ✅")
    print("Los supuestos de este modelo son:")
    print(supuestos4)  # Supuestos 1 a 4 comunes
    print(f"    Supuesto 5. s = {s}")
    print("    Supuesto 6. La tasa media de llegadas no depende del número de clientes en el sistema.")
    print("    Supuesto 7. La tasa media de servicio depende del número de clientes en el sistema.")
    print("    Supuesto 8. ρ<1.")
    if disciplina == 1:
        print("    Supuesto 9. La disciplina de la cola es FIFO.")
    elif disciplina == 2:
        print("    Supuesto 9. La disciplina de la cola es LIFO.")
    elif disciplina == 3:
        print("    Supuesto 9. La disciplina de la cola es SIRO.")
    elif disciplina == 4:
        print("    Supuesto 9. La disciplina de la cola es Disciplina General.")


if opCapacidad==2 and s==1:            #CALCULOS MM1  
    print(calculo)
    while True:
        opCalculo=input("Digite la opción: ")
        if opCalculo:
            if opCalculo.isdigit():
                opCalculo=int(opCalculo)
                if opCalculo==1 or opCalculo==2 or opCalculo==3 or opCalculo==4:
                    break
                else: 
                    print(opError)
            else:
                print(errorValor)       
        else:
            print(errorVacio)  
    if opCalculo==1:
            medDesempeñoMM1(landa,mu)
    if opCalculo==2:
            while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)  
            print(calculoPn)
            while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            probabilidadMM1(tipodeCalculoPn,n)
    if opCalculo==3:  
        if disciplina != 1:
            print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
        else:        
            while True:
                t = input("\nDigite el tiempo: ")
                if t:
                    if t.replace(".", "", 1).isdigit():
                        t = float(t)
                        break
                    else:
                        print(errorValor)
                else:
                    print(errorVacio)
            
            print(unidadesTiempos)
            while True:
                opUnidTiempost = input("Digite la opción: ")
                if opUnidTiempost:
                    if opUnidTiempost.isdigit():
                        opUnidTiempost = int(opUnidTiempost)
                        if opUnidTiempost in [1, 2, 3]:
                            break
                        else:
                            print(opError)
                    else:
                        print(errorValor)
                else:
                    print(errorVacio)
            
            # Convertimos el tiempo según la opción seleccionada
            if opUnidTiempost == 1:
                t = t / 60
            elif opUnidTiempost == 3:
                t = t * 60
            
            ro = landa / mu
            from math import e
            calculoPw = e ** (-mu * (1 - ro) * t)
            print(f"\nLa probabilidad de esperar en el sistema un tiempo mayor a {t} es P(W>t): {calculoPw}")

    if opCalculo==4:  
            if disciplina != 1:
                print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
            else:

                while True:
                    t=input("\nDigite el tiempo: ")
                    if t:
                        if t.replace(".","",1).isdigit():
                            t=float(t)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)   
                print(unidadesTiempos)
                while True:
                    opUnidTiempost=input("Digite la opción: ")
                    if opUnidTiempost:
                        if opUnidTiempost.isdigit():
                            opUnidTiempost=int(opUnidTiempost)
                            if opUnidTiempost==1 or opUnidTiempost==2 or opUnidTiempost==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                if opUnidTiempost==1:
                    t=t/60
                elif opUnidTiempost==3:
                    t=t*60
                if t!=0:
                     ro=landa/mu
                     from math import e
                     calculoPwq=(e**(-mu*(1-ro)*(t)))*(ro)
                else: 
                    ro=landa/mu
                    calculoPwq=1-ro   
                print(f"La probabilidad de esperar en la cola un tiempo mayor a {t} es P(Wq>t): {calculoPwq}")       
  
if opCapacidad==2 and s!=1:             #CALCULOS MMS
        print(calculo)
        while True:
            opCalculo=input("Digite la opción: ")
            if opCalculo:
                if opCalculo.isdigit():
                    opCalculo=int(opCalculo)
                    if opCalculo==1 or opCalculo==2 or opCalculo==3 or opCalculo==4:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)
        if opCalculo==1:
            medDesempeñoMMs(landa,mu,s)
        if opCalculo==2:
            while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)  
            print(calculoPn)
            while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            probabilidadMMs(tipodeCalculoPn,n,s,landa,mu)
        if opCalculo==3:
            if disciplina != 1:
                print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
            else:  
                while True:
                    t=input("\nDigite el tiempo: ")
                    if t:
                        if t.replace(".","",1).isdigit():
                            t=float(t)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio) 
                print(unidadesTiempos)
                while True:
                    opUnidTiempost=input("Digite la opción: ")
                    if opUnidTiempost:
                        if opUnidTiempost.isdigit():
                            opUnidTiempost=int(opUnidTiempost)
                            if opUnidTiempost==1 or opUnidTiempost==2 or opUnidTiempost==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                if opUnidTiempost==1:
                    t=t/60
                elif opUnidTiempost==3:
                    t=t*60
                ro=landa/mu
                sumatoria=0
                for n in range (0,s):
                    sumatoria +=(((landa/mu)**n)/(factorial(n)))
                denominador=sumatoria+((((landa/mu)**s)/(factorial(s)))*(1/(1-(ro1))))
                P0=1/denominador
                a=(s-1-ro)
                import math
                if a==0:
                     calculoPw=((e**(-mu*t))*((1+(P0*(ro**s)))/((factorial(s)*(1-ro1))))*(mu*t))
                else:
                    calculoPw = math.exp(-mu * t) * (1 + P0 * ((landa / mu) ** s) / (factorial(s) * (1 - ro1)) * ((1 - math.exp(-mu * t * (s - 1 - landa / mu))) / (s - 1 - landa / mu)))
                print(f"\nLa probabilidad de esperar en el sistema un tiempo mayor a {t} es P(W>t): {calculoPw}")   
        if opCalculo==4:  
            if disciplina != 1:
                print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
            else:  
                while True:
                    t=input("\nDigite el tiempo: ")
                    if t:
                        if t.replace(".","",1).isdigit():
                            t=float(t)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio) 
                print(unidadesTiempos)
                while True:
                    opUnidTiempost=input("Digite la opción: ")
                    if opUnidTiempost:
                        if opUnidTiempost.isdigit():
                            opUnidTiempost=int(opUnidTiempost)
                            if opUnidTiempost==1 or opUnidTiempost==2 or opUnidTiempost==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                if opUnidTiempost==1:
                    t=t/60
                elif opUnidTiempost==3:
                    t=t*60
                ro=landa/mu
                sumatoria=0
                for n in range (0,s):
                      sumatoria +=(((landa/mu)**n)/(factorial(n)))
                denominador=sumatoria+((((landa/mu)**s)/(factorial(s)))*(1/(1-(ro1))))
                P0=1/denominador
                from math import e
                wq0=1-(((ro**s)/(factorial(s)*(1-ro1)))*P0)
                if t==0:
                    calculoPwq=wq0
                else:
                    calculoPwq=(1-wq0)*(e**(-s*mu*(1-ro1)*t))    
                print(f"La probabilidad de esperar en la cola un tiempo mayor a {t} es P(Wq>t): {calculoPwq}") 
           
if opCapacidad==1 and s==1:          #CALCULOS MM1K
    print(calculok)
    while True:
        opCalculo=input("Digite la opción: ")
        if opCalculo:
            if opCalculo.isdigit():
                opCalculo=int(opCalculo)
                if opCalculo==1 or opCalculo==2:
                    break
                else: 
                    print(opError)
            else:
                print(errorValor)       
        else:
            print(errorVacio)
    if opCalculo==1:
        ro=landa/mu
        print(f"\nEl factor de utilización del sistema es (ρ): {ro:.5f}")
        if ro==1:
            medDesempeñoMM1K1(landa,k)
        if ro!=1:
            medDesempeñoMM1K2(landa,k,ro)  
    if opCalculo==2:
        ro=landa/mu
        if ro==1:
            while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            print(calculoPn)
            while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            probabilidadMM1K1(tipodeCalculoPn,k,n)
        if ro!=1:
            while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            print(calculoPn)
            while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            probabilidadMM1K2(tipodeCalculoPn,k,n)
           
if opCapacidad ==1 and s!=1:          #CALCULOS MMSK
    print(calculok)
    while True:
        opCalculo=input("Digite la opción: ")
        if opCalculo:
            if opCalculo.isdigit():
                opCalculo=int(opCalculo)
                if opCalculo==1 or opCalculo==2:
                    break
                else: 
                    print(opError)
            else:
                print(errorValor)       
        else:
            print(errorVacio)
    if opCalculo==1:
        ro=landa/(mu*s)
        print(f"\nEl factor de utilización del sistema es (ρ): {ro:.5f}")
        if ro==1:
                medDesempeñoMMsK1(landa,mu,s,k)
        if ro!=1:
                medDesempeñoMMsK2(landa,ro,mu,s,k)  
    if opCalculo==2:
        ro=landa/(mu*s)
        if ro==1:
            sumatoria1=0 
            for n in range (0,s):
                sumatoria1 +=(((landa/mu)**n)/factorial(n))
            P0=1/(sumatoria1+(((landa/mu)**s)/factorial(s))*(k-s+1))
            while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            print(calculoPn)
            while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            probabilidadMMsK(tipodeCalculoPn,landa,n,k,s,P0)
        if ro!=1:
            sumatoria1=0
            for n in range (0,(s+1)):
                sumatoria1 +=(((landa/mu)**n)/factorial(n))
            sumatoria2=0
            for n in range(s+1,k+1):
                sumatoria2 +=((landa/(s*mu))**(n-s))
            P0=1/(sumatoria1+(((landa/mu)**s/factorial(s))*sumatoria2)) 
            while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            print(calculoPn)
            while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
            probabilidadMMsK(tipodeCalculoPn,landa,n,k,s,P0)
   
#Repeticion 
print(calculo2)
while True:
    opCalculo2=input("Digite la opción: ")
    if opCalculo2:
        if opCalculo2.isdigit():
            opCalculo2=int(opCalculo2)
            if opCalculo2==1 or opCalculo2==2:
                break
            else: 
                print(opError)
        else:
            print(errorValor)       
    else:
        print(errorVacio)
if opCapacidad==2 and s==1 and opCalculo2==2:
    while True:
        print(fin)
        time.sleep(5)
        exit()
if opCapacidad==2 and s!=1 and opCalculo2==2:
    while True:
        print(fin)
        time.sleep(5)
        exit()
if opCapacidad==1 and s==1 and opCalculo2==2:
    while True:
        print(fin)
        time.sleep(5)
        exit()
if opCapacidad==1 and s!=1 and opCalculo2==2:
    while True:
        print(fin)
        time.sleep(5)
        exit()
if opCapacidad==2 and s==1 and opCalculo2==1:            #CALCULOS MM1  
    while True:
        print(calculo)
        while True:
            opCalculo=input("Digite la opción: ")
            if opCalculo:
                if opCalculo.isdigit():
                    opCalculo=int(opCalculo)
                    if opCalculo==1 or opCalculo==2 or opCalculo==3 or opCalculo==4:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)  
        if opCalculo==1:
             medDesempeñoMM1(landa,mu)
        if opCalculo==2:
             while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)  
             print(calculoPn)
             while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
             probabilidadMM1(tipodeCalculoPn,n)
        if opCalculo==3:  
                if disciplina != 1:
                    print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
                else:

                 while True:
                    t=input("\nDigite el tiempo: ")
                    if t:
                        if t.replace(".","",1).isdigit():
                            t=float(t)
                            break
                        else:
                            print(errorValor)       
                    else:
                         print(errorVacio)
                 print(unidadesTiempos)
                 while True:
                    opUnidTiempost=input("Digite la opción: ")
                    if opUnidTiempost:
                        if opUnidTiempost.isdigit():
                            opUnidTiempost=int(opUnidTiempost)
                            if opUnidTiempost==1 or opUnidTiempost==2 or opUnidTiempost==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 if opUnidTiempost==1:
                     t=t/60
                 elif opUnidTiempost==3:
                     t=t*60
                 ro=landa/mu
                 from math import e
                 calculoPw=e**(-mu*(1-ro)*(t))
                 print(f"\nLa probabilidad de esperar en el sistema un tiempo mayor a {t} es P(W>t): {calculoPw}")   
        if opCalculo==4:
                if disciplina != 1:
                    print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
                else:

                 while True:
                    t=input("\nDigite el tiempo: ")
                    if t:
                        if t.replace(".","",1).isdigit():
                            t=float(t)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)   
                 print(unidadesTiempos)
                 while True:
                    opUnidTiempost=input("Digite la opción: ")
                    if opUnidTiempost:
                        if opUnidTiempost.isdigit():
                            opUnidTiempost=int(opUnidTiempost)
                            if opUnidTiempost==1 or opUnidTiempost==2 or opUnidTiempost==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 if opUnidTiempost==1:
                     t=t/60
                 elif opUnidTiempost==3:
                     t=t*60
                 if t!=0:
                    ro=landa/mu
                    from math import e
                    calculoPwq=(e**(-mu*(1-ro)*(t)))*(ro)
                 else: 
                    ro=landa/mu
                    calculoPwq=1-ro   
                 print(f"La probabilidad de esperar en la cola un tiempo mayor a {t} es P(Wq>t): {calculoPwq}")

        print(calculo2)        
        while True:
            opCalculo2=input("Digite la opción: ")
            if opCalculo2:
                if opCalculo2.isdigit():
                    opCalculo2=int(opCalculo2)
                    if opCalculo2==1 or opCalculo2==2:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)   
        if opCalculo2==2:
             print(fin)
             time.sleep(5)
             exit()
if opCapacidad==2 and s!=1 and opCalculo2==1:             #CALCULOS MMS
    while True: 
         print(calculo)
         while True:
            opCalculo=input("Digite la opción: ")
            if opCalculo:
                if opCalculo.isdigit():
                    opCalculo=int(opCalculo)
                    if opCalculo==1 or opCalculo==2 or opCalculo==3 or opCalculo==4:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)
         if opCalculo==1:
             medDesempeñoMMs(landa,mu,s)
         if opCalculo==2:
             while True:
                n=input("\nIngrese el número de clientes en el sistema (n): ")
                if n:
                    if n.isdigit():
                        n=int(n)
                        break
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)  
             print(calculoPn)
             while True:
                tipodeCalculoPn=input("Digite la opción: ")
                if tipodeCalculoPn:
                    if tipodeCalculoPn.isdigit():
                        tipodeCalculoPn=int(tipodeCalculoPn)
                        if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                            break
                        else: 
                            print(opError)
                    else:
                        print(errorValor)       
                else:
                    print(errorVacio)
             probabilidadMMs(tipodeCalculoPn,n,s,landa,mu)
         if opCalculo==3:
            if disciplina != 1:
                print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
            else:  
                 while True:
                    t=input("\nDigite el tiempo: ")
                    if t:
                        if t.replace(".","",1).isdigit():
                            t=float(t)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio) 
                 print(unidadesTiempos)
                 while True:
                    opUnidTiempost=input("Digite la opción: ")
                    if opUnidTiempost:
                        if opUnidTiempost.isdigit():
                            opUnidTiempost=int(opUnidTiempost)
                            if opUnidTiempost==1 or opUnidTiempost==2 or opUnidTiempost==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 if opUnidTiempost==1:
                     t=t/60
                 elif opUnidTiempost==3:
                     t=t*60
                 ro=landa/mu
                 sumatoria=0
                 for n in range (0,s):
                    sumatoria +=(((landa/mu)**n)/(factorial(n)))
                 denominador=sumatoria+((((landa/mu)**s)/(factorial(s)))*(1/(1-(ro1))))
                 P0=1/denominador
                 a=(s-1-ro)
                 from math import e
                 if a==0:
                    calculoPw=((e**(-mu*t))*((1+(P0*(ro**s)))/((factorial(s)*(1-ro1))))*(mu*t))
                 else:
                    calculoPw=((e**(-mu*t))*((1+(P0*(ro**s)))/((factorial(s)*(1-ro1))))*((1-e**(-mu*t*a))/(a)))  
     
                 print(f"\nLa probabilidad de esperar en el sistema un tiempo mayor a {t} es P(W>t): {calculoPw}")   

         if opCalculo==4:
            if disciplina != 1:
                print("\n ¡Error! No se puede calcular porque la disciplina de la cola no es FIFO.")
            else:  
                 while True:
                    t=input("\nDigite el tiempo: ")
                    if t:
                        if t.replace(".","",1).isdigit():
                            t=float(t)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio) 
                 print(unidadesTiempos)
                 while True:
                    opUnidTiempost=input("Digite la opción: ")
                    if opUnidTiempost:
                        if opUnidTiempost.isdigit():
                            opUnidTiempost=int(opUnidTiempost)
                            if opUnidTiempost==1 or opUnidTiempost==2 or opUnidTiempost==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 if opUnidTiempost==1:
                     t=t/60
                 elif opUnidTiempost==3:
                     t=t*60
                 ro=landa/mu
                 sumatoria=0
                 for n in range (0,s):
                    sumatoria +=(((landa/mu)**n)/(factorial(n)))
                 denominador=sumatoria+((((landa/mu)**s)/(factorial(s)))*(1/(1-(ro1))))
                 P0=1/denominador
                 from math import e
                 wq0=1-(((ro**s)/(factorial(s)*(1-ro1)))*P0)
                 if t==0:
                     calculoPwq=wq0
                 else:
                     calculoPwq=(1-wq0)*(e**(-s*mu*(1-ro1)*t))    
                 print(f"La probabilidad de esperar en la cola un tiempo mayor a {t} es P(Wq>t): {calculoPwq}")
           
         print(calculo2)         
         while True:
            opCalculo2=input("Digite la opción: ")
            if opCalculo2:
                if opCalculo2.isdigit():
                    opCalculo2=int(opCalculo2)
                    if opCalculo2==1 or opCalculo2==2:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)      
         if opCalculo2==2:
             print(fin)
             time.sleep(5)
             exit()
if opCapacidad==1 and s==1 and opCalculo2==1:          #CALCULOS MM1K
    while True:
         print(calculok)
         while True:
            opCalculo=input("Digite la opción: ")
            if opCalculo:
                if opCalculo.isdigit():
                    opCalculo=int(opCalculo)
                    if opCalculo==1 or opCalculo==2:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)
         if opCalculo==1:
             ro=landa/mu
             print(f"\nEl factor de utilización del sistema es (ρ): {ro:.5f}")
             if ro==1:
                 medDesempeñoMM1K1(landa,k)
             if ro!=1:
                 medDesempeñoMM1K2(landa,k,ro)  
         if opCalculo==2:
             ro=landa/mu
             if ro==1:
                 while True:
                    n=input("\nIngrese el número de clientes en el sistema (n): ")
                    if n:
                        if n.isdigit():
                            n=int(n)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 print(calculoPn)
                 while True:
                    tipodeCalculoPn=input("Digite la opción: ")
                    if tipodeCalculoPn:
                        if tipodeCalculoPn.isdigit():
                            tipodeCalculoPn=int(tipodeCalculoPn)
                            if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 probabilidadMM1K1(tipodeCalculoPn,k,n)
             if ro!=1:
                 while True:
                    n=input("\nIngrese el número de clientes en el sistema (n): ")
                    if n:
                        if n.isdigit():
                            n=int(n)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 print(calculoPn)
                 while True:
                    tipodeCalculoPn=input("Digite la opción: ")
                    if tipodeCalculoPn:
                        if tipodeCalculoPn.isdigit():
                            tipodeCalculoPn=int(tipodeCalculoPn)
                            if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 probabilidadMM1K2(tipodeCalculoPn,k,n)
         
         print(calculo2)         
         while True:
            opCalculo2=input("Digite la opción: ")
            if opCalculo2:
                if opCalculo2.isdigit():
                    opCalculo2=int(opCalculo2)
                    if opCalculo2==1 or opCalculo2==2:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)      
         if opCalculo2==2:
             print(fin)
             time.sleep(5)
             exit()             
if opCapacidad ==1 and s!=1 and opCalculo2:          #CALCULOS MMSK
    while True:
         print(calculok)
         while True:
            opCalculo=input("Digite la opción: ")
            if opCalculo:
                if opCalculo.isdigit():
                    opCalculo=int(opCalculo)
                    if opCalculo==1 or opCalculo==2:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)
         if opCalculo==1:
             ro=landa/(mu*s)
             print(f"\nEl factor de utilización del sistema es (ρ): {ro:.5f}")
             if ro==1:
                medDesempeñoMMsK1(landa,mu,s,k)
             if ro!=1:
                medDesempeñoMMsK2(landa,ro,mu,s,k)  
         if opCalculo==2:
             ro=landa/(mu*s)
             if ro==1:
                 sumatoria1=0 
                 for n in range (0,s):
                     sumatoria1 +=(((landa/mu)**n)/factorial(n))
                 P0=1/(sumatoria1+(((landa/mu)**s)/factorial(s))*(k-s+1))
                 while True:
                    n=input("\nIngrese el número de clientes en el sistema (n): ")
                    if n:
                        if n.isdigit():
                            n=int(n)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 print(calculoPn)
                 while True:
                    tipodeCalculoPn=input("Digite la opción: ")
                    if tipodeCalculoPn:
                        if tipodeCalculoPn.isdigit():
                            tipodeCalculoPn=int(tipodeCalculoPn)
                            if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 probabilidadMMsK(tipodeCalculoPn,landa,n,k,s,P0)
             if ro!=1:
                 sumatoria1=0
                 for n in range (0,(s+1)):
                     sumatoria1 +=(((landa/mu)**n)/factorial(n))
                 sumatoria2=0
                 for n in range(s+1,k+1):
                     sumatoria2 +=((landa/(s*mu))**(n-s))
                 P0=1/(sumatoria1+(((landa/mu)**s/factorial(s))*sumatoria2)) 
                 while True:
                    n=input("\nIngrese el número de clientes en el sistema (n): ")
                    if n:
                        if n.isdigit():
                            n=int(n)
                            break
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 print(calculoPn)
                 while True:
                    tipodeCalculoPn=input("Digite la opción: ")
                    if tipodeCalculoPn:
                        if tipodeCalculoPn.isdigit():
                            tipodeCalculoPn=int(tipodeCalculoPn)
                            if tipodeCalculoPn==1 or tipodeCalculoPn==2 or tipodeCalculoPn==3:
                                break
                            else: 
                                print(opError)
                        else:
                            print(errorValor)       
                    else:
                        print(errorVacio)
                 probabilidadMMsK(tipodeCalculoPn,landa,n,k,s,P0)
         
         print(calculo2)
         while True:
            opCalculo2=input("Digite la opción: ")
            if opCalculo2:
                if opCalculo2.isdigit():
                    opCalculo2=int(opCalculo2)
                    if opCalculo2==1 or opCalculo2==2:
                        break
                    else: 
                        print(opError)
                else:
                    print(errorValor)       
            else:
                print(errorVacio)      
         if opCalculo2==2:
             print(fin)
             time.sleep(5)
             exit()    

if opCapacidad==1 and s==1 and opCalculo==2:
             print(fin)
             time.sleep(5)
             exit()


def main():
    pass


if __name__ == "__main__":
    main()