from flask import Flask, render_template, request
import model
import nyt

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/name/<name>')
def hello_name(name):
    return render_template('name.html', var = name)


@app.route('/rhyme/<word>')
def find_rhymes(word):
    return render_template('list.html', 
        title="Rhymes with " + word, my_list=model.get_rhymes())
		

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        #print(firstname)
    else:
        firstname = ''
        lastname = ''
    return render_template("hello.html",firstname=firstname, lastname=lastname)
	
@app.route('/sum', methods=['GET', 'POST'])
def sum():
    if request.method == 'POST':
        level = request.form.get('comp_select')
        content = request.form['message']
        summarization_info, summary = model.get_summarization_by_textrank(text = content, left_num = level)
        API_flage = True
    else:
        content = nyt.get_article()
        summarization_info, summary = model.get_summarization_by_textrank(text = content, left_num = 1)
        API_flage = False
        #print(summarization)
    return render_template("summarization.html",content = summarization_info, summary = summary, API_flage = API_flage)
		
if __name__ == "__main__":
    model.rhymes()
    app.run(debug=True)