# -*- coding: utf-8 -*-

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    name = "nao"
    return render_template('home.html', name=name)



if __name__ == '__main__':
	app.run(debug=True)
    
    
    
    