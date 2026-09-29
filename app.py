"""Mission Control web application for searching words in local documents."""

from __future__ import annotations

import os
import secrets
from pathlib import Path

from flask import Flask, jsonify, render_template, request
from werkzeug.exceptions import RequestEntityTooLarge

from utils.finder import SearchError, search_document

BASE_DIR = Path(__file__).resolve().parent
SAMPLE_FILE = BASE_DIR / "data" / "sample-mission-log.txt"
MAX_UPLOAD_BYTES = 16 * 1024 * 1024


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_mapping(
        MAX_CONTENT_LENGTH=MAX_UPLOAD_BYTES,
        SECRET_KEY=os.environ.get("SOB_WORDS_SECRET") or secrets.token_hex(32),
        JSON_SORT_KEYS=False,
    )
    if test_config:
        app.config.update(test_config)

    @app.get("/")
    def index():
        return render_template("index.html", version="2.0.0")

    @app.post("/api/search")
    def search():
        query = request.form.get("query", "").strip()
        if not query:
            return jsonify(error="Enter a word or phrase to begin the scan."), 400
        if len(query) > 120:
            return jsonify(error="The search term must contain 120 characters or fewer."), 400

        source = request.form.get("source", "sample")
        uploaded = request.files.get("file")
        try:
            limit = min(max(int(request.form.get("limit", "50")), 1), 200)
        except ValueError:
            limit = 50
        options = {
            "case_sensitive": request.form.get("caseSensitive") == "true",
            "whole_word": request.form.get("wholeWord") == "true",
            "limit": limit,
        }

        try:
            if source == "upload":
                if not uploaded or not uploaded.filename:
                    return jsonify(error="Choose a document before starting the scan."), 400
                result = search_document(uploaded.read(), uploaded.filename, query, **options)
            else:
                result = search_document(SAMPLE_FILE.read_bytes(), SAMPLE_FILE.name, query, **options)
        except SearchError as exc:
            return jsonify(error=str(exc)), 400
        return jsonify(result)

    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(_error):
        return jsonify(error="This document exceeds the 16 MB mission limit."), 413

    @app.get("/health")
    def health():
        return jsonify(status="nominal", version="2.0.0")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
