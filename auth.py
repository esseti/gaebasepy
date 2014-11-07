import json
import logging
from urllib import urlencode
import urllib2
from google.appengine.api import urlfetch
from gymcentral.exceptions import AuthenticationError
import models


__author__ = 'stefano'


class GCAuth():
    """
    Class that manages the Authorization

    TODO: create a cron job that deletes old/expired tokens
    """
    __user_model = models.User

    @classmethod
    def auth_user(cls, user):
        """
        get the token of the current user
        :param user
        :return: token
        """
        user_id = user.get_id()
        user_token = cls.__user_model.create_auth_token(user_id)
        token = str(user_id) + "|" + user_token
        # if int(self.__AUTH_TYPE) == 1:
        return {"token": token}
        # elif int(self.__AUTH_TYPE) == 2:
        # scs = SecureCookieSerializer(self.__SECRET_KEY)
        # token = scs.serialize('token', token)
        # expiration = datetime.datetime.now() + datetime.timedelta(minutes=1)
        #     self.response.set_cookie('gc_token', token, path='/', secure=self.__SECURE,
        #                              expires=expiration)
        #     self.render()

    @classmethod
    def get_user_or_none(cls, req):
        """
        actual method that return the user or None
        :param req:
        :return:
        """
        # if int(self.__AUTH_TYPE) == 1:
        token = req.headers.get("Authorization")
        if token:
            uid, ut = token.split("Token")[1].split("|")
        else:
            return None
        # NOTE: we do not use this
        # elif int(self.__AUTH_TYPE) == 2:
        # logging.debug("here")
        # scs = SecureCookieSerializer(self.__SECRET_KEY)
        # token = self.request.cookies.get('gc_token')
        # if token:
        #         uid, ut = scs.deserialize('token', token).split("|")
        #     else:
        #         return None
        # else:
        #     return None
        if uid and ut:
            user, timestamp = cls.__user_model.get_by_auth_token(long(uid), ut)
            if user:
                return user
            else:
                return None
        else:
            return None

    @classmethod
    def get_user(cls, req):
        """
        Get the user from the authorization.
        :return: the user or None
        """
        user = cls._get_user(req)
        if user:
            return user
        else:
            raise AuthenticationError("Auth error")

def user_required(handler):
    """
    Wrapper to check that auth is done
    :param handler:
    :return:
    """

    def wrapper(req, *args, **kwargs):
        user = GCAuth.get_user(req)
        if user is None:
            raise AuthenticationError
        req.user = user
        return handler(req, *args, **kwargs)

    return wrapper



