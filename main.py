from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
app = Flask("__name__")
app.config["SECRET_KEY"] = "mff1910"

from wtforms import Form, FloatField, validators, SubmitField, BooleanField
bootstrap = Bootstrap(app)

#väLJA HUR MÅNGA BOLLAR OCH VIKT
#HYDRATION, JÄST, SALT

class Pizza(FlaskForm):
	bollar = FloatField("Antal Bollar", [validators.DataRequired()])
	bollar_vikt = FloatField("Vikt/boll gram", [validators.DataRequired()])
	hydration = FloatField("Hydration %", [validators.DataRequired()])
	jäst = FloatField("Jäst %", [validators.DataRequired()])
	salt = FloatField("Salt %", [validators.DataRequired()])
	regnmätare = BooleanField("Regnmätare (80g), för att mäta jäsning")
	submit = SubmitField()

class Surdeg(FlaskForm):
	antal_bröd = FloatField("Antal Bröd", [validators.DataRequired()])
	gram_mjöl = FloatField("Gram Mjöl/bröd", [validators.DataRequired()])
	hydration = FloatField("Hydration %", [validators.DataRequired()])
	surdeg = FloatField("Surdeg %", [validators.DataRequired()])
	salt = FloatField("Salt %", [validators.DataRequired()])
	regnmätare = BooleanField("Regnmätare (55g), för att mäta jäsning")
	submit = SubmitField()

result = {
	"Pizza":
	{"Mjöl": {"vikt": "", "icon": "<i class='fa-solid fa-wheat-awn'></i>"},
			"Vatten": {"vikt": "", "icon": '<i class="fa-solid fa-droplet"></i>'},
			"Jäst": {"vikt": "", "icon": '<i class="fa-solid fa-disease"></i>'},
			"Salt": {"vikt": "", "icon": "&#129474;"}},
	"Surdeg":
		{"Mjöl": {"vikt": "", "icon": "<i class='fa-solid fa-wheat-awn'></i>"},
			"Vatten": {"vikt": "", "icon": '<i class="fa-solid fa-droplet"></i>'},
			"Surdeg": {"vikt": "", "icon": '<i class="fa-solid fa-disease"></i>'},
			"Salt": {"vikt": "", "icon": "&#129474;"}}
		}

@app.route("/")
def home():
	return render_template("index.html")

@app.route("/pizza", methods=["POST", "GET"])
def pizza():
	form = Pizza(jäst=0.025, salt=2.7, hydration=66, bollar=3, bollar_vikt=250)
	if form.validate_on_submit():

		regnmätare_vikt = 0
		if form.regnmätare.data:
			regnmätare_vikt = 80
		sammanlagd_vikt = form.bollar.data *form.bollar_vikt.data + regnmätare_vikt
		mjöl_vikt = sammanlagd_vikt/((100+form.hydration.data+form.jäst.data+form.salt.data)/100)
		result["Pizza"]["Mjöl"]["vikt"] = str(int(mjöl_vikt))
		result["Pizza"]["Vatten"]["vikt"] = str(int(mjöl_vikt*(form.hydration.data/100)))
		result["Pizza"]["Jäst"]["vikt"] = f'{(mjöl_vikt * (form.jäst.data/100)):.2f}'
		result["Pizza"]["Salt"]["vikt"] = str(round(mjöl_vikt*(form.salt.data/100),1))
		return render_template("uträknare.html", form=form ,result=result["Pizza"], mode="result", bild="pizza_3.jpg", title="Pizza")

	return render_template("uträknare.html", form=form, mode="form", bild="pizza_3.jpg", title="Pizza")

@app.route("/sourdough", methods=["POST", "GET"])
def sourdough():
	form = Surdeg(antal_bröd=1, gram_mjöl=450, salt=2.2, hydration=72, surdeg=10)
	if form.validate_on_submit():
		regnmätare_vikt = 0
		regnmätare_mjöl = 0
		if form.regnmätare.data:
			regnmätare_mjöl = 55/((100+form.hydration.data+form.salt.data+form.surdeg.data)/100)
		mjöl_vikt = form.gram_mjöl.data + regnmätare_mjöl
		result['Surdeg']["Mjöl"]["vikt"] = str(int(mjöl_vikt))
		result['Surdeg']["Vatten"]["vikt"] = str(int(mjöl_vikt*(form.hydration.data/100)))
		result['Surdeg']["Surdeg"]["vikt"] = str(int(mjöl_vikt * (form.surdeg.data/100)))
		result['Surdeg']["Salt"]["vikt"] = str(round(mjöl_vikt*(form.salt.data/100),1))
		return render_template("uträknare.html", form=form ,result=result["Surdeg"], mode="result", bild="sourdough.jpg", title="Surdeg")
	return render_template("uträknare.html", form=form, bild="sourdough.jpg", title="Surdeg")

#Favicon, namn dokument


if __name__ == "__main__":
	app.run(debug=True)

