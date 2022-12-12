from sqlalchemy import create_engine, text
# здесь museums.db  - название бд, которуя  я развернул у себя. (надо будет заменить)

class ArtsData(object):
    def __init__(self):
        self._engine = create_engine(f"sqlite:///museums.db", echo = True)
	

    def get_full_info_museum(self, museumId):
        # " на выходе словарь, в котором ключи: "museumName","foundDate", "city","сountry", "id", "artworks", все кроме последнего значения - строки/ инты, а последнее - список строк."
        sql = text("select m.name as museumName, m.date_found as foundDate, ci.name as city, co.name as country, m.id as id \
        from Museums as m left join Cities as ci on m.city_id = ci.id \
        left join Countries as co on co.id=ci.country_id \
        WHERE m.id =" + str(museumId) + ";")
        sql_result = self._engine.execute(sql)
        row = sql_result.fetchone() 
		
        museum_dict = {}
        museum_dict["museumName"] = row[0]
        museum_dict["foundDate"] = row[1]	
        museum_dict["city"] = row[2]
        museum_dict["country"] = row[3]
        museum_dict["id"] = row[4]
        museum_dict["artworks"] = []

        # "сделать запрос отдельно к артворк"
        sql2 = text(f"select name as artwork \
		from Artworks \
		where museum_id = {museumId};")
        sql_result2 = self._engine.execute(sql2)
        rows = sql_result2.fetchall()
        for i in range(len(rows)):
            museum_dict["artworks"].append(rows[i][0])
        return museum_dict


    def get_museums(self):
        # возвращает список названий музеев.
        sql = text("select id, name from Museums;")
        sql_result = self._engine.execute(sql)
        row = sql_result.fetchall()  
        return row



    def get_people(self):
        # список кортежей вида (id, name)
        sql = text("select id, name from People;")
        sql_result = self._engine.execute(sql)
        row = sql_result.fetchall()  
        return row


    def get_full_info_person(self, person_id):
        # возвращает словарь с ключами: id, name, birthday, deathDate, countries, artworks. Два послдених значения - списки.
        sql = text(f"select p.id, p.name, p.date_of_birth, d.date\
        from People p left join Deaths d on p.id = d.people_id\
        where p.id = {person_id};")
        sql_result = self._engine.execute(sql)
        row = sql_result.fetchone()

        person_dict = {}
        person_dict["id"] = row[0]
        person_dict["name"] = row[1]
        person_dict["birthday"] = row[2]
        person_dict["deathDate"] = row[3]
        person_dict["countries"] = []
        person_dict["artworks"] = []

        # "сделать запрос отдельно к артворк"
        sql2 = text(f"select a.name \
		from Artworks as a inner join Arts_people as ap\
        on a.id = ap.art_id\
        inner join People as p\
        on p.id = ap.people_id\
		where p.id = {person_id};")
        sql_result2 = self._engine.execute(sql2)
        rows1 = sql_result2.fetchall()
        for i in range(len(rows1)):
            person_dict["artworks"].append(rows1[i][0])

        # "сделать запрос отдельно к странам"
        sql3 = text(f"select c.name\
        from Countries as c inner join Country_person as cp\
        on c.id = cp.country_id\
        inner join  People as p\
        on p.id = cp.people_id\
        where p.id = {person_id};")
        sql_result3 = self._engine.execute(sql3)
        rows2 = sql_result3.fetchall()
        for i in range(len(rows2)):
            person_dict["countries"].append(rows2[i][0])

        return person_dict
  
    def get_full_info_artworks(self):
        # возвращает список кортежей вида (название произведения искуства, тип, автор, дата создания, музей (если нет, то None))
        sql = text("select a.name, at.name, p.name, a.date_created, m.name from Artworks as a\
        left join Art_types at on at.id=a.type_id\
        left join Arts_people ap on ap.art_id=a.id\
        left join People p on p.id=ap.people_id\
        left join Museums m on m.id = a.museum_id;")
        sql_result = self._engine.execute(sql)
        row = sql_result.fetchall()  
        return row
