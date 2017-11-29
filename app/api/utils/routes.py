"""
Module contains all the routes required by the API
"""
from app.api import API as restful
from app.api import views as funcs

restful.add_resource(funcs.Index, '/')
restful.add_resource(funcs.Register, '/auth/register')
restful.add_resource(funcs.Authentication, '/auth/login')
restful.add_resource(funcs.ResetPassword, '/auth/reset-password')
restful.add_resource(funcs.Events, '/events')
restful.add_resource(funcs.ManageEvent, '/events/<eventId>')
restful.add_resource(funcs.Rsvp, '/event/<eventId>/rsvp')
