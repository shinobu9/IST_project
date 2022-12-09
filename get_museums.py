	def get_full_info_museum(self, museumId):
		"""
		на выходе словарь, в котором ключи:
		"museumName", "foundDate", "city", "сountry", "artworks", 
		все кроме последнего значения - строки/инты, а последнее - список строк.
		"""
		sql = text(f"select m.name as "museumName", m.date_found as "foundDate", ci.name as "city", co.name as "сountry" from Museums as m left join Cities as ci on m.city_id = ci.id left join Countries as co on co.id=ci.country_id	WHERE m.id = {museumId};")
		sql_result = self._engine.execute(sql)
		row = sql_result.fetchone() # По логике должен вернуть  один кортеж с содержанием:(название музея, дата основ, город, страна)
		
		museum_dict = {}
		museum_dict["museumName"] = row[0]
		museum_dict["foundDate"] = row[1]	
		museum_dict["city"] = row[2]
		museum_dict["сountry"] = row[3]
		museum_dict["artworks"] = []

		# сделать запрос отдельно к артворк
		sql2 = text(f"select name as artwork from Artworks where museum_id = {museumId};")
		sql_result2 = self._engine.execute(sql2)
		rows = sql_result.fetchall() # на выходе список кортежей, в каждом из которых произведение, находящееся в нужном музее
		for i in range(len(rows)):
			museum_dict["artworks"].append(rows[i][0])
