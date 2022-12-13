from sqlalchemy import create_engine, text
class museums_data(object):
    def __init__(self):
        self._engine= create_engine("sqlite:///art.db", echo = True)
    def get_museums(self):
        sql = text("""select a.name as name, a.id as id, date_found, b.city as city, b.country as country from Museums a join
        (select a.name as city, b.name as country, a.id as city_id from Cities a join Countries b on a.country_id = b.id) as b on a.city_id = b.city_id;""")
        sql_result = self._engine.execute(sql)
        ret =  []
        for record in sql_result:
            ret.append(dict(record))
        return ret
    def get_people(self):
        sql = text("""select a.id , a.name, a.date_of_birth as birth, b.date as death from People a join Deaths b on a.id = b.people_id;""")
        sql_result = self._engine.execute(sql)
        ret = []
        for record in sql_result:
            ret.append(dict(record))
        return ret
    def get_artworks(self):
        sql = text("""select distinct a.name as name, a.date_created as date_of_creation, t.name as type, xxx.name as artist, m.name as museum from Artworks a 
        left join Art_types t on t.id=a.type_id 
        left join Museums m on m.id=a.museum_id 
        left join Arts_people ap on ap.art_id=a.id 
        left join (select ap.art_id as art_id, group_concat(p.name, ", ") as name from Arts_people ap left join People p on p.id=ap.people_id group by ap.art_id) xxx on xxx.art_id = a.id;""")
        sql_result = self._engine.execute(sql)
        ret = []
        for record in sql_result:
            ret.append(dict(record))
        return ret
    def get_artworks_museum(self,museums_id):
        sql = text("""select group_concat(a.name,\",\") as name from Artworks as a join Museums as b on a.museum_id = b.id where b.id = """+str(museums_id)+";" )
        sql_result = self._engine.execute(sql)
        ret = []
        for record in sql_result:
           ret.append(dict(record))
        return ret
    def get_country(self, museums_id):
        sql = text("""select group_concat(a.name,\",\") as countries from
                       Countries as a join(select * from Cities as a join Museums as b on a.id = b.city_id where
                       b.id= """ + str(museums_id) +") as b on a.id = b.country_id;")
        sql_result = self._engine.execute(sql)
        for record in sql_result:
            dictionary = dict(record)
        return dictionary["countries"]
    def get_museum_name(self,museum_id):
        sql = text("select * from Museums where id = " +str(museum_id) +";")
        sql_result = self._engine.execute(sql)
        for muse in sql_result:
            res = str(muse["name"])
        return res
    def get_museum_date_of_found(self, museum_id):
        sql = text("select * from Museums where id=" +str(museum_id)+";")
        sql_result = self._engine.execute(sql)
        for muse in sql_result:
            res = str(muse["date_found"])
        return res
    def get_museum_city(self, museum_id):
        sql = text("select c.name as name from Museums m join Cities c on c.id=m.city_id where m.id ="+str(museum_id)+ " ;")
        sql_result = self._engine.execute(sql)
        for muse in sql_result:
            res = str(muse["name"])
        return res
    def get_country_people(self,people_id):
        sql = text("""select  group_concat(a.name, \", \") as name  from Countries as a join Country_person as b on a.id = b.country_id where people_id = """+str(people_id)+";")
        sql_result = self._engine.execute(sql)
        ret = []
        for record in sql_result:
            ret.append(dict(record))
        return ret
    def get_artworks_people(self,people_id):
#         sql =  text("select group_concat(a.name,\",\") as people, b.name as name from People as a left join Arts_people ap on ap.people_id = a.id left join Artworks as b on ap.art_id =b.id where a.id=" + str(people_id) +";")
        sql = text("select group_concat(a.name,\",\") as name from People as p left join Arts_people ap on ap.people_id = p.id left join Artworks as a on ap.art_id =a.id where p.id=" + str(people_id) +";")
        sql_result = self._engine.execute(sql)
        ret = []
        for record in sql_result:
            ret.append(dict(record))
        return ret
    def get_name_people(self,people_id):
        sql = text("select * from People where id =" +str(people_id) + ";")
        sql_result = self._engine.execute(sql)
        for peo in sql_result:
            res = str(peo["name"])
        return res
                    
                    
# bd = museums_data()
# print(bd.get_artworks())
# print(bd.get_museums())
# print(bd.get_country(6))
# print(bd.get_museum_name(6))
