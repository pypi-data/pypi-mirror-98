# -*- coding: utf-8 -*-
#  _     _       _
# | |   (_)  _  (_)
# | |  _ _ _| |_ _  ____ _____
# | |_/ ) (_   _) |/ ___|____ |
# |  _ (| | | |_| ( (___/ ___ |
# |_| \_)_|  \__)_|\____)_____|
#
# kitica DevicePool API
# Created by    : Joshua Kim Rivera
# Date          : March 8 2021 13:43 PST
#
from .service import Service
from webargs import fields, validate
from webargs.flaskparser import use_kwargs
from flask_socketio import emit


class Servers(Service):
    """ kitica Devices Endpoint.

    ...

    Methods
    ----------
    GET
        Handles the GET Requests to /hosts/servers.
        Fetches the servers manifest as a list.
    POST
        Handles POST Request to /hosts/servers.
        Inserts new server to the database.
    """
    args = {
        'server': fields.String(required=False)
    }

    def get(self):
        """ Servers GET Method Handler.

        Handles GET Request made to /hosts/servers endpoint.

        Returns
        ----------
        data : list
            Returns the list of servers whitelisted by the API.
        """
        return Service.get_servers()

    @use_kwargs(args)
    def post(self, server):
        """ Servers POST Method Handler.

        Handles POST Request made to /hosts/servers endpoint.

        Parameters
        ----------
        server : str
            The server to be whitelisted, must not be existing.
        """
        servers = Service.get_servers()
        if server not in servers:
            query = f'INSERT INTO servers (serverAddress) VALUES(\"{server}\");'
            self._update(query)
            return {
                'message': f'Added {server} to allowed hosts.',
                'statusCode': 1
            }
        else:
            return {
                'message': 'Host already exists.',
                'statusCode': -1
            }
