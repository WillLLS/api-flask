from flask import Flask, jsonify, url_for, request, abort
from flask_restx import Api, Resource, fields
import sqlite3

"""
connection = sqlite3.connect("video.db")

cursor = connection.cursor()

id = (1,)

cursor.execute('SELECT * FROM categorie WHERE id_categorie = ?',id)
req = cursor.fetchone()
categorie = {
    'intitule':req[1],
    'description':req[2]
}


cursor.execute('SELECT id_categorie FROM categorie ')
req = cursor.fetchall()
print(req)

test = ('Du suspence tout le temps tout le temps',5)

cursor.execute("UPDATE categorie SET description_categorie = ? WHERE id_categorie = ? ",test)
connection.commit()


sql = '''SELECT film.id_film,film.titre_film FROM film
                JOIN film_categorie
                ON film.id_film = film_categorie.film_id
                JOIN categorie
                ON film_categorie.categorie_id = categorie.id_categorie
                WHERE categorie.id_categorie = ?
                
                '''
cursor.execute(sql,id)
print(cursor.fetchall())

cursor.execute("SELECT film.id_film FROM film")
id = len(cursor.fetchall())+1

print(f'cursor.lastrowid1 = {cursor.lastrowid}')
new_film = (id,'Titanic 2',
            'Leonardo Dicaprio',
            '2008',
            '3h15',
            'Un gros bateau qui coule 2 fois',
            10)

cursor.execute('INSERT INTO film VALUES(?,?,?,?,?,?,?)',new_film)
print(f'cursor.lastrowid = {cursor.lastrowid}')
film_cat = (id,4)
cursor.execute('INSERT INTO film_categorie VALUES (?,?)',film_cat)

connection.commit()

connection.close()
"""


app = Flask(__name__)
api = Api(app)

get_allcategories = api.model('retourgetallcategories',{'intitule':fields.String(exemple='Action'),'location':fields.Url(exemple='/categorieFilm/1')})

categoriepost = api.model('categoriepost',{'intitule':fields.String(exemple='Horreur',required=True),'description':fields.String(exemple='Catégorie avec plein d explosion qui font boom', required=False)})
categorieget = api.model('categorieget',{'id':fields.Integer(exemple=1),'intitule':fields.String(exemple='Action'),'description':fields.String(exemple='Catégorie avec plein d explosion qui font boom ')})

get_allfilm = api.model('retourgetallfilm',{'Titre':fields.String(exemple='Inception'),'categorie':fields.String(exemple='Science-Fiction'),'location':fields.Url(exemple='/categorieFilm/1/film/4')})

filmpost = api.model('filmpost',
                    {'titre':fields.String(exemple='Black Panther',required=True),
                    'acteur_film':fields.String(exemple='Chadwick Boseman; Michael B.Jordan',required=False),
                    'année réalisation':fields.String(exemple='2018',required=False),
                    'durée':fields.String(exemple='2h15',required=False),
                    'resume_film':fields.String(exemple='Un film incroyable',required=False),
                    'age_min':fields.Integer(exemple=12,required=False)})

filmget = api.model('filmget',
                    {'id':fields.Integer(exemple=7),
                    'categorie':fields.String(exemple='Action'),
                    'titre':fields.String(exemple='Black Panther'),
                    'acteur_film':fields.String(exemple='Chadwick Boseman; Michael B.Jordan'),
                    'année réalisation':fields.String(exemple='2018'),
                    'durée':fields.String(exemple='2h15'),
                    'resume_film':fields.String(exemple='Un film incroyable'),
                    'age_min':fields.Integer(exemple=12)})

@api.route('/categorieFilm')
class CategorieAll(Resource):
    @api.doc(model=get_allcategories)
    def get(self):
        """
        Retourne l'intitulé et la location de toutes les catégories de vidéo
        """
        locations=[]
        connection = sqlite3.connect("video1.db")
        cursor = connection.cursor()
        cursor.execute('SELECT DISTINCT id_categorie, nom_categorie FROM categorie')
        categories = cursor.fetchall()

        for idc in categories:
            intitule = idc[1]
            locations.append({
                'intitule':intitule,
                'location':'/categorieFilm/'+str(idc[0])})

        connection.close()
        return(jsonify(locations))

    @api.doc(body=categoriepost,model=categorieget)
    def post(self):
        """
        Création d'une nouvelle catégorie
        """
        categorie = {}
        id = 0
        if request.json :
            try:
                categorie['intitule']=request.json['intitule']
                categorie['description']=request.json['description']

                connection = sqlite3.connect('video1.db')
                cursor = connection.cursor()
                new_categorie = (cursor.lastrowid, request.json['intitule'],request.json['description'])
                cursor.execute('INSERT INTO categorie VALUES(?,?,?)',new_categorie)
                id = cursor.lastrowid
                connection.commit()
    
            except Exception as e:
                print("[ERREUR]",e)
                connection.rollback()
            finally:
                connection.close()

            response = jsonify(categorie)
            response.status_code = 201
            response.headers['location'] = '/categorieFilm/'+str(id)
            return response
        
        else:
            abort(415)

@api.route('/categorieFilm/<idcat>', endpoint='categorieget')
class CategorieOne(Resource):
    @api.doc(model = categorieget)
    def get(self,idcat):
        """
        Retourne le détail d'une catégorie
        """
        connection = sqlite3.connect('video1.db')
        cursor = connection.cursor()
        cursor.execute('SELECT id_categorie FROM categorie ')
        last_id = len(cursor.fetchall())
        if int(idcat) > last_id or int(idcat)==0:
            connection.close()
            abort(404)
        
        id = (idcat,)
        cursor.execute('SELECT * FROM categorie WHERE id_categorie = ?',id)
        req = cursor.fetchone()

        categorie = {
            'id':req[0],
            'intitule':req[1],
            'description':req[2]
        }

        connection.close()

        response=jsonify(categorie)
        response.status=200
        return response

    @api.doc(body=categoriepost, model=categorieget)
    def put(self,idcat):
        """
        Modifie les détails d'une catégorie (Titre, Description)
        """
        if request.json:
            intid = int(idcat)
            connection = sqlite3.connect("video1.db")
            cursor = connection.cursor()

            cursor.execute('SELECT id_categorie FROM categorie')
            categories_id = []
            categorie = {}
            for i in cursor.fetchall():
                categories_id.append(int(i[0]))
            
            if intid not in categories_id:
                abort(404)

            try:
                update_categorie = (request.json['intitule'],request.json['description'],intid)
                cursor.execute('UPDATE categorie SET nom_categorie = ?, description_categorie = ? WHERE id_categorie = ?',update_categorie)
                connection.commit()

                categorie['intitule']=request.json['intitule']
                categorie['description']=request.json['description']

            except(TypeError, ValueError):
                abort(400)
                connection.rollback()
            finally:
                connection.close()


            response = jsonify(categorie)
            response.status_code=200
            response.headers['location'] = '/categorieFilm'+str(intid)
            return response

        else:
            abort(415)

    @api.doc()
    def delete(self,idcat):
        """
        Supprimer une catégorie
        """
        intid = int(idcat)

        connection = sqlite3.connect("video1.db")
        cursor = connection.cursor()

        cursor.execute('SELECT id_categorie FROM categorie')
        categories_id = []
        for i in cursor.fetchall():
            categories_id.append(int(i[0]))
        
        if intid not in categories_id:
            abort(404)
        
        try:
            categorie_delete = (intid,)
            cursor.execute('DELETE FROM categorie WHERE id_categorie = ?',categorie_delete)
            connection.commit()
        except sqlite3.Error as e:
            print("Erreur lors de la suppression de la catégorie",e)
            connection.rollback()
        finally:
            connection.close()
            return()

@api.route('/categorieFilm/<idcat>/film')
class FilmAll(Resource):
    api.doc(model=get_allfilm)
    def get(self,idcat):
        """
        Retourne le titre et la location de tout les films compris dans 
        cette catégorie 
        """
        locations = []
        try:
            connection = sqlite3.connect('video1.db')
            cursor = connection.cursor()
            id = (int(idcat),)
            sql = """SELECT film.id_film,film.titre_film, categorie.nom_categorie FROM film
                    JOIN film_categorie
                    ON film.id_film = film_categorie.film_id
                    JOIN categorie
                    ON film_categorie.categorie_id = categorie.id_categorie
                    WHERE categorie.id_categorie = ?
                    """
            
            cursor.execute(sql,id)
            films = cursor.fetchall()
            for i in films:
                titre = i[1]
                locations.append({
                    'titre':titre,
                    'categorie':i[2],
                    'location':'categorieFilm/'+idcat+'/film/'+str(i[0])})
        except sqlite3.Error as e:
            print("Erreur",e)
            connection.rollback()
        finally:
            connection.close()
            return(jsonify(locations))

    @api.doc(body=filmpost, model=filmget)
    def post(self,idcat):
        """
        Ajout d'un film dans la catégorie
        """
        film = {}
        id = 0
        intid = int(idcat)
        if request.json :
            try:
                connection = sqlite3.Connection("video1.db")
                cursor = connection.cursor()
                
                cursor.execute("SELECT film.id_film FROM film")
                id = len(cursor.fetchall())+1
                
                new_film = (id,request.json['titre'],
                            request.json['acteur_film'],
                            request.json['année réalisation'],
                            request.json['durée'],
                            request.json['resume_film'],
                            request.json['age_min'])

                cursor.execute('INSERT INTO film VALUES(?,?,?,?,?,?,?)',new_film)
                #id = cursor.lastrowid
                film_cat = (id,intid)
                cursor.execute('INSERT INTO film_categorie VALUES (?,?)',film_cat)

                connection.commit()

                film['titre']=request.json['titre']
                film['acteur film']=request.json['acteur_film']
                film['année réalisation']=request.json['année réalisation']
                film['durée']=request.json['durée']
                film['résumé film']=request.json['resume_film']
                film['age minimum']=request.json['age_min']
                
            

            except Exception as e:
                print("[Erreur]",e)
                connection.rollback()
            
            finally:
                connection.close()

            response = jsonify(film)
            response.status_code = 201
            response.headers['location'] = 'categorieFilm/'+idcat+'/film/'+str(id)
            return response

        else:
            abort(415)




if __name__=='__main__' :
    app.run(debug=True)

