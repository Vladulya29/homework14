from flask import Flask, jsonify
from sql import from_sql


app = Flask(__name__)

@app.route('/movie/<title>')
def get_sql_title(title):
    query = f'''
    SELECT title
            , country
            , release_year
            , listed_in
            , description
    FROM netflix
    WHERE title = '{title}'
    ORDER BY release_year DESC
    LIMIT 1
'''
    films = from_sql(query)[0]
    result = {
        'title': films[0],
        'country': films[1],
        'realese_year': films[2],
        'genre': films[3],
        'description': films[4]
    }
    return jsonify(result)

@app.route('/movie/<int:start>/to/<int:stop>')
def get_sql_year(start, stop):
    query = f'''
    SELECT title
    , release_year
    FROM netflix
    WHERE release_year BETWEEN {start} AND {stop}
    ORDER BY release_year
    LIMIT 100
'''
    films = from_sql(query)
    list_result = []
    for film in films:
        result = {
            'title': film[0],
            'release_year': film[1]
        }
        list_result.append(result)
    return jsonify(list_result)

@app.route('/rating/<group>')
def get_sql_group(group):
    groups = {
        'children': "'G'",
        'family': "'G', 'PG', 'PG-13'",
        'adult': "'R', 'NC-17'"
    }
    query = f'''
    SELECT title
    , rating
    , description 
    FROM netflix
    WHERE rating IN ({groups[group]})
    LIMIT 100
'''
    films = from_sql(query)
    list_result = []
    for film in films:
        result = {
            'title': film[0],
            'rating': film[1],
            'description': film[2]
        }
        list_result.append(result)
    return jsonify(list_result)

@app.route('/genre/<genre>')
def get_sql_genre(genre):
    query = f'''
    SELECT title
    , description 
    FROM netflix
    WHERE listed_in LIKE '%Comedies%'
    ORDER BY release_year DESC  
    LIMIT 10
'''
    films = from_sql(query)
    list_result = []
    for film in films:
        result = {
            'title': film[0],
            'description': film[1]
        }
        list_result.append(result)
    return jsonify(list_result)



if __name__ == '__main__':
    app.run()