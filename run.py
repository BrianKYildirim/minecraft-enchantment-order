from app import create_app, send_from_directory

app = create_app()

@app.route("/ads.txt")
def ads_txt():
    return send_from_directory(app.root_path, "ads.txt", mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
