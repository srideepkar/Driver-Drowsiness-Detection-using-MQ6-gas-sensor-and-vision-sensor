from flask import Flask, render_template, request
import main2
app = Flask(__name__)
@app.route('/')
def hello():
	return render_template('temp.html')

@app.route('/send',methods=['POST'])
def send():
	if request.method == 'POST':
		result,img = main2.ddd()
		return render_template('temp.html', result=result)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
