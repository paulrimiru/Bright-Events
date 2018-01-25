"""
Module contains all the routes required by the API
"""

from app.api_v2 import API as restful
from app.api_v2 import views as funcs

restful.add_resource(funcs.RegisterUser, '/auth/register')
restful.add_resource(funcs.LoginUser, '/auth/login')
restful.add_resource(funcs.LogoutUser, '/auth/logout')
restful.add_resource(funcs.Events, '/events')
restful.add_resource(funcs.PasswordReset, '/auth/reset-password')
restful.add_resource(funcs.ManageEvents, '/events/<event_id>')
restful.add_resource(funcs.ManageRsvp, '/event/<event_id>/rsvp')
restful.add_resource(funcs.FilterEvents, '/events/filter')
