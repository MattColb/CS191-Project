import datetime
from PIL import Image
import io
import base64

def create_image_bytes(image_bytes):
    image = Image.open(image_bytes)
    sizes = image.size
    image = image.resize((int(sizes[0]*.6), int(sizes[1]*.6)))
    image_bytes = io.BytesIO()
    image.save(image_bytes, format="png")
    image_str = base64.b64encode(image_bytes.getvalue()).decode("utf-8")
    image_final = f"data:image/png;base64,{image_str}"
    return image_final


def create_html(current_week_info, student_name, previous_snapshot, image_bytes):
    if previous_snapshot != None and len(previous_snapshot) != 0:
        previous_snapshot = previous_snapshot[0]
    else:
        previous_snapshot = {"MATH_answered":0, "SPELLING_answered":0}

    
    try:
        math_percentage = (current_week_info["MATH_answered"]/previous_snapshot["MATH_answered"])-1
    except:
        math_percentage = 1

    try:
        spelling_percentage = (current_week_info["SPELLING_answered"]/previous_snapshot["SPELLING_answered"])-1
    except:
        spelling_percentage = 1
    
    mn = 1000
    mn_label = None
    for k, v in current_week_info.items():
        if "percentage" in k and v < mn:
            mn_label = k.split("_")[0].lower()
            mn = v
    

    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BuzzyBee Weekly Snapshot</title>
    <style>
        body {{
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #fcf8e3;
            color: #333;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            box-shadow: 0 0 15px rgba(0,0,0,0.1);
            border-radius: 15px;
        }}
        .header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-bottom: 15px;
            border-bottom: 3px datheyd #ffd54f;
        }}
        .logo {{
            width: 80px;
            height: 80px;
            background-color: #ffd54f;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }}
        .logo-inner {{
            width: 70px;
            height: 70px;
            background-color: #fff;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: #333;
            position: relative;
        }}
        .logo-bee {{
            font-size: 24px;
            position: absolute;
        }}
        .title {{
            font-size: 28px;
            font-weight: bold;
            color: #f9a825;
            text-align: center;
            flex-grow: 1;
        }}
        .date {{
            font-weight: bold;
            color: #666;
        }}
        .student-name {{
            font-size: 24px;
            font-weight: bold;
            margin-top: 15px;
            color: #5d4037;
        }}
        .snapshot-image {{
            width: 100%;
            height: 300px;
            margin: 20px 0;
            background-color: #f5f5f5;
            border: 3px solid #ffd54f;
            border-radius: 10px;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .subject-section {{
            background-color: #e8f5e9;
            padding: 15px;
            margin: 20px 0;
            border-radius: 10px;
            border-left: 5px solid #81c784;
        }}
        .subject-title {{
            font-weight: bold;
            font-size: 20px;
            color: #2e7d32;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }}
        .subject-icon {{
            margin-right: 10px;
            font-size: 24px;
        }}
        .subject-content {{
            padding-left: 15px;
        }}
        .highlight {{
            background-color: #fff9c4;
            padding: 2px 5px;
            border-radius: 3px;
        }}
        .recommendation {{
            background-color: #e3f2fd;
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            border-left: 5px solid #64b5f6;
        }}
        .recommendation-title {{
            font-weight: bold;
            font-size: 22px;
            color: #1565c0;
            margin-bottom: 10px;
        }}
        .footer {{
            text-align: center;
            margin-top: 30px;
            padding-top: 10px;
            border-top: 3px datheyd #ffd54f;
            font-size: 14px;
            color: #666;
        }}
        .bee-trail {{
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }}
        .bee {{
            font-size: 18px;
            margin: 0 5px;
        }}
        .download-section {{
            text-align: center;
            margin: 30px 0 10px;
        }}
        .download-btn {{
            background-color: #ffd54f;
            color: #5d4037;
            border: none;
            padding: 12px 25px;
            font-size: 16px;
            font-weight: bold;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 3px 5px rgba(0,0,0,0.1);
            font-family: 'Comic Sans MS', 'Chalkboard SE', sans-serif;
            display: inline-flex;
            align-items: center;
            justify-content: center;
        }}
        .download-btn:hover {{
            background-color: #ffb300;
            transform: translateY(-2px);
            box-shadow: 0 5px 8px rgba(0,0,0,0.15);
        }}
        .download-btn:active {{
            transform: translateY(0);
            box-shadow: 0 2px 3px rgba(0,0,0,0.1);
        }}
        .download-icon {{
            margin-right: 8px;
            font-size: 18px;
        }}
        .unsubscribe {{
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #999;
            text-align: center;
        }}
        .unsubscribe a {{
            color: #666;
            text-decoration: underline;
        }}
        @media print {{
            body {{
                background-color: white;
            }}
            .container {{
                box-shadow: none;
                max-width: 100%;
            }}
            .download-section {{
                display: none;
            }}
            .unsubscribe {{
                display: none;
            }}
        }}
    </style>
    </head>
    <body>
    <div class="container">
        <div class="header">
            <div class="logo">
                <div class="logo-inner">
                    <span class="logo-bee">🐝</span>
                </div>
            </div>
            <div class="title">Weekly Learning Snapshot</div>
            <div class="date">{datetime.datetime.now().strftime("%B %d, %Y")}</div>
        </div>
        
        <div class="student-name">{student_name}</div>
        
        <div class="snapshot-image">
            <img src="{create_image_bytes(image_bytes)}" alt="{student_name}'s weekly progress showing their classroom activities and achievements in mathematics, spelling and grammar">
        </div>
        
        <div class="subject-section">
            <div class="subject-title">
                <span class="subject-icon">🔢</span>
                Mathematics
            </div>
            <div class="subject-content">
                <p><strong>{student_name} did well this week! they completed {current_week_info["MATH_answered"]} problems with {round(current_week_info["MATH_percentage"]*100, 2)}% accuracy, a {abs(round(math_percentage*100,2))}% {"increase" if math_percentage > 0 else "decrease"} in answering questions from last week.</strong></p>
            </div>
        </div>
        
        <div class="subject-section">
            <div class="subject-title">
                <span class="subject-icon">📝</span>
                Spelling
            </div>
            <div class="subject-content">
                <p><strong>{student_name} did well this week! they completed {current_week_info["SPELLING_answered"]} problems with {round(current_week_info["SPELLING_percentage"]*100, 2)}% accuracy, a {abs(round(spelling_percentage*100,2))}% {"increase" if spelling_percentage > 0 else "decrease"} in answering questions from last week.</strong></p>
            </div>
        </div>
        
        <div class="subject-section">
            <div class="subject-title">
                <span class="subject-icon">📚</span>
                Grammar
            </div>
            <div class="subject-content">
                <p><strong>This subject is currently under contstruction</strong></p>
            </div>
        </div>
        
        <div class="recommendation">
            <div class="recommendation-title">Recommendations & Feedback</div>
            <p>{student_name} has shown excellent progress across all subjects this week! To continue their growth, we recommend focusing in on {mn_label}</p>
            <p>{student_name}'s enthusiasm for learning continues to shine through in their participation. Keep up the great work!</p>
        </div>
        
        <div class="download-section">
            <button id="downloadPDF" class="download-btn" onclick="preparePrint()">
                <span class="download-icon">📥</span> Save this report
            </button>
        </div>
        
        <div class="bee-trail">
            <div class="bee">🐝</div>
            <div class="bee">🐝</div>
            <div class="bee">🐝</div>
        </div>
        
        <div class="footer">
            <p>BuzzyBee Learning - Helping children discover the joy of learning!</p>
            <p>Questions? Contact us at <strong>teactheirs@buzzybee.com</strong></p>
            
            <div class="unsubscribe">
                <p>You're receiving this email because you're registered with BuzzyBee Learning's weekly progress reports.</p>
                <p><a href="#">Update your preferences</a> | <a href="#">Unsubscribe</a> | <a href="#">Privacy Policy</a></p>
                <p>© 2025 BuzzyBee Learning. All rights reserved.</p>
                <p>1806 Main Street, San Diego, CA 90845</p>
            </div>
        </div>
    </div>


    <script>
        function preparePrint() {{
            // Add student name to filename
            const studentName = document.querySelector('.student-name').innerText.trim();
            const date = document.querySelector('.date').innerText.trim();
            const sanitizedName = studentName.replace(/\s+/g, '_');
            const sanitizedDate = date.replace(/,\s+/g, '_');
            const filename = `BuzzyBee_Report_${{sanitizedName}}_${{sanitizedDate}}`;
            
            // Set a download attribute with the filename (for browsers that support HTML saving)
            document.title = filename;
            
            // Use the print functionality which allows saving as PDF
            window.print();
        }}
        
        // Downloading as HTML if needed
        document.addEventListener('DOMContentLoaded', function() {{


        }});
    </script>
    </body>
    </html>


    """