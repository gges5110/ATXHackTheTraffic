from flask import Blueprint, render_template

heatmap = Blueprint('heatmap', __name__)

@heatmap.route("/heatmap", methods=['GET'])
def heatmap_function():
    return render_template("heatmap.html")
