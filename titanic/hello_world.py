from flask import Flask, render_template
import jinja2

app=Flask(__name__)
@app.route('/')
def hello_world():
    name = "Hello World!"
    date = 'July 2016'

    return render_template('index.html', name=name,
                           date=date)



if __name__ == '__main__' :

    app.run()

