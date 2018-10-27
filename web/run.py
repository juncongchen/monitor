#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Flask,request,render_template

from app import app


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    # 命令行运行才能指定端口： "python run.py runserver -h 127.0.0.1 -p 8080"

