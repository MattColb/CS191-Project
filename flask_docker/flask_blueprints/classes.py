from flask import Blueprint, render_template, request, session, flash, url_for, redirect
from buzzy_bee_db.account.stu_account import get_stu_accounts_teacher
from buzzy_bee_db.classes_content.classes_content import *
import datetime

classes = Blueprint('classes', __name__,
                        template_folder='templates')

@classes.route("/Class", methods=["POST"])
def add_class():
    if request.method == "POST":
        teacher_id = session.get("user_id")
        class_name = request.form.get("class_name")
        
        #Post class with class name, class teacher
        create_class(teacher_id, class_name)

        return redirect(url_for("login_register.teacher_account"))

@classes.route("/Class/<class_id>", methods=["POST", "GET"])
def get_class(class_id):
    if request.method == "GET":
        class_info = get_class_information(class_id).class_information
        #Remove content older than current date
        current_time = datetime.datetime.utcnow().isoformat()
        content = get_class_content(class_id).content_information
        content = [c for c in content if c.get('due_date') >= current_time]
        sub_accounts=get_stu_accounts_teacher(session.get("user_id")).stu_accounts
        sub_accounts = [sa for sa in sub_accounts if sa.get("student_id") in class_info.get("students")]

        return render_template("class.html", class_info=class_info, sub_accounts = sub_accounts, class_id=class_id, content=content)

@classes.route("/Class/add_students", methods = ["POST"])
def add_students_to_class():
    if request.method == "POST":
        class_id = request.form.get("class_id")
        student_ids = request.form.getlist("student_ids")
        response = add_students_to_class_db(class_id, student_ids)
        if response.success == True:
            return redirect(url_for("login_register.teacher_account"))
        else:
            return redirect(url_for("login_register.teacher_account"))

@classes.route("/Class/<class_id>/Content", methods=["POST", "GET"])
def manage_class_content(class_id):
    if request.method == "GET":
        content = get_class_content(class_id).content_information
        #Adding content here doesn't work :3
        return render_template("content_archive.html", content=content, user_type="teacher")
    if request.method == "POST":
        teacher_id = session.get("user_id")
        video_link = request.form.get("video_link")

        if "embed" not in video_link:
            v = video_link.split("/")
            last_item = v.pop()
            v.append("embed")
            v.append(last_item)
            video_link = "/".join(v)
        
        due_date = request.form.get("due_date")
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").isoformat()
        title = request.form.get("title")

        response = add_class_content(teacher_id, class_id, video_link, due_date, title)
        if response.success == True:
            return redirect(url_for("classes.get_class", class_id=class_id))
        else:
            return redirect(url_for("classes.get_class", class_id=class_id))

#Need to flash this one out
@classes.route("/Content/<content_id>", methods=["GET"])
def view_content(content_id):
    if request.method == "GET":
        content_information = get_content_information(content_id).content_information
        return render_template("content.html", content=content_information)
    

@classes.route("/Class/<class_id>/Students/Remove", methods=["POST"])
def remove_students(class_id):
    if request.method == "POST":
        remove = request.form.getlist("student_ids")
        response = remove_students_db(class_id, remove)
        return redirect(url_for("classes.get_class", class_id=class_id))