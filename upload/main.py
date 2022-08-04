from flask import Flask, render_template
from forms import UploadFileForm
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = "supersercetkey"
app.config['UPLOAD_FOLDER'] = 'static/'



@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
       
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename)))
        

        return "file has been upload"

    return render_template('index.html', form=form)


if __name__ == '__main__':
 app.run(debug=True)
