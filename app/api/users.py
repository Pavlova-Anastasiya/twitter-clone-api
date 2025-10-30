from __future__ import annotations
from flask_smorest import Blueprint
from .. import db
from ..models import User, Follow
from .utils import get_current_user, ApiError
from ..schemas.users import ProfileSchema
from ..schemas.common import ResultSchema


blp = Blueprint("users", __name__, description="Users endpoints")


def _profile_dict(user: User) -> dict:
return {
"id": user.id,
"name": user.name,
"followers": [{"id": f.follower.id, "name": f.follower.name} for f in user.followers],
"following": [{"id": f.following.id, "name": f.following.name} for f in user.following],
}


@blp.route("/me", methods=["GET"])
@blp.response(200, ProfileSchema)
def me():
user = get_current_user()
return {"result": True, "user": _profile_dict(user)}


@blp.route("/<int:user_id>", methods=["GET"])
@blp.response(200, ProfileSchema)
def get_user(user_id: int):
target = db.session.get(User, user_id)
if not target:
raise ApiError("User not found")
return {"result": True, "user": _profile_dict(target)}


@blp.route("/<int:user_id>/follow", methods=["POST"])
@blp.response(200, ResultSchema)
def follow(user_id: int):
user = get_current_user()
if user.id == user_id:
raise ApiError("Cannot follow yourself")
target = db.session.get(User, user_id)
if not target:
raise ApiError("User not found")
exists = db.session.query(Follow).filter_by(follower_id=user.id, following_id=user_id).first()
if not exists:
db.session.add(Follow(follower_id=user.id, following_id=user_id))
db.session.commit()
return {"result": True}


@blp.route("/<int:user_id>/follow", methods=["DELETE"])
@blp.response(200, ResultSchema)
def unfollow(user_id: int):
user = get_current_user()
rel = db.session.query(Follow).filter_by(follower_id=user.id, following_id=user_id).first()
if rel:
db.session.delete(rel)
db.session.commit()
return {"result": True}