import os

from flask import Flask, jsonify, request, send_from_directory

from alignment_logic import (
    get_symbol,
    global_alignment,
    local_alignment,
    parse_sequence,
)

MAX_SEQUENCE_LENGTH = 5000

app = Flask(__name__, static_folder="static")


class BadRequest(Exception):
    pass


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    return jsonify(error=str(error)), 400


@app.after_request
def allow_cross_origin(response):
    """
    Lets the page be hosted apart from the API (static host + API host).
    Safe to open up: the API is stateless, reads no cookies and no auth.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


def get_sequence(payload, field):
    """
    Reads a sequence from an uploaded file (multipart) or a JSON/form field.
    Both accept raw text or FASTA.
    """
    uploaded = request.files.get(field)
    raw = uploaded.read().decode("utf-8") if uploaded else payload.get(field)

    if not raw:
        raise BadRequest(f"missing sequence '{field}'")

    seq = parse_sequence(raw)

    if not seq:
        raise BadRequest(f"sequence '{field}' is empty")
    if len(seq) > MAX_SEQUENCE_LENGTH:
        raise BadRequest(
            f"sequence '{field}' exceeds {MAX_SEQUENCE_LENGTH} characters"
        )

    return seq


def get_int(payload, field, default):
    value = payload.get(field, default)
    try:
        return int(value)
    except (TypeError, ValueError):
        raise BadRequest(f"'{field}' must be an integer")


@app.get("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.get("/health")
def health():
    return jsonify(status="ok")


@app.route("/align", methods=["POST", "OPTIONS"])
def align():
    if request.method == "OPTIONS":
        return "", 204

    payload = request.get_json(silent=True) or request.form

    seq1 = get_sequence(payload, "seq1")
    seq2 = get_sequence(payload, "seq2")

    match = get_int(payload, "match", 5)
    mismatch = get_int(payload, "mismatch", -1)
    gap = get_int(payload, "gap", -3)

    mode = str(payload.get("mode", "global")).lower()

    if mode == "global":
        align1, align2, score = global_alignment(seq1, seq2, match, mismatch, gap)
    elif mode == "local":
        align1, align2, score = local_alignment(seq1, seq2, match, mismatch, gap)
    else:
        raise BadRequest("'mode' must be 'global' or 'local'")

    return jsonify(
        mode=mode,
        score=score,
        alignment1=align1,
        alignment2=align2,
        symbols=get_symbol(align1, align2),
        length=len(align1),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
