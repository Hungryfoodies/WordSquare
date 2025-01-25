from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/play', methods=['POST'])
def play():
    user_input = request.form.get('user_input')
    # Your game logic here using the TXT file
    result = f"You entered: {user_input}"  # Replace with actual game logic
    return {'result': result}

if __name__ == '__main__':
    app.run(debug=True)
