@app.route("/post_job", methods=["GET", "POST"])
@login_required
def post_job():
    if request.method == "POST":
        title = request.form.get("title")
        company = request.form.get("company")
        location = request.form.get("location")
        salary = request.form.get("salary")
        description = request.form.get("description")

        job = Job(
            title=title,
            company=company,
            location=location,
            salary=salary,
            description=description
        )

        db.session.add(job)
        db.session.commit()
        return redirect(url_for("index"))

    return render_template("post_job.html")