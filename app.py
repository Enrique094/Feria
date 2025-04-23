from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/About")
def pene():
    return render_template("About.html")

@app.route("/register")
def register():
    return render_template("register.html") 

@app.route("/login", methods=["GET", "POST"])
def login():
    return redirect("/")




if __name__ == "__main__":
    app.run(debug=True)