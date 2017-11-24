"""
Module contains all the routes required by the API
"""
from app import API as restful
from app import views as funcs

restful.add_resource(funcs.Register, '/api/auth/register')
restful.add_resource(funcs.Authentication, '/api/auth/login')
restful.add_resource(funcs.ResetPassword, '/api/auth/reset-password')
restful.add_resource(funcs.CreateEvent, '/api/events')
restful.add_resource(funcs.Event, '/api/events/<eventId>')
restful.add_resource(funcs.Rsvp, '/api/event/<eventId>/rsvp')
