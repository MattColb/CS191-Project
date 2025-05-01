import datetime
import io
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
from flask import send_file
import matplotlib.dates as mdates

#Get a student progress graph based on class info
def create_student_progress_graph(new_info):
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