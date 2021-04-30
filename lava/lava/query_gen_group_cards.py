import json
from datetime import datetime

txt_root = 'INSERT INTO tarjetas(equipos_partidos_id,partidos_id, jugador_id,tipo) VALUES\n '
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
    tarjetas_local =match['tarjetas_locales']
    tipo_de_tarjeta_local = match['tipo_de_tarjeta_local']
    equipo_local = match['nombre_local']
    local = 'local'

    if len(tarjetas_local)>0:
        for i in range(len(tarjetas_local)):
            tarjeta=tarjetas_local[i].replace(' ','%')
            print(tarjeta)
            arbitro = arbitro.replace(' ','%')
            if tipo_de_tarjeta_local[i].find("yellow"):
                txt = f'''((SELECT id FROM equipos_partidos WHERE partido_id = (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1) AND local_o_visitante = 'local'),
                (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1),
                (SELECT id FROM jugadores WHERE nombre LIKE "%{tarjeta}%" LIMIT 1),
                "amarilla"),'''
                txt_root += txt
            else:
                txt = f'''((SELECT id FROM equipos_partidos WHERE partido_id = (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1) AND local_o_visitante = 'local'),
                (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1),
                (SELECT id FROM jugadores WHERE nombre LIKE "%{tarjeta}%" LIMIT 1),
                "roja"),'''
                txt_root += txt

    tarjetas_visitante = match['tarjetas_visitantes']
    tipo_de_tarjeta_visitantes = match['tipo_de_tarjeta_visitantes']
    equipo_visitante = match['nombre_visitante']
    visitante = 'visitante'

    if len(tarjetas_visitante)>0:
        for i in range(len(tarjetas_visitante)):
            tarjeta=tarjetas_visitante[i].replace(' ','%')
            print(tarjeta)
            arbitro = arbitro.replace(' ','%')
            if tipo_de_tarjeta_visitantes[i].find("yellow"):
                txt = f'''((SELECT id FROM equipos_partidos WHERE partido_id = (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1) AND local_o_visitante = 'visitante'),
                (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1),
                (SELECT id FROM jugadores WHERE nombre LIKE "%{tarjeta}%" LIMIT 1),
                "amarilla"),'''
                txt_root += txt
            else:
                txt = f'''((SELECT id FROM equipos_partidos WHERE partido_id = (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1) AND local_o_visitante = 'visitante'),
                (SELECT id FROM partidos WHERE arbitro_id = (SELECT id FROM arbitros WHERE nombre LIKE "%{arbitro}%" LIMIT 1) AND
                fase_id = (SELECT id FROM fase WHERE tipo_fase = "{fase}" LIMIT 1) AND fecha_y_hora_partido = "{fecha}" LIMIT 1),
                (SELECT id FROM jugadores WHERE nombre LIKE "%{tarjeta}%" LIMIT 1),
                "roja"),'''
                txt_root += txt

print(txt_root)
