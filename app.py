from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/deploy', methods=['POST'])
def deploy():
    project_name = request.form.get('project_name')
    result = deploy_to_azure(project_name)
    return f"<h2>Deployment Output:</h2><pre>{result}</pre>"

if __name__ == '__main__':
    app.run(debug=True)
