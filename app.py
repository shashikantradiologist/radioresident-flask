from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.utils import secure_filename
from docx import Document
import markdown2
import os

app = Flask(__name__)
app.secret_key = 'your_super_secret_key'  # Change this in production!

# === File Upload Config ===
UPLOAD_FOLDER = os.path.join("uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/question-bank")
def question_bank():          
    return render_template("question-bank.html")

@app.route("/case-of-day")
def case_of_day():
    return render_template("case-of-day.html")

@app.route("/flashcards")
def flashcards():
    return render_template("flashcards.html")

@app.route("/exam-sim")
def exam_sim():
    return render_template("stub.html", label="Exam Simulator (coming soon)")

@app.route("/notes")
def notes_list():
    systems = [
        {"name": "Thorax (Chest)", "slug": "chest"},
        {"name": "Abdomen", "slug": "abdomen"},
        {"name": "Neuro", "slug": "neuro"},
        {"name": "MSK", "slug": "msk"},
        {"name": "Spine", "slug": "spine"},
        {"name": "Head & Neck", "slug": "headneck"},
        {"name": "Genitourinary System", "slug": "genitourinary"}
    ]
    return render_template("notes_list.html", systems=systems)

@app.route("/logbook")
def logbook():
    return render_template("stub.html", label="Logbook (coming soon)")

@app.route("/settings")
def settings():
    return render_template("stub.html", label="Settings (coming soon)")

@app.route("/notes/<topic>")
def show_note(topic):
    md_file = f"content/{topic}.md"
    if not os.path.exists(md_file):
        abort(404, description=f"{topic}.md not found")

    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown2.markdown(md_content)

    return render_template("note_display.html", content=html_content, title=topic.title())

@app.route("/content/mnemonics")
def mnemonics():
    return render_template("content/mnemonics.html")

@app.route("/content/image-bank")
def image_bank():
    return render_template("content/image-bank.html")

@app.route("/content/planner")
def planner():
    return render_template("content/planner.html")

@app.route("/content/viva")
def viva():
    return render_template("content/viva.html")

@app.cli.command("routes")
def list_routes():
    from flask import url_for
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.endpoint):
        print(f"{rule.endpoint:20s}  →  {rule.rule}")

# =========================
# ADMIN ROUTES
# =========================

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USERNAME and request.form['password'] == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
def admin_home_redirect():
    return redirect(url_for('admin_dashboard'))

@app.route("/admin/dashboard")
def admin_dashboard():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))
    return render_template("admin_dashboard.html")

@app.route("/admin/upload", methods=['GET', 'POST'])
def upload_docx():
    if 'admin_logged_in' not in session:
        return redirect(url_for('admin_login'))

    if request.method == 'POST':
        file = request.files.get('docxfile')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Convert .docx to .md
            doc = Document(filepath)
            markdown_lines = [para.text for para in doc.paragraphs]
            markdown_text = '\n\n'.join(markdown_lines)

            md_filename = filename.rsplit('.', 1)[0] + ".md"
            md_path = os.path.join("content", md_filename)
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(markdown_text)

            flash("File uploaded and converted successfully!", "success")
            return redirect(url_for("upload_docx"))

    return render_template("admin_upload.html")

# =========================
if __name__ == "__main__":
    app.run(debug=True)
