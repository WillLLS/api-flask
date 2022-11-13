from .app import app,api
from flask_restx import fields

get_allcategories = api.model('retourgetallcategories',{'intitule':fields.String(exemple='Action'),'location':fields.Url(exemple='/categorieFilm/1')})

categoriepost = api.model('categoriepost',{'intitule':fields.String(exemple='Horreur',required=True),'description':fields.String(exemple='Catégorie avec plein d explosion qui font boom', required=False)})
categorieget = api.model('categorieget',{'id':fields.Integer(exemple=1),'intitule':fields.String(exemple='Action'),'description':fields.String(exemple='Catégorie avec plein d explosion qui font boom ')})

get_allfilm = api.model('retourgetallfilm',{'Titre':fields.String(exemple='Inception'),'categorie':fields.String(exemple='Science-Fiction'),'location':fields.Url(exemple='/categorieFilm/1/film/4')})

filmpost = api.model('filmpost',
                    {'titre':fields.String(exemple='Black Panther',required=True),
                    'categorie':fields.List(fields.Integer),
                    'acteur_film':fields.String(exemple='Chadwick Boseman; Michael B.Jordan',required=False),
                    'annee_realisation':fields.String(exemple='2018',required=False),
                    'duree':fields.String(exemple='2h15',required=False),
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
