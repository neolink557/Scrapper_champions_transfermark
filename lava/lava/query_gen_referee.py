import json
from datetime import datetime
from google_trans_new import google_translator

translator = google_translator()


txt_root = 'INSERT INTO arbitros (CODIGO_ISO, fecha_nacimiento,	nombre) VALUES\n '
with open('E:/Users/Braya/Documents/scrapy_platzi/lava/final_referee.json', encoding='utf-8') as source:
    json_source = source.read()
    data = json.loads('[{}]'.format(json_source))



for referee in data[0]:
    citizenship = translator.translate(str(referee['referee_citizenship']), lang_tgt='es')
    fecha = referee['referee_birthdate']
    fecha = fecha.strip()
    fecha = datetime.strptime(fecha, '%b %d, %Y')
    fecha = fecha.strftime('%Y-%m-%d %H:%M:%S')
    nombres = referee['referee_name']
    txt = f'((select codigo_iso from pais where nombre = "{citizenship}"),"{fecha}","{nombres}"),\n'
    txt_root += txt

print(txt_root)
