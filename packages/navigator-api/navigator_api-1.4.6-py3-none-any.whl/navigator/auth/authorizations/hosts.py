""" Authorization based on HOSTS lists."""

from .base import BaseAuthzHandler
from navigator.conf import HOSTS
from aiohttp import web
import logging

class authz_hosts(BaseAuthzHandler):
    """
    BasicHosts.
       Use for basic Host authorization, simply creating a list of allowed hosts
    """

    async def check_authorization(self, request: web.Request) -> bool:
        if request.host in HOSTS:
            #logging.debug('Authorized based on HOST Authorization')
            return True
        try:
            if request.headers["origin"] in HOSTS:
                #logging.debug('Authorized based on HOST Authorization')
                return True
        except KeyError:
            return False
        return False
