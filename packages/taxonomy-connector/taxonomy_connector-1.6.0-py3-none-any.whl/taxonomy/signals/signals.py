"""
This module contains taxonomy related signals.
"""


from django.dispatch import Signal

UPDATE_COURSE_SKILLS = Signal(providing_args=["course_uuid"])
