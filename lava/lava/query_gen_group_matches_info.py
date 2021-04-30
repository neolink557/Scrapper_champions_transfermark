import json
from datetime import datetime

txt_root = 'INSERT INTO equipos_partidos(partido_id, temporada_id,equipos_id,local_o_visitante) VALUES\n '
with open('E:/Users/Braya/Documents/scrapy_platzi/lava/final_match.json', encoding='utf-8') as source:
    json_source = source.read()
    data = json.loads('[{}]'.format(json_source))



for match in data[0]:
    arbitro = match['arbitro']
    estadio = match['estadio']
    fase = match['fase']
    fecha = match['fecha']+' '+match['hora']
    #fecha = fecha[0:-10]
    fecha = fecha.strip()
    fecha = datetime.strptime(fecha, '%a, %m/%d/%y %I:%M %p')
    fecha = fecha.strftime('%Y-%m-%d %H:%M:%S')

    temporada = '19-20'
    equipo_local = match['nombre_local']
    local = 'local'

    txt = f'''((select id from partidos where fecha_y_hora_partido = "{fecha}"
     AND arbitro_id = (select id from arbitros where nombre = "{arbitro}" LIMIT 1) LIMIT 1),
    (select id from temporadas where nombre = "{temporada}" LIMIT 1),
    (select id from equipos where nombres= "{equipo_local}" LIMIT 1),
    "{local}"),\n'''
    txt_root += txt

    equipo_visitante = match['nombre_visitante']
    visitante = 'visitante'

    txt = f'''((select id from partidos where fecha_y_hora_partido = "{fecha}"
     AND arbitro_id = (select id from arbitros where nombre = "{arbitro}" LIMIT 1) LIMIT 1),
    (select id from temporadas where nombre = "{temporada}" LIMIT 1),
    (select id from equipos where nombres= "{equipo_visitante}" LIMIT 1),
    "{visitante}"),\n'''
    txt_root += txt

print(txt_root)
