
        const recordButton = document.getElementById('record');
        const waveformImage = document.getElementById('waveform');
        const predictionText = document.getElementById('prediction');

        recordButton.addEventListener('click', async () => {
            try {
                // Clear previous results
                waveformImage.src = '';
                predictionText.textContent = '';

                // Initiate recording
                const recording = await navigator.mediaDevices.getUserMedia({ audio: true });
                const recorder = new MediaRecorder(recording);

                const chunks = [];
                recorder.ondataavailable = event => chunks.push(event.data);
                recorder.onstop = async () => {
                    const blob = new Blob(chunks, { type: 'audio/webm' });
                    const audioData = await blob.arrayBuffer();  // Read audio data into an array buffer

                    // Send audio data to Flask for prediction
                    $.ajax({
                        url: '/predict',
                        type: 'POST',
                        data: audioData,
                        processData: false,
                        contentType: false,
                        success: function(result) {
                            // Display prediction and waveform (if generated)
                            predictionText.textContent = result.prediction;
                            if (result.waveform) {
                                waveformImage.src = `data:image/png;base64,${result.waveform}`;
                            }
                        },
                        error: function(jqXHR, textStatus, errorThrown) {
                            predictionText.textContent = `Error: ${errorThrown}`;
                            if (errorThrown.includes("n_fft")) {
                            predictionText.textContent = "Audio too short. Please record a longer sound.";
                            } else {
                            predictionText.textContent = `Error: ${errorThrown}`;
                        }

                        }
                    });
                };

                recorder.start();
                setTimeout(() => recorder.stop(), 5000); // Record for 5 seconds
            } catch (error) {
                predictionText.textContent = `Error: ${error.message}`;
            }

        });
    </script> -->
    