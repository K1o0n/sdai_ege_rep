from flask import Flask, render_template

app = Flask(__name__)

@app.route('/group')
def group():
    return render_template('group.html')

if __name__ == '__main__':
    app.run(debug=True)
