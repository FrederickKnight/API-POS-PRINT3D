from app import db
from flask import Response,json

from os import urandom
import binascii
from hashlib import sha256
from datetime import datetime,timedelta
import math
from app.custom_errors import (
    ValidationError
)

class BaseAuthController:
    def __init__(self,user_model,user_defaults,session_model,session_defaults):
        self._model = user_model
        self._user_session = session_model
        self._user_defaults = user_defaults
        self._session_defaults = session_defaults
        
        self.session = db.session

    def register_user(self,data):
        if "id" in data:
            data["id"] = None
            
        user_already_exist = True if self.__query_username__(data["username"]) else False
        if not user_already_exist:
            if not "password" in data:
                raise ValidationError("invalid given data, not password")
            
            try:
                new_data = self._model(**{**self._user_defaults,**data})
                new_data.set_password(data["password"])
                self.session.add(new_data)
                self.session.commit()
                
            except Exception as e:
                self.session.rollback()
                raise e

            return self.__return_json__(self.session.query(self._model).filter_by(id = new_data.id).first())
        else:
            raise ValidationError("User already exist")
        
    def delete_user_by_id(self,id):
    
        _user = self.__query_id__(id)
            
        if _user != None:
            try:
                self.session.delete(_user)
                self.session.commit()
                
            except Exception as e:
                self.session.rollback()
                raise e
            
            return Response(status=204)
        else:
            raise ValidationError("User doesn't exist or invalid given data")
        
    
    def get_by_id(self,_id):
        _user = self.__query_id__(_id)
        
        if _user != None:
            return self.__return_json__(_user)
        else:
            raise ValidationError("User doesn't exist or invalid given data")
            
    def validate_user(self,data):
        if "username" in data and "password" in data:
            _user = self.__query_username__(data["username"])
            if _user == None:
                raise ValidationError("User doesn't exist or invalid given data")
                
            data_pass = _user.validate_password(data["password"])
            
            if data_pass == False:
                raise ValidationError("Password is incorrect or invalid given data")
                
            return self.__return_json__(_user)
        
        else:
            raise ValidationError("invalid given data, not username or password")
        

    # auth
    def generateSessionToken(self):
        bytes = urandom(20)
        token = binascii.hexlify(bytes).decode()
        return Response(response=json.dumps({"token":token}),status=200,mimetype="application/json")
        

    def createSessionToken(self,_json,UserId:int):
        if not "token" in _json:
            raise ValidationError("there is no token")
        
        token = _json["token"]    
        userSessionId = sha256(token.encode('utf-8'),usedforsecurity=True).hexdigest()
        expires_at = datetime.now() + timedelta(days=30)
        session_data = {
            "id_client":UserId,
            "session":userSessionId,
            "expires_at":math.floor(expires_at.timestamp())
        }
        
        try:
            new_session = self._user_session(**{**self._session_defaults,**session_data})
            self.session.add(new_session)
            self.session.commit()
            
        except Exception as e:
            self.session.rollback()
            raise e
        
        return Response(response=json.dumps(session_data),status=200,mimetype="application/json")
        
        
    def validateSessionToken(self,token:str):
        userSessionId = sha256(token.encode('utf-8'),usedforsecurity=True).hexdigest()
        _query = self.session.query(self._user_session).filter_by(session = userSessionId).first()
        
        sessionData = {
            "session":None,
            "user":None
        }
        
        if not _query:
            return {
            "session":None,
            "user":None
        }
        
        sessionJson = _query.get_json(True)
        expiration_Date = datetime.fromtimestamp(sessionJson["expires_at"])
        if datetime.now() >= expiration_Date:
            # si expiro
            self.session.delete(_query)
            self.session.commit()
            return {
                "session":None,
                "user":None
            }
        
        if datetime.now() >= (expiration_Date - timedelta(days=-15)):
            # si es menor a 15 dias
            new_expires_at = datetime.now() + timedelta(days=30)
            _query.expires_at = new_expires_at
            self.session.merge(_query)
            self.session.flush()
            self.session.commit()
        
        id_user = sessionJson["client"]["id"]
        sessionData["user"] = sessionJson["client"]
        
        del sessionJson["client"]
        sessionJson["id_client"] = id_user
        sessionData["session"] = sessionJson
        return Response(response=json.dumps(sessionData),status=200,mimetype="application/json")

    def invalidateSession(self,userSessionId:str):
        _query = self.session.query(self._user_session).filter_by(session = userSessionId).first()
        if _query:
            self.session.delete(_query)
            self.session.commit()
            return Response(status=204,mimetype="application/json")
        else:
            raise ValidationError("Invalid Session")

    #helpers
    def __return_json__(self,items_query,isSecret:bool = True):   
            _response = []
            try:
                if(isinstance(items_query,list) or isinstance(items_query,dict)):
                    _response = [item.get_dict() for item in items_query] if isSecret else [item.__get_secrets__() for item in items_query]
                else:
                    _response = [items_query.get_json()] if isSecret else [items_query.__get_secrets__()]
            except:
                return items_query
            
            return {
                "data":_response,
                "metadata":{
                    "type":str(self._model().__getClassName__()),
                    "size":len(_response)
                }
            }
            
    def __query_id__(self,_id):
        if isinstance(_id,int):
            return self.session.query(self._model).filter_by(id = _id).first()
        return None

    def __query_username__(self,_username):
        if isinstance(_username,str):
            return self.session.query(self._model).filter_by(username = _username).first()
        return None

        
    def __query_username__(self,_username):
        if isinstance(_username,str):
            return self.session.query(self._model).filter_by(username=_username).first()
        else:
            return None