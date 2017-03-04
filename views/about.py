from flask import Blueprint, render_template

aboutUs = Blueprint('aboutUs', __name__)

@aboutUs.route("/aboutUs", methods=['GET'])
def aboutUs_function():
    return render_template("aboutUs.html")
