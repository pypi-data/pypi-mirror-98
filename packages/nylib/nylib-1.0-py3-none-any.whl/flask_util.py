from flask import Flask, render_template, request, jsonify, Blueprint


def getRequestParam(paramKey):
    v = request.form.get(paramKey)
    if v == None:
        v = request.args.get(paramKey)
    return v
