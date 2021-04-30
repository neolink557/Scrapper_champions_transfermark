import scrapy
#xpath
# all 8th 1 matches
# //td[@colspan = 8 and @class ="hauptlink"]/a[contains(.,"last 16 1st leg")]/../../../tr[not(@class)]/td[@class = "zentriert hauptlink"]/a[@title = "Match report"]/@href
#arbitro = //p[@class = "sb-zusatzinfos"]/a/@href
#stadium = //p[@class = "sb-zusatzinfos"]/span/a/text()
#date = //p[@class = "sb-datum hide-for-small"]/a/text()
#hour = //p[@class = "sb-datum hide-for-small"]/text()[2]
#score = //div[@class = "sb-endstand"]/text()[1]
#LOCAL
#name = //div[@class = "sb-team sb-heim"]/a/text()
#goals = //div[@id = "sb-tore"]/ul/li[@class = "sb-aktion-heim"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()
#card owner =  //div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-heim"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()
#card_type = //div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-heim"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/text()
#VISITOR
#name = //div[@class = "sb-team sb-gast"]/a/text()
#goals = //div[@id = "sb-tore"]/ul/li[@class = "sb-aktion-gast"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()
#card owner =  //div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-gast"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()
#card_type = //div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-gast"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/text()
#REFEREE
#name = //div[@class = "spielername-profil"]/text()
#birthdate = //table[@class = "profilheader"]/tbody/tr/td/text()  [0]
#citizenship = //table[@class = "profilheader"]/tbody/tr/td/a[@href]/text() [0]
#arbitro = //p[@class = "sb-zusatzinfos"]/a/text()
class SpiderMatches(scrapy.Spider):
    name = 'matches-8-1'
    start_urls = [
        'https://www.transfermarkt.com/uefa-champions-league/gesamtspielplan/pokalwettbewerb/CL/saison_id/2019'
    ]
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'FEED_URI' : '8-1_matches.json',
        'FEED_FORMAT' : 'json',
        'FEED_EXPORT_ENCODING' : 'utf-8'
    }

    def parse(self, response):
        links_matches = response.xpath('//td[@colspan = 8 and @class ="hauptlink"]/a[contains(.,"last 16 1st leg")]/../../../tr[not(@class)]/td[@class = "zentriert hauptlink"]/a[@title = "Match report"]/@href').getall()
        total_links =len(links_matches)
        for link in links_matches:
            yield response.follow(link,callback = self.parse_link,cb_kwargs ={'links':total_links})

    def parse_link(self,response,**kwargs):
        stadium = response.xpath('//p[@class = "sb-zusatzinfos"]/span/a/text()').get()
        date =  response.xpath('//p[@class = "sb-datum hide-for-small"]/a/text()').get()
        date = date.replace('\n','')
        date = date.replace('|','')
        date = date.strip()
        hour = response.xpath('//p[@class = "sb-datum hide-for-small"]/text()[2]').get()
        hour = hour.replace('\n','')
        hour = hour.replace('|','')
        hour = hour.strip()
        link_referee = response.xpath('//p[@class = "sb-zusatzinfos"]/a/@href').get()
        arbitro = response.xpath('//p[@class = "sb-zusatzinfos"]/a/text()').get()

        score = response.xpath('//div[@class = "sb-endstand"]/text()[1]').getall()[0]
        score = score.strip()
        score = score.replace(" ",'')
        score = score.replace("\n",'')
        score = score.split(':')

        #local
        name_local = response.xpath('//div[@class = "sb-team sb-heim"]/a/text()').get()
        if int(score[0]) > 0:
            goals_and_asistances_local = response.xpath('//div[@id = "sb-tore"]/ul/li[@class = "sb-aktion-heim"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()').getall()
        else:
            goals_and_asistances_local = []

        card_owner_local = response.xpath('//div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-heim"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()').getall()
        card_type_local = response.xpath('//div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-heim"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/text()').getall()
        x = []
        if len(card_type_local) > 1:
            for card in card_type_local:
                card=card.replace('\n','')
                card=card.split(',')[0]
                card=card.strip()[2::]
                x.append(card)
            card_type_local = x

        #visitor
        name_visitor = response.xpath('//div[@class = "sb-team sb-gast"]/a/text()').get()
        if int(score[1]) > 0:
            goals_and_asistances_visitor = response.xpath('//div[@id = "sb-tore"]/ul/li[@class = "sb-aktion-gast"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()').getall()
        else:
            goals_and_asistances_visitor = []

        card_owner_visitor = response.xpath('//div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-gast"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/a[@class = "wichtig"]/text()').getall()
        card_type_visitor = response.xpath('//div[@id = "sb-karten"]/ul/li[@class = "sb-aktion-gast"]/div[@class = "sb-aktion"]/div[@class = "sb-aktion-aktion"]/text()').getall()
        x = []
        if len(card_type_visitor) > 1:
            for card in card_type_visitor:
                card=card.replace('\n','')
                card=card.split(',')[0]
                card=card.strip()[2::]
                x.append(card)
            card_type_visitor = x

        yield {
            'tipo'   : 'ida',
            'arbitro': arbitro,
            'links':    kwargs['links'],
            'score':    score,
            'estadio' : stadium,
            'fecha'   : date,
            'hora'    : hour,
            'fase'     :'grupos',
            'nombre_local':name_local,
            'nombre_goleadores_locales_asistentes':goals_and_asistances_local,
            'tarjetas_locales':card_owner_local,
            'tipo_de_tarjeta_local' :card_type_local,
            'nombre_visitante':name_visitor,
            'nombre_goleadores_visitantes_asistentes':goals_and_asistances_visitor,
            'tarjetas_visitantes':card_owner_visitor,
            'tipo_de_tarjeta_visitantes' :card_type_visitor
        }
        #yield response.follow(link_referee,callback = self.parse_referee, cb_kwargs ={'local':name_local,'visitor':name_visitor})

    def parse_referee(self,response, **kwargs):
        local = kwargs['local']
        visitante = kwargs['visitor']
        referee_name = response.xpath('///div[@class = "spielername-profil"]/text()').get()
        referee_name = referee_name.replace('\n','')
        referee_name = referee_name.replace('\t','')
        referee_birthdate = response.xpath('//table[@class = "profilheader"]//tr/td/text()').getall()[0]
        referee_citizenship = response.xpath('//table[@class = "profilheader"]//tr/td/a[@href]/text()').getall()[0]
        yield{
            'local' : local,
            'visitante' : visitante,
            'referee_name' : referee_name,
            'referee_birthdate' : referee_birthdate,
            'referee_citizenship' : referee_citizenship
        }
