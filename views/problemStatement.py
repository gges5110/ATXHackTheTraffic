from flask import Blueprint, render_template

problemStatement = Blueprint('problemStatement', __name__)

@problemStatement.route("/problemStatement")
def problemStatement_function():
    return render_template("problemStatement.html")
