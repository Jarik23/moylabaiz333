import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm, RecaptchaField
from PIL import Image
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
app = Flask(__name__)
 
 
@app.route("/")
def hello():
    return " <html><head></head> <body> Enter </body></html>"
 
 
from flask import render_template
 
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField,IntegerField
 
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
 
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY
 
app.config['RECAPTCHA_USE_SSL'] = False
app.config["RECAPTCHA_PUBLIC_KEY"] = "6LdHWLkaAAAAAFJioRgnPe-YNl4xxUhNaLTkCZno"
app.config["RECAPTCHA_PRIVATE_KEY"] = "6LdHWLkaAAAAANYhxdrrw7ujYb-3g4aZGOZcWcN8"
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
 
from flask_bootstrap import Bootstrap
 
bootstrap = Bootstrap(app)
 
 
class NetForm(FlaskForm):
    cho = IntegerField('Введите угол поворота', validators=[DataRequired()])
 
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
 
    upload2 = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    cho2 = IntegerField('Введите угол поворота 2', validators=[DataRequired()])
    recaptcha = RecaptchaField()
 
    submit = SubmitField('send')
 
 
from werkzeug.utils import secure_filename
import os
 
import numpy as np
from PIL import Image
import seaborn as sns
 
 
def watermark(img, mask):
    x,y = mask.size
    mask.putalpha(200)
    mask = mask.convert("RGBA")
    img.paste(mask, (0,0), mask)
    img.save("./static/last.png")
    return 'ok'
 
def draw(filename, cho, fl2 , cho2):
    img = Image.open(filename)
    img = img.rotate(cho2)
    img2=Image.open(fl2)
    img2 = img2.rotate(cho)
    output_filename = filename
    img.save(filename)
    img2.save(fl2)
    img = img.convert("RGBA")
    watermark(img, img2)
    x, y = img.size
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot()
    data = np.random.randint(0, 255, (100, 100))
    ax.imshow(img, cmap='plasma')
    b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
    fig.colorbar(b, ax=ax)
    gr_path = "./static/newgr.png"
    sns.displot(data)
    plt.savefig(gr_path)
    plt.close()
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot()
    data = np.random.randint(0, 255, (100, 100))
    ax.imshow(img, cmap='plasma')
    b = ax.pcolormesh(data, edgecolors='black', cmap='plasma')
    fig.colorbar(b, ax=ax)
    gr_path2 = "./static/newgr2.png"
    sns.displot(data)
    plt.savefig(gr_path2)
    plt.close()
    return output_filename, gr_path, gr_path2
 
 
@app.route("/net", methods=['GET', 'POST'])
def net():
    global combine
    form = NetForm()
 
    filename = None
    filename2 = None
    newfilename = None
    grname = None
    grname2 = None
    combine = None
    rotate_path=None
    if form.validate_on_submit():
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        ch = form.cho.data
        ch2 = form.cho2.data
        filename2 = os.path.join('./static', secure_filename(form.upload2.data.filename))
        form.upload.data.save(filename)
        form.upload2.data.save(filename2)
        newfilename, grname, grname2 = draw(filename, int(ch), filename2, ch2)
    return render_template('net.html', form=form, fl2=filename2, image_name=newfilename, gr_name=grname, gr_name2=grname2)
 
 
if __name__ == "__main__":
    app.run(debug=True)
