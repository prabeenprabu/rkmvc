from flask import Flask, render_template, request
import re
import requests
from bs4 import BeautifulSoup as bs

app = Flask(__name__)


@app.route("/")
@app.route("/home")
@app.route("/index")
def index():
    return render_template("index.html")


# checking the input


@app.route("/check", methods=["GET", "POST"])
def check():
    if request.method == "POST":
        regNo = request.form["regNo"]
        pattern = "^\d{13}$"
        if re.search(pattern, regNo):
            # variables to get from my web site
            url = "https://rkmvc.ac.in/marksheet/ug/marksheet_ug.php?reg_num="
            response = ""
            regNo = str(regNo)
            try:
                response = requests.get(url + regNo)
            except Exception as e:
                return render_template("index.html")

            soup = bs(response.text, "html.parser")
            table = soup.find("table")

            if table == None:
                return render_template("index.html")
            else:
                name = (
                    soup.find_all("td", width="45%")[-1]
                    .get_text(strip=True)
                    .split("Candidate")[-1]
                )
                subjects = soup.find_all("td", width="666")
                ese = soup.find_all("td", width="49")
                tot = soup.find_all("td", width="51")
                regEnd = "End Of Statement"
                idx = 0
                # print(len(subjects))
                for i in range(0, len(subjects)):
                    subjects[i] = subjects[i].get_text()
                    ese[i] = ese[i].get_text()
                    tot[i] = tot[i].get_text()
                    if re.search(regEnd, subjects[i]):
                        idx = i

                mainSubjects = []
                mainEse = []
                total = []
                for i in range(1, idx):
                    mainSubjects.append(subjects[i])
                    mainEse.append(int(ese[i]))
                    total.append(tot[i])

                return render_template(
                    "data.html",
                    name=name,
                    regno=regNo,
                    subjects=mainSubjects,
                    ese=mainEse,
                    marks=total,
                    url=url + regNo,
                    idx=idx - 1,
                )

        else:
            return render_template("index.html")
    if request.method == "GET":
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
