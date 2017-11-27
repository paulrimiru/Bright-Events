"""
Module contains all the routes required by the API
"""
from app import API as restful
from app import views as funcs

restful.add_resource(funcs.Register, '/api/v1/auth/register')
restful.add_resource(funcs.Authentication, '/api/v1/auth/login')
restful.add_resource(funcs.ResetPassword, '/api/v1/auth/reset-password')
restful.add_resource(funcs.CreateEvent, '/api/v1/events')
restful.add_resource(funcs.Event, '/api/v1/events/<eventId>')
restful.add_resource(funcs.Rsvp, '/api/v1/event/<eventId>/rsvp')
