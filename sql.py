import sqlite3

def from_sql(query):
    with sqlite3.connect('netflix.db') as connection:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()

def get_sql_casts(name_1, name_2):
    query = f'''
    SELECT "cast"
    FROM netflix
    WHERE "cast" LIKE '%{name_1}%' AND "cast" LIKE '%{name_2}%'
'''
    costs = from_sql(query)
    actors = []
    for cost in costs:
        actors.extend(cost[0].split(', '))
    result = []
    for actor in actors:
        if actor not in [name_1, name_2]:
            if actors.count(actor) > 2:
                result.append(actor)
    result = set(result)
    return result

def get_sql_films(type, year, genre):
    query = f'''
    SELECT title
            , description
    FROM netflix
    WHERE "type" = '{type}'
        AND release_year = {year}
        AND listed_in LIKE '%{genre}%'
'''
    films = from_sql(query)
    list_result = []
    for film in films:
        result = {
            'title': film[0],
            'description': film[1]
        }
        list_result.append(result)
    return list_result
