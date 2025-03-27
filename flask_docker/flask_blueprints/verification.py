from flask import Blueprint, render_template, request, session, flash
from buzzy_bee_db.account.verification_notification import update_verification_and_weekly_updates

verification = Blueprint('verification', __name__,
                        template_folder='templates')

@verification.route("/verify", methods="get")
def verify():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        update_verification_and_weekly_updates(user_id)
        return render_template("verification_complete.html")