import json
from datetime import datetime

txt_root = 'INSERT INTO partidos (arbitro_id, estadios_id,fase_id,fecha_y_hora_partido,modalidad_id) VALUES\n '
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
    print(fecha)
    fecha = datetime.strptime(fecha, '%a, %m/%d/%y %I:%M %p')
    fecha = fecha.strftime('%Y-%m-%d %H:%M:%S')
    txt = f'''((select id from arbitros where nombre = "{arbitro}" LIMIT 1),
    (select id from estadios where nombre = "{estadio}"),
    (select id from fase where tipo_fase= "final"),
    "{fecha}",
    (select id from modalidad where tipo_modalidad = "unico")),\n'''
    txt_root += txt

print(txt_root)
