from flask import Blueprint, render_template, request, session, flash
from buzzy_bee_db.account.verification_notification import update_verification_and_weekly_updates

verification = Blueprint('verification', __name__,
                        template_folder='templates')

#Verify the user from the user id in the link
@verification.route("/verify", methods=["GET"])
def verify():
    if request.method == "GET":
        user_id = request.args.get("user_id")
        update_verification_and_weekly_updates(user_id)
        return render_template("verification_complete.html")