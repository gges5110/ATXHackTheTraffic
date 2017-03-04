from flask import Blueprint, render_template

historyStats = Blueprint('historyStats', __name__)

@historyStats.route("/historyStats", methods=['GET'])
def historyStats_function():
    return render_template("historyStats.html")
