from __future__ import annotations
import os
from werkzeug.utils import secure_filename
from flask import request, current_app
from flask_smorest import Blueprint
from .. import db
from ..models import Media
from .utils import get_current_user, ApiError
from ..schemas.medias import MediaUploadResponse




blp = Blueprint("medias", __name__, description="Media upload")




@blp.route("", methods=["POST"])
@blp.response(200, MediaUploadResponse)
def upload():
user = get_current_user()
if "file" not in request.files:
raise ApiError("Form-data must include 'file'")
file = request.files["file"]
if file.filename == "":
raise ApiError("Empty filename")
filename = secure_filename(file.filename)
upload_dir = current_app.config["UPLOAD_DIR"]
os.makedirs(upload_dir, exist_ok=True)
path = os.path.join(upload_dir, filename)
# avoid overwrite
base, ext = os.path.splitext(filename)
i = 1
while os.path.exists(path):
filename = f"{base}_{i}{ext}"
path = os.path.join(upload_dir, filename)
i += 1
file.save(path)
media = Media(filename=filename, path=f"/media/{filename}", content_type=file.mimetype, owner_id=user.id)
db.session.add(media)
db.session.commit()
return {"result": True, "media_id": media.id}