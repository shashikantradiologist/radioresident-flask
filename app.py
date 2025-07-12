from flask import Flask, render_template
app = Flask(__name__)

# ---------- ROUTES ----------
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

# ••• stub pages so sidebar doesn’t break •••
@app.route("/exam-sim")
def exam_sim():
    return render_template("stub.html", label="Exam Simulator (coming soon)")

@app.route("/notes")
def notes():
    return render_template("stub.html", label="System-wise Notes (coming soon)")

@app.route("/logbook")
def logbook():
    return render_template("stub.html", label="Logbook (coming soon)")

@app.route("/settings")
def settings():
    return render_template("stub.html", label="Settings (coming soon)")

# ✅ new content routes matching your index.html
@app.route("/content/abdomen-notes")
def abdomen_notes():
    return render_template("content/abdomen-notes.html")

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

# ------------------------------------------
@app.cli.command("routes")
def list_routes():
    from flask import url_for
    for rule in sorted(app.url_map.iter_rules(), key=lambda r: r.endpoint):
        print(f"{rule.endpoint:20s}  →  {rule.rule}")

if __name__ == "__main__":
    app.run(debug=True)
