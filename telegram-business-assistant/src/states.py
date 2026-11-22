"""Finite-state flow for collecting a structured enquiry."""

from aiogram.fsm.state import State, StatesGroup


class RequestFlow(StatesGroup):
    waiting_contact = State()
    waiting_details = State()
