from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from newsapi import NewsApiClient

app = Flask(__name__)

api_key = 'a7c40948db6d454aa8ee3f7d5754234b'

@app.route("/")
def about():
    return render_template('index.html')

@app.route("/news")
def news():
    # Create a NewsApiClient object
    newsapi = NewsApiClient(api_key=api_key)

    # Get top headlines
    top_headlines = newsapi.get_top_headlines(
                                          category='health',
                                          language='en',
                                          country='in')

    # Extract articles
    articles = top_headlines['articles']
    print(articles)
    length = len(articles)
    return render_template('news.html', articles=articles, len = length)


@app.route("/meddit")
def meddit():
    return render_template('meddit.html')

@app.route("/locator")
def locator():
    return render_template('locator.html')

@app.route("/skincancer")
def skincancer():
    return render_template('skincancer.html')

@app.route("/breastcancer")
def breastcancer():
    return render_template('breastcancer.html')

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/test")
def test():
    return render_template("onlinetest.html")

#handling lung cancer
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['USER_INFO_FILE'] = 'user_info.txt'

# Mapping each step to its corresponding recording duration
RECORDING_DURATIONS = {
    'Breathing Deep': 11,
    'Breathing Shallow': 8,
    'Cough Heavy': 5,
    'Cough Shallow': 5,
    'Vowel A': 8,
    'Vowel E': 8,
    'Vowel O': 8,
    'Counting Fast': 5,
    'Normal': 10
}

@app.route("/lungcancer")
def lungcancer():
    return render_template('lungcancer/lungcancer.html')
@app.route('/record', methods=['POST'])
def record():
    user_info = {
        'name': request.form['name'],
        'age': request.form['age'],
        'place': request.form['place'],
        'smoking': request.form['smoking'],
        'previous_disease': request.form['previous_disease'],
        'phone': request.form['phone'],
        'email': request.form['email']
    }

    # Save user info to a text file
    with open(app.config['USER_INFO_FILE'], 'w') as file:
        for key, value in user_info.items():
            file.write(f'{key}: {value}\n')

    return redirect(url_for('record_page'))

@app.route('/record_page')
def record_page():
    return render_template('lungcancer/record3.html', recording_durations=RECORDING_DURATIONS)


@app.route("/disease_info_page")
def disease_info_page():
    return render_template("lungcancer/lungcancer_info.html")

@app.route('/record_audio', methods=['POST'])
def record_audio():
    audio_step = request.form['audio_step']

    # Create the uploads folder if it doesn't exist
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Set the file path for the recorded audio
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{audio_step.replace(" ", "_")}.wav')

    # Record audio using sounddevice
    duration = RECORDING_DURATIONS.get(audio_step, 5)  # Default to 5 seconds if step not found
    samplerate = 48000
    recording = sounddevice.rec(int(samplerate * duration), samplerate=samplerate, channels=1, dtype='int16')
    sounddevice.wait()

    # Save the recorded audio data to a file
    soundfile.write(file_path, recording, samplerate)

    return 'OK'

if __name__ == "__main__":
    app.run(debug=True)