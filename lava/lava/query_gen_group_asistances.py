import json
from datetime import datetime

txt_root = 'INSERT INTO asistencias_goles(jugador_id) VALUES\n '
with open('E:/Users/Braya/Documents/scrapy_platzi/lava/group_matches.json', encoding='utf-8') as source:
    json_source = source.read()
    data = json.loads('[{}]'.format(json_source))



for match in data[0]:
    arbitro = match['arbitro']
    estadio = match['estadio']
    fase = "grupos"
    fecha = match['fecha']+' '+match['hora']
    #fecha = fecha[0:-10]
    fecha = fecha.strip()
    fecha = datetime.strptime(fecha, '%a, %m/%d/%y %I:%M %p')
    fecha = fecha.strftime('%Y-%m-%d %H:%M:%S')

    temporada = '19-20'
    goles_local =match['nombre_goleadores_locales_asistentes']
    equipo_local = match['nombre_local']
    local = 'local'

    if len(goles_local)>1:
        for i in range(len(goles_local)//2):
            asistant= goles_local[1+(i*2)].replace(' ','%')
            txt = f'''((SELECT id FROM jugadores WHERE nombre LIKE "%{asistant}%" LIMIT 1)),\n'''
            txt_root += txt

    goles_visitante =match['nombre_goleadores_visitantes_asistentes']
    equipo_visitante = match['nombre_visitante']
    visitante = 'visitante'
    if len(goles_visitante)>1:
        for i in range(len(goles_visitante)//2):
            arbitro = arbitro.replace(' ','%')
            names = goles_visitante[0+(i*2)].replace(' ','%')
            asistant= goles_visitante[1+(i*2)].replace(' ','%')
            txt = f'''((SELECT id FROM jugadores WHERE nombre LIKE "%{asistant}%" LIMIT 1)),\n'''
            txt_root += txt

print(txt_root)
