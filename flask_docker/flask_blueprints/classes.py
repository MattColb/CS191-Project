import matplotlib
matplotlib.use('Agg')  
from flask import Blueprint, render_template, request, session, flash, url_for, redirect, send_file
from buzzy_bee_db.account.stu_account import get_stu_accounts_teacher
from buzzy_bee_db.classes_content.classes_content import *
from buzzy_bee_db.classes_content.student_content import *
from buzzy_bee_db.account.stu_account import get_stu_accounts_list
from buzzy_bee_db.weekly_snapshot.weekly_snapshot import get_snapshots_list
import datetime
import urllib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import io

classes = Blueprint('classes', __name__,
                        template_folder='templates')

@classes.route("/Teacher/Remove/Students", methods=["POST"])
def remove_student():
    if request.method == "POST":
        teacher_id = session.get("user_id")
        students = request.form.getlist("student_ids")

        remove_students_teacher_db(teacher_id, students)

        return redirect(url_for("login_register.teacher_account"))
        
    pass

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
        return render_template("content_archive.html", content=content, user_type="teacher", class_id=class_id)
    if request.method == "POST":
        teacher_id = session.get("user_id")
        video_link = request.form.get("video_link")

        #Embeded video not working

        if "v=" in video_link:
            video_id = video_link.split("=")[-1]
        else:
            v = video_link.split("/")
            last_item = v.pop()
            video_id = last_item.split("?")[0]
        
        due_date = request.form.get("due_date")
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").isoformat()
        title = request.form.get("title")

        response = add_class_content(teacher_id, class_id, video_id, due_date, title)
        if response.success == True:
            return redirect(url_for("classes.get_class", class_id=class_id))
        else:
            return redirect(url_for("classes.get_class", class_id=class_id))

#Need to flash this one out
@classes.route("/Content/<content_id>", methods=["GET"])
def view_content(content_id):
    if request.method == "GET":
        content_information = get_content_information(content_id).content_information
        video_id = content_information["video_url"].split("=")[-1]
        return render_template("content.html", content=content_information, video_id=video_id)
    

@classes.route("/Class/<class_id>/Students/Remove", methods=["POST"])
def remove_students(class_id):
    if request.method == "POST":
        remove = request.form.getlist("student_ids")
        response = remove_students_db(class_id, remove)
        return redirect(url_for("classes.get_class", class_id=class_id))
    

@classes.route("/Student/Content")
def get_student_content():
    sub_account_id = session.get("sub_account_id")
    classes = get_student_classes(sub_account_id).class_information
    classes = [c.get("class_id") for c in classes]
    content = get_student_content_db(classes).content_information
    current_time = datetime.datetime.utcnow().isoformat()
    content = [c for c in content if c.get('due_date') >= current_time]

    return render_template("content_archive.html", content=content, user_type="student", class_id="")
    pass

@classes.route("/Class/Progress/<class_id>", methods=["GET"])
def get_class_progress_visual(class_id):
    resp = get_class_information(class_id)
    students = []
    if resp.success:
        students = resp.class_information.get("students")
        snapshots = get_snapshots_list(students).responses

    date_info = dict()
    for snapshot in snapshots:
        timestamp = snapshot["timestamp_utc"]
        date = datetime.datetime.fromisoformat(timestamp).date().isoformat()
        if date_info.get(date) == None:
            date_info[date] = {"score_in_math":[], "score_in_spelling":[]}
        date_info[date]["score_in_math"].append(snapshot.get("score_in_math", 0))
        date_info[date]["score_in_spelling"].append(snapshot.get("score_in_spelling", 0))

    new_info = []
    for date, vals in date_info.items():
        d = {"date":date}
        if len(vals.get("score_in_math", [])) != 0:
            d["score_in_math"] = sum(vals.get("score_in_math"))/len(vals.get("score_in_math"))
        else:
            d["score_in_math"] = 0
        if len(vals.get("score_in_spelling", [])) != 0:
            d["score_in_spelling"] = sum(vals.get("score_in_spelling"))/len(vals.get("score_in_spelling"))
        else:
            d["score_in_spelling"] = 0

        new_info.append(d)

    new_info = sorted(new_info, key=lambda d: d["date"])


    fig, ax = plt.subplots()

    dates = [datetime.datetime.fromisoformat(snapshot.get("date")) for snapshot in new_info]
    math = [snapshot.get("score_in_math", 0) for snapshot in new_info]
    spelling = [snapshot.get("score_in_spelling", 0) for snapshot in new_info]

    ax.plot(dates, math, label='Math')
    ax.plot(dates, spelling, label='Spelling')

    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    ax.set_title('Student Progress over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Score Rating')

    # Add a legend
    ax.legend()

    #Save like we did for clocks
    # Rotate date labels for better readability
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    img_bytes = io.BytesIO()
    plt.savefig(img_bytes, format="png", bbox_inches="tight", dpi=200)
    plt.close()

    img_bytes.seek(0)  # Move to the beginning of the byte stream
    return send_file(img_bytes, mimetype="image/png")

if __name__ == "__main__":
    get_class_progress_visual("d6a14d1f-3071-414a-9227-208f1b103091")