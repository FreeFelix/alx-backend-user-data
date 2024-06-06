#!/usr/bin/env python3
""" 
Module of Index views
"""

from flask import jsonify, abort
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status() -> str:
    """
    GET /api/v1/status
    Endpoint to check the status of the API.
    
    Return:
      - JSON response with the status of the API.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/', strict_slashes=False)
def stats() -> str:
    """
    GET /api/v1/stats
    Endpoint to get the statistics of different objects.
    
    Return:
      - JSON response with the number of each object.
    """
    from models.user import User
    stats = {}
    stats['users'] = User.count()
    return jsonify(stats)


@app_views.route('/unauthorized', methods=['GET'], strict_slashes=False)
def unauthorized() -> str:
    """
    GET /api/v1/unauthorized
    Endpoint to trigger a 401 Unauthorized error.
    
    Return:
      - Aborts with a 401 status code.
    """
    abort(401)


@app_views.route('/forbidden', methods=['GET'], strict_slashes=False)
def forbidden() -> str:
    """
    GET /api/v1/forbidden
    Endpoint to trigger a 403 Forbidden error.
    
    Return:
      - Aborts with a 403 status code.
    """
    abort(403)
