# Простая раздача загруженных файлов в dev-режиме
from flask import send_from_directory, current_app


def register_media_route(app):
@app.route('/media/<path:filename>')
def media(filename):
return send_from_directory(current_app.config["UPLOAD_DIR"], filename)