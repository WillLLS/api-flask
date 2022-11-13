from video import *

add_client = api.model('clientpost', {
                                    'nom_client':fields.String(exemple='Dupond'),
                                     "prenom":fields.String(exemple='Dupond'), 
                                     "email":fields.String(exemple='truc@truc.fr'), 
                                     "age":fields.Integer(exemple=49)})


@api.route("/clients")
class client(Resource):
    @api.doc(model=add_client)
    def get(self):
        """
        Retourne la liste de tous les clients
        """
        connection = sqlite3.connect("video1.db")
        try:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM client;')
            clients = cursor.fetchall()
            app.logger.info(clients[0])
        except sqlite3.Error as e:
            raise(e)
        finally:
            connection.close()

        
        return jsonify(self.ClienttoJson(clients))
    
    def ClienttoJson(self, clients):
        allClientList = []
        for client in clients:
            row = {"nom_client": client[1], "prenom": client[2], "email": client[3], "age": client[4]}
            allClientList.append(row)
        return allClientList

    @api.doc(body=add_client, model=add_client)
    def post(self):
        """
        Ajout d'un nouveau client
        """

        newClient = {}
        if request.json:
            connection = sqlite3.connect('video1.db')
            try:
                
                cursor = connection.cursor()
                
                var =  (request.json["nom_client"], request.json["prenom"], request.json["email"], request.json["age"])
                query = 'INSERT INTO client(nom_client, prenom, email, age) VALUES (?, ?, ?, ?)'
                
                cursor.execute(query, var)
                connection.commit()
                
            except sqlite3.Error as e:
                connection.rollback()
                print(e)
            finally:
                connection.close()

            newClient["nom_client"] = request.json["nom_client"]
            newClient["prenom"] = request.json["prenom"]
            newClient["email"] = request.json["email"]
            newClient["age"] = request.json["age"]
            

            response = jsonify(newClient)
            response.status_code = 201
            response.headers['location'] = '/clients'
            return response
        else:
            abort(415)

if __name__=='__main__' :
    app.run(debug=True)