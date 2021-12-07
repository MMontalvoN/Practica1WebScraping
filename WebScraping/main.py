# Paso 01: Instalación e importación de las librerías
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Paso 02: Configuración de la web site para el scraping
url = 'https://www.laliga.com/laliga-santander/clasificacion'
page = requests.get(url)
soup = BeautifulSoup(page.content, 'html.parser')

# Paso 03: Extracción de los equipos y posición en la clasificación general
eq = soup.find_all('div', class_ = 'styled__ShieldContainer-lo8ov8-0 bkblFd shield-desktop')
equipos = list()
count = 0
equipos.append('EQUIPO')
for i in eq:
    if count < 20:
        equipos.append(i.text)
    else:
        break
    count += 1

# Paso 04: Extracción de los indicadores de clasificación
pts = soup.find_all('div', class_= 'styled__Td-e89col-10 gETuZs')
puntos = list()
count = 1

for i in pts:
    if count < 169:
        puntos.append(i.text)
    else:
         break
    count += 1

fila = 21
col = 8
M = [puntos[col*i: col*(i+1)] for i in range(fila)]

# Paso 05: Preparación y almacenamiento de los conjuntos de datos (dataset)
## Posición y equipos
de = pd.DataFrame({'Nombre':equipos}, index=list(range(1,22)))

## Indicadores de clasificación
dp = pd.DataFrame(data=M, index=pd.RangeIndex(range(1, 22)), columns=pd.RangeIndex(range(1, 9)))

## Unificación de los dataframes
frames = [de, dp]
result = pd.concat(frames, axis=1, join='inner')

# Paso 06: Exportación del data frames a un cojuntos de datos CSV
result.to_csv('WebScraping_Cladificacion.csv', index=False, header=None)