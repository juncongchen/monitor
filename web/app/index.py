#coding:utf-8

from flask import Flask,render_template,url_for
from app import app
import pymysql
import json


@app.route('/')
def hello():
    # return "hello"
    return render_template('index.html')

