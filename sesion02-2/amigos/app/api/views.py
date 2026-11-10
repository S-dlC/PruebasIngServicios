from flask import request, abort, jsonify
from .. import db
from . import api
from ..models import Amigo


def amigo_a_dict(amigo):
    "Convierte un objeto Amigo en un diccionario listo para jsonify()"
    return {"id": amigo.id, "name": amigo.name,
            "lati": amigo.lati, "longi": amigo.longi,
            "device": amigo.device}


@api.route("/amigos")
def list_amigos():
    """
    Retorna un JSON con la lista de amigos.
    """
    return jsonify([amigo_a_dict(a) for a in Amigo.query.all()])


@api.route("/amigo/<int:id>")
def get_amigo(id):
    amigo = Amigo.query.get_or_404(id)
    return jsonify(amigo_a_dict(amigo))


@api.route("/amigo/byName/<name>")
def get_amigo_by_name(name):
    amigo = Amigo.query.filter_by(name=name).first()
    if not amigo:
        abort(404, "No se encuentra ningún amigo con ese nombre")
    return jsonify(amigo_a_dict(amigo))


@api.route("/amigo/<int:id>", methods=["PUT"])
def edit_amigo(id):
    amigo = Amigo.query.get_or_404(id)
    if not request.json:
        abort(422, "No se ha enviado JSON")

    name = request.json.get("name")
    lati = request.json.get("lati")
    longi = request.json.get("longi")
    device = request.json.get("device")

    if name:
        amigo.name = name
    if lati:
        amigo.lati = lati
    if longi:
        amigo.longi = longi
    # device admite cadena vacía, así que se compara con None
    if device is not None:
        amigo.device = device

    db.session.commit()
    return jsonify(amigo_a_dict(amigo))


@api.route("/amigo/<int:id>", methods=["DELETE"])
def delete_amigo(id):
    """
    Elimina el amigo cuyo id recibe como parámetro.
    """
    amigo = Amigo.query.get_or_404(id)
    db.session.delete(amigo)
    db.session.commit()
    return ('', 204)


@api.route("/amigos", methods=["POST"])
def new_amigo():
    if not request.json:
        abort(422, "No se ha enviado JSON")

    name = request.json.get("name")
    if not name:
        abort(422, "El JSON no incluye el campo 'name'")
    if Amigo.query.filter_by(name=name).first():
        abort(422, "Ya existe un amigo con ese nombre")

    lati = request.json.get("lati", "0")
    longi = request.json.get("longi", "0")
    device = request.json.get("device")      # None si no viene

    amigo = Amigo(name=name, lati=lati, longi=longi, device=device)
    db.session.add(amigo)
    db.session.commit()
    return jsonify(amigo_a_dict(amigo))


@api.route("/devices")
def list_devices():
    """
    Lista de todos los device que no son NULL ni cadena vacía.
    """
    amigos = Amigo.query.filter(Amigo.device.isnot(None),
                                Amigo.device != "").all()
    return jsonify([a.device for a in amigos])