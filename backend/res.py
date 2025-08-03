from flask import jsonify

def res(code, data=None, message=""):
  return jsonify({
    "data": data,
    "message": message,
  }), code