"""
Module contains all the routes required by the API
"""

from app.api_v1 import API as restful
from app.api_v1 import views as funcs

restful.add_resource(funcs.Index, '/')
restful.add_resource(funcs.Register, '/auth/register')
restful.add_resource(funcs.Authentication, '/auth/login')
restful.add_resource(funcs.Logout, '/auth/logout')
restful.add_resource(funcs.ResetPassword, '/auth/reset-password')
restful.add_resource(funcs.Events, '/events')
restful.add_resource(funcs.ManageEvent, '/events/<event_id>')
restful.add_resource(funcs.Rsvp, '/event/<event_id>/rsvp')
restful.add_resource(funcs.ManageRsvp, '/manageRsvp')
