from flask import Flask, render_template, Response
import sounddevice as sd
import numpy as np
import librosa
from keras.models import load_model
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

predicted_class = 'Not predicted'

# Load pre-built model
model = load_model('/Users/rohitphotography/Downloads/Audio-Classification/saved_models/audio_classification.hdf5')

# Load the label encoder used during training
label_encoder = LabelEncoder()
label_encoder.classes_ = np.load('/Users/rohitphotography/Downloads/Projects/label_encoder.npy')

# Define the audio parameters
sample_rate = 22050
duration = 2  # You can adjust this based on your model's input size
input_shape = (60,)

# Callback function for live audio processing
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Error: {status}")
    else:
        # Convert audio data to MFCC features
        mfccs_features = librosa.feature.mfcc(y=indata[:, 0], sr=sample_rate, n_mfcc=60)
        mfccs_scaled_features = np.mean(mfccs_features.T, axis=0)
        
        # Reshape for model input
        mfccs_scaled_features = mfccs_scaled_features.reshape(1, -1)

        # Make prediction using the pre-built model
        predicted_probabilities = model.predict(mfccs_scaled_features)
        predicted_label = np.argmax(predicted_probabilities, axis=1)
        prediction_class = label_encoder.inverse_transform(predicted_label)

        ppredicted_class = f"Predicted Class: {prediction_class}"
        return predicted_class

@app.route('/')
def index():
    return render_template('index.html', predicted_class=predicted_class)

def generate_audio():
    with sd.InputStream(callback=audio_callback, channels=1, samplerate=sample_rate):
        print("Live audio monitoring... Press Ctrl+C to stop.")
        sd.sleep(duration * 1000)  # Run for a specified duration (in milliseconds)

        while True:
            # yield a dummy response to keep the connection open
            yield b'\0'

@app.route('/audio_feed')
def audio_feed():
    return Response(generate_audio(), content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)