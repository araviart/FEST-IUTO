import json
from BD import Groupe
from BD import Reseaux
from BD import Evenement
from BD import Membre_Groupe
# fais l'import pour datetime
from datetime import datetime
from ConnexionBD import ConnexionBD
from sqlalchemy.sql.expression import text
from sqlalchemy.exc import SQLAlchemyError

class GroupeBD:
    def __init__(self, conx: ConnexionBD):
        self.connexion = conx
     
    def search_groupes_with_save_json(self, groupe_recherche, idUser, date = None, genre = None):
        try:
            groupe_recherche = f"%{groupe_recherche}%"
            if date:
                # time data '21 Juillet' does not match format '%d %B'
                moisVersChiffre = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}
                date = date.split(" ")
                # ajoutes l'année (2024)
                date = date[0] + " " + moisVersChiffre[date[1]] + " 2024"
                date = datetime.strptime(date, '%d %m %Y').date()
            requete = "select idE, GROUPE.idG, nomG, heureDebutE, dateDebutE, descriptionG, idH, isSaved(:idUser, groupe.idg) as isSaved from EVENEMENT INNER JOIN GROUPE ON GROUPE.idG = EVENEMENT.idG WHERE idE in (SELECT idE FROM CONCERT) AND nomG LIKE :search" + (" AND dateDebutE = :date" if date else "") + (" AND GROUPE.idG in (SELECT idG FROM GROUPE_STYLE NATURAL JOIN STYLE_MUSICAL WHERE nomSt = :genre)" if genre else "")
            query = text(requete)
            groupes = []
            result = []
            if date and genre:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche, "date": date, "genre": genre, "idUser": idUser})
            elif date:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche, "date": date, "idUser": idUser})
            elif genre:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche, "genre": genre, "idUser": idUser})
            else:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche, "idUser": idUser})
            for idE, idG, nomG, heureDebutE, dateDebutE, descriptionG, idH, isSaved in result:
                groupe = Groupe(idG, idH, nomG, descriptionG, dateDebutE, heureDebutE, isSaved == 1)
                groupes.append(groupe)
            return json.dumps([groupe.to_dict() for groupe in groupes])
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return []
        
        
    def search_groupes_json(self, groupe_recherche, date = None, genre = None):
        try:
            groupe_recherche = f"%{groupe_recherche}%"
            if date:
                # time data '21 Juillet' does not match format '%d %B'
                moisVersChiffre = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}
                date = date.split(" ")
                # ajoutes l'année (2024)
                date = date[0] + " " + moisVersChiffre[date[1]] + " 2024"
                date = datetime.strptime(date, '%d %m %Y').date()
            requete = "select idE, GROUPE.idG, nomG, heureDebutE, dateDebutE, descriptionG, idH from EVENEMENT INNER JOIN GROUPE ON GROUPE.idG = EVENEMENT.idG WHERE idE in (SELECT idE FROM CONCERT) AND nomG LIKE :search" + (" AND dateDebutE = :date" if date else "") + (" AND GROUPE.idG in (SELECT idG FROM GROUPE_STYLE NATURAL JOIN STYLE_MUSICAL WHERE nomSt = :genre)" if genre else "")
            query = text(requete)
            groupes = []
            result = []
            if date and genre:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche, "date": date, "genre": genre})
            elif date:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche, "date": date})
            elif genre:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche, "genre": genre})
            else:
                result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche})
            for idE, idG, nomG, heureDebutE, dateDebutE, descriptionG, idH in result:
                groupe = Groupe(idG, idH, nomG, descriptionG, dateDebutE, heureDebutE)
                groupes.append(groupe)
                
            # convertit en json
            groupes_json = []
            
            for groupe in groupes:
                groupes_json.append(groupe.to_dict())
                
            return json.dumps(groupes_json)
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return []
        
    def get_infos_artiste_json(self, idG):
        try:
            # on veut la description du groupe (descriptionG) dans Groupe
            # et tous les liens des réseaux (reseau) dans lien_reseaux_sociaux
            
            query = text("SELECT descriptionG, reseau, nomG, descriptionG, heureDebutE, dateDebutE, nomL FROM GROUPE NATURAL JOIN LIEN_RESEAUX_SOCIAUX NATURAL JOIN EVENEMENT NATURAL JOIN LIEU WHERE idE in (SELECT idE FROM CONCERT) AND idG = :idG") 
            result = self.connexion.get_connexion().execute(query, {"idG": idG})
            
            print(idG)
            
            descriptionG = ""
            nomG = ""
            heurePassage = ""
            datePassage = ""
            scene = ""
            reseaux = Reseaux()
            
            for description, reseau, nomG, descriptionG, heurePassageG, datePassageG, nomL in result:
                descriptionG = description
                nomG = nomG
                heurePassage = heurePassageG
                datePassage = datePassageG
                scene = nomL
                reseaux.ajoute_reseau(reseau)
            
            lesMembres = []
            
            for membre in self.get_membres_groupe(idG):
                if (type(membre) == Membre_Groupe):
                    lesMembres.append(membre.get_nomDeSceneMG())
            
            lesStylesMusicaux = self.get_styles_groupe(idG)
            
            lesActivitesAnnexe = self.get_activites_annexe_groupe(idG)
            
            return Groupe(idG, None, nomG, descriptionG, datePassage, heurePassage, None, None, reseaux, lesStylesMusicaux, lesMembres, lesActivitesAnnexe, scene).to_dict()
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
    
    def get_infos_supplementaires_artiste_json(self, idG):
        try:
            # on veut la description du groupe (descriptionG) dans Groupe
            # et tous les liens des réseaux (reseau) dans lien_reseaux_sociaux
            
            query = text("SELECT descriptionG, reseau, nomL FROM GROUPE NATURAL JOIN LIEN_RESEAUX_SOCIAUX NATURAL JOIN EVENEMENT NATURAL JOIN LIEU WHERE idG = :idG AND idE in (SELECT idE FROM CONCERT)") 
            result = self.connexion.get_connexion().execute(query, {"idG": idG})
            
            descriptionG = ""
            reseaux = Reseaux()
            scene = ""
            
            for description, reseau, nomL in result:
                descriptionG = description
                reseaux.ajoute_reseau(reseau)
                scene = nomL
                
            lesMembres = []
            
            for membre in self.get_membres_groupe(idG):
                if (type(membre) == Membre_Groupe):
                    lesMembres.append(membre.get_nomDeSceneMG())
            
            lesStylesMusicaux = self.get_styles_groupe(idG)
            
            lesActivitesAnnexe = self.get_activites_annexe_groupe(idG)
            
            return Groupe(idG, None, None, descriptionG, None, None, None, None, reseaux, lesStylesMusicaux, lesMembres, lesActivitesAnnexe,scene).to_dict()
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            
    def get_activites_annexe_groupe(self, idG):
        try:
            query = text("SELECT idG, idE, typeA, descriptionG, dateDebutE, heureDebutE, heureFinE, dateFinE FROM GROUPE NATURAL JOIN EVENEMENT NATURAL JOIN ACTIVITE_ANNEXE WHERE idE in (SELECT idE FROM ACTIVITE_ANNEXE) AND idG = :idG")
            activites_annexe = []
            result = self.connexion.get_connexion().execute(query, {"idG": idG})
            for idG, idE, typeA, descriptionG, dateDebutE, heureDebutE, heureFinE, dateFinE in result:
                activites_annexe.append(Evenement(idE, idG, -1, typeA, heureDebutE, heureFinE, dateDebutE, dateFinE))
            return activites_annexe
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            
    def get_styles_groupe(self, idG):
        # SELECT * FROM festiuto.groupe_style NATURAL JOIN style_musical; on doit recup nomSt
        try:
            query = text("SELECT * FROM GROUPE_STYLE NATURAL JOIN STYLE_MUSICAL WHERE idG = :idG")
            result = self.connexion.get_connexion().execute(query, {"idG": idG})
            styles = []
            for _, _, nomSt in result:
                styles.append(nomSt)
            return styles
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
        
    def get_mon_planning_json(self, idUser):
        try:
            # on doit renvoyer un dico avec les dates de passages en clé et les groupes qui passent ces jours là en valeur
            res = dict()
            
            # on va récuprérer les dates de passage en faisant un call sur la fonctiion getDatesPassage
            
            query = text("call getDatesPassage()")
            result = self.connexion.get_connexion().execute(query)
            for date in result:
                res[str(date[0])] = []
                  
            # on va récupérer les groupes qui passent ces jours là en faisant un call sur la fonction getGroupesDate
            
            for date in res.keys():
                self.connexion = ConnexionBD()
                query = text("call getGroupesDate(:idUser, :dateDebutE)")
                result = self.connexion.get_connexion().execute(query, {"idUser": idUser, "dateDebutE": date})
                # affiche le résultat de la requête
                print(result.keys())
                for idE, idG, nomG, heureDebutE, heureFinE, dateDebutE, descriptionG, in result:
                    self.connexion = ConnexionBD()
                    genres_musicaux = self.get_styles_groupe(idG)
                    nomScene = self.get_nom_scene(idE)
                    res[date].append(Groupe(idG, None, nomG, descriptionG, dateDebutE, heureDebutE, True, heureFinE, None, genres_musicaux, None, None, nomScene).to_dict())
            
            return res
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            
    def get_nom_scene(self, idE):
        #select nomL from evenement natural join lieu WHERE....;
        try:
            query = text("SELECT nomL FROM EVENEMENT natural join LIEU WHERE idE = :idE")
            result = self.connexion.get_connexion().execute(query, {"idE": idE})
            for nomL in result:
                return nomL[0]
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
        
    def get_groupes_with_save_json(self, idUser, date = None, genre = None):
        try:
            if date:
                # time data '21 Juillet' does not match format '%d %B'
                moisVersChiffre = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}
                date = date.split(" ")
                # ajoutes l'année (2024)
                date = date[0] + " " + moisVersChiffre[date[1]] + " 2024"
                date = datetime.strptime(date, '%d %m %Y').date()
            # select idE, groupe.idG, nomG, heureDebutE, dateDebutE, descriptionG, isSaved(#IDUSER, groupe.idg) as isSaved from evenement INNER JOIN groupe ON groupe.idG = evenement.idG;
            requete = "select idE, GROUPE.idG, nomG, heureDebutE, dateDebutE, descriptionG, isSaved(:idUser, GROUPE.idg) as isSaved from EVENEMENT INNER JOIN GROUPE ON GROUPE.idG = EVENEMENT.idG WHERE idE in (SELECT idE FROM CONCERT)" + (" AND dateDebutE = :date" if date else "") + (" AND GROUPE.idG in (SELECT idG FROM GROUPE_STYLE NATURAL JOIN STYLE_MUSICAL WHERE nomSt = :genre)" if genre else "")
            query = text(requete)
            groupes = []
            result = None
            if date and genre:
                result = self.connexion.get_connexion().execute(query, {"date": date, "genre": genre, "idUser": idUser})
            elif date:
                result = self.connexion.get_connexion().execute(query, {"date": date, "idUser": idUser})
            elif genre:
                result = self.connexion.get_connexion().execute(query, {"genre": genre, "idUser": idUser})
            else:
                result = self.connexion.get_connexion().execute(query, {"idUser": idUser})
                
            print(result.keys())
            for idE, idG, nomG, heureDebutE, dateDebutE, descriptionG, isSaved in result:
                groupe = Groupe(idG, None, nomG, descriptionG, dateDebutE, heureDebutE, isSaved == 1)
                groupes.append(groupe.to_dict())
            return json.dumps(groupes)
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
       
    def get_all_groupes_concert(self, date = None, genre = None):
        try:
            if date:
                # time data '21 Juillet' does not match format '%d %B'
                moisVersChiffre = {"Janvier": "01", "Février": "02", "Mars": "03", "Avril": "04", "Mai": "05", "Juin": "06", "Juillet": "07", "Août": "08", "Septembre": "09", "Octobre": "10", "Novembre": "11", "Décembre": "12"}
                date = date.split(" ")
                # ajoutes l'année (2024)
                date = date[0] + " " + moisVersChiffre[date[1]] + " 2024"
                date = datetime.strptime(date, '%d %m %Y').date()
            requete = "select idE, GROUPE.idG, nomG, heureDebutE, dateDebutE, descriptionG, idH from EVENEMENT INNER JOIN GROUPE ON GROUPE.idG = EVENEMENT.idG WHERE idE in (SELECT idE FROM CONCERT)" + (" AND dateDebutE = :date" if date else "") + (" AND GROUPE.idG in (SELECT idG FROM GROUPE_STYLE NATURAL JOIN STYLE_MUSICAL WHERE nomSt = :genre)" if genre else "")
            print(requete)
            query = text(requete)
            groupes = []
            result = None
            if date and genre:
                result = self.connexion.get_connexion().execute(query, {"date": date, "genre": genre})
            elif date:
                result = self.connexion.get_connexion().execute(query, {"date": date})
            elif genre:
                result = self.connexion.get_connexion().execute(query, {"genre": genre})
            else:
                result = self.connexion.get_connexion().execute(query)
            for idE, idG, nomG, heureDebutE, dateDebutE, descriptionG, idH in result:
                print(idE, idG, nomG, heureDebutE, dateDebutE, descriptionG, idH)
                groupe = Groupe(idG, idH, nomG, descriptionG, dateDebutE, heureDebutE)
                groupes.append(groupe)
                
            return groupes
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")   
            
    def get_groupes_horaire_json(self):
        query = text("""
            SELECT
                EVENEMENT.idE,
                GROUPE.idG,
                nomG,
                heureDebutE,
                heureFinE,
                dateDebutE,
                descriptionG,
                nomSt,
                nomL,
                ACTIVITE_ANNEXE.typeA,
                ACTIVITE_ANNEXE.ouvertAuPublic
            FROM EVENEMENT
            INNER JOIN GROUPE ON GROUPE.idG = EVENEMENT.idG
            INNER JOIN GROUPE_STYLE ON GROUPE.idG = GROUPE_STYLE.idG
            INNER JOIN STYLE_MUSICAL ON GROUPE_STYLE.idSt = STYLE_MUSICAL.idSt
            LEFT JOIN LIEU ON EVENEMENT.idL = LIEU.idL
            LEFT JOIN ACTIVITE_ANNEXE ON EVENEMENT.idE = ACTIVITE_ANNEXE.idE
        """)

        result = self.connexion.get_connexion().execute(query)
        res = []

        for idE, idG, nomG, heureDebutE, heureFinE, dateDebutE, descriptionG, nomSt, nomL, typeA, ouvertAuPublic in result:
            groupe = Groupe(idG, None, nomG, descriptionG, dateDebutE, heureDebutE, None, heureFinE)
            merged_dict = groupe.to_dict()
            merged_dict.update({
                "nomSt": nomSt,
                "scene": nomL,
                "typeA": typeA,  # Add attributes from ACTIVITE_ANNEXE
                "ouvertAuPublic": ouvertAuPublic
            })
            res.append(merged_dict)
        return res
    def get_all_groupes(self):
        try:
            # on convertit la date qui est en format "22 juillet" en format "2024-07-22"
            query = text("select idE, GROUPE.idG, nomG, heureDebutE, dateDebutE, descriptionG, idH from EVENEMENT INNER JOIN GROUPE ON GROUPE.idG = EVENEMENT.idG WHERE idE in (SELECT idE FROM CONCERT);")
            groupes = []
            result = self.connexion.get_connexion().execute(query)
            for idE, idG, nomG, heureDebutE, dateDebutE, descriptionG, idH in result:
                print(idE, idG, nomG, heureDebutE, dateDebutE, descriptionG, idH)
                groupe = Groupe(idG, idH, nomG, descriptionG, dateDebutE, heureDebutE)
                groupes.append(groupe)
                
            return groupes
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            
    def insert_groupe(self, groupe):
        try:
            query = text("INSERT INTO GROUPE (idH, nomG, descriptionG) VALUES (:idH, :nomG, :descriptionG)")
            result = self.connexion.get_connexion().execute(query, {"idH": groupe.get_idHebergement(), "nomG": groupe.get_nomG(), "descriptionG": groupe.get_descriptionG()})
            groupe_id = result.lastrowid
            print(f"Le groupe {groupe_id} a été ajouté")
            self.connexion.get_connexion().commit()
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            
    def delete_all_membres_groupe(self, groupe):
        try:
            query = text("DELETE FROM MEMBRE_GROUPE WHERE idG = :idG")
            self.connexion.get_connexion().execute(query, {"idG": groupe.get_idG()})
            print(f"Les membres du groupe {groupe.get_idG()} ont été supprimés")
            self.connexion.get_connexion().commit()
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            
    def delete_groupe_by_name(self, groupe, nom):
        try:
            self.delete_all_membres_groupe(groupe)
            query = text("DELETE FROM GROUPE WHERE idG = :idG AND nomG = :nom")
            self.connexion.get_connexion().execute(query, {"idG": groupe.get_idG(), "nom": nom})
            print(f"Le groupe {groupe.get_idG()} a été supprimé")
            self.connexion.get_connexion().commit()
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")

    def get_groupe_by_id(self, id):
        try:
            query = text("SELECT idG, idH, nomG, descriptionG FROM GROUPE WHERE idG = :id")
            result = self.connexion.get_connexion().execute(query, {"id": id})
            for idG, idH, nomG, descriptionG in result:
                return Groupe(idG, idH, nomG, descriptionG)
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}") 

    def get_all_groupes_concert_json(self, date=None, genre=None):
        groupes = self.get_all_groupes_concert(date, genre)
        groupes_json = []
        for groupe in groupes:
            groupes_json.append(groupe.to_dict())
        return json.dumps(groupes_json)

    # renvoie le nom, l'id, la date et l'heure de passage d'un groupe EN JSON
    def get_groupes_json(self):
        groupes = self.get_all_groupes()
        groupes_json = []
        for groupe in groupes:
            groupes_json.append(groupe.to_dict())
        return json.dumps(groupes_json)
    
    
    
    
    def add_image(self, idGroupe, image):
        try:
            query = text("UPDATE GROUPE SET imgG = :imgG WHERE idG = :idG")
            self.connexion.get_connexion().execute(query, {"imgG": image, "idG": idGroupe})
            self.connexion.get_connexion().commit()
            return True
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return False
        
    def modifier_img(self, idGroupe, image):
        try:
            query = text("UPDATE GROUPE SET imgG = :imgG WHERE idG = :idG")
            self.connexion.get_connexion().execute(query, {"imgG": image, "idG": idGroupe})
            self.connexion.get_connexion().commit()
            return True
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return False
        
    def get_image(self,idGroupe):
        try:
            query = text("SELECT imgG FROM GROUPE WHERE idG = :idG")
            result = self.connexion.get_connexion().execute(query, {"idG": idGroupe})
            for imgMG in result:
                return imgMG[0]
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return None
        
    def search_groupes(self, groupe_recherche):
        try:
            groupe_recherche = f"%{groupe_recherche}%"
            query = text("SELECT idG, idH, nomG, descriptionG FROM GROUPE WHERE nomG LIKE :search")
            groupes = []
            result = self.connexion.get_connexion().execute(query, {"search": groupe_recherche})
            for idG, idH, nomG, descriptionG in result:
                groupes.append(Groupe(idG, idH, nomG, descriptionG).to_dict())
            return groupes
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return []
        
    def update_groupe(self, groupe):
        try:
            query = text("UPDATE GROUPE SET idH = :idH, nomG = :nomG, descriptionG = :descriptionG WHERE idG = :idG")
            self.connexion.get_connexion().execute(query, {"idH": groupe.get_idHebergement(), "nomG": groupe.get_nomG(), "descriptionG": groupe.get_descriptionG(), "idG": groupe.get_idG()})
            self.connexion.get_connexion().commit()
            return True
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return False
        
    def get_membres_groupe(self, idGroupe):
        try:
            query = text("select idMG, idG, nomMG, prenomMG, nomDeSceneMG, descriptionA from MEMBRE_GROUPE natural join GROUPE where idG=:idG")
            membres = []
            result = self.connexion.get_connexion().execute(query, {"idG": idGroupe})
            for idMG, idG, nomMG, prenomMG, nomDeSceneMG, descriptionA in result:
                membres.append(Membre_Groupe(idMG, idG, nomMG, prenomMG, nomDeSceneMG, descriptionA))
            return membres
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return []

    def get_id_groupe_by_name(self, nom):
        try:
            query = text("SELECT idG FROM GROUPE WHERE nomG = :nom")
            result = self.connexion.get_connexion().execute(query, {"nom": nom})
            for idG in result:
                return idG[0]
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return None
        
    def update_image(self, groupe, image):
        try:
            query = text("UPDATE GROUPE SET imgG = :imgG WHERE idG = :idG")
            self.connexion.get_connexion().execute(query, {"imgG": image, "idG": groupe.get_idG()})
            self.connexion.get_connexion().commit()
            return True
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return False
        
    def get_all_groupes_bd_normal(self):
        try:
            query = text("SELECT idG, idH, nomG, descriptionG FROM GROUPE")
            groupes = []
            result = self.connexion.get_connexion().execute(query)
            for idG, idH, nomG, descriptionG in result:
                groupes.append(Groupe(idG, idH, nomG, descriptionG))
            return groupes
        except SQLAlchemyError as e:
            print(f"La requête a échoué : {e}")
            return []