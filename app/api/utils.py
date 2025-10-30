from __future__ import annotations
from flask import request
from ..models import User
from .. import db


class ApiError(Exception):
pass


def get_current_user() -> User:
api_key = request.headers.get("api-key") or request.headers.get("API-KEY")
if not api_key:
raise ApiError("Missing 'api-key' header")
user = db.session.query(User).filter_by(api_key=api_key).first()
if not user:
raise ApiError("Invalid api-key")
return user