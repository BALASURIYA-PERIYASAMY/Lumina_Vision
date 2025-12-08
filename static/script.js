const video = document.getElementById('videoElement');
const canvas = document.getElementById('canvasElement');
const btnDetect = document.getElementById('btnDetect');
const btnRead = document.getElementById('btnRead');
const resultText = document.getElementById('resultText');
const autoSpeak = document.getElementById('autoSpeak');

// Initial Message
speak("Third Eye initialized. Camera starting.");

// Access Camera
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
        .then(function (stream) {
            video.srcObject = stream;
        })
        .catch(function (error) {
            console.error("Camera error:", error);
            resultText.innerText = "Error: Cannot access camera.";
            speak("Error. Cannot access camera.");
        });
}

function captureFrame() {
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);
    return canvas.toDataURL('image/jpeg');
}

async function analyzeScene(mode) {
    // UI Feedback
    resultText.innerText = "Analyzing...";
    speak("Analyzing...");

    // Disable buttons
    btnDetect.disabled = true;
    btnRead.disabled = true;

    try {
        const imageData = captureFrame();

        const response = await fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ image: imageData, mode: mode })
        });

        const data = await response.json();

        if (data.error) {
            resultText.innerText = "Error: " + data.error;
            speak("Error occurred.");
        } else {
            const text = data.result;
            resultText.innerText = text;
            speak(text);
        }

    } catch (e) {
        console.error(e);
        resultText.innerText = "Network Error";
        speak("Network error.");
    } finally {
        btnDetect.disabled = false;
        btnRead.disabled = false;
    }
}

function speak(text) {
    if (!autoSpeak.checked) return;

    if ('speechSynthesis' in window) {
        // Cancel current speech
        window.speechSynthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        // utterance.lang = 'en-US'; // Default
        window.speechSynthesis.speak(utterance);
    }
}

// Event Listeners
btnDetect.addEventListener('click', () => analyzeScene('detect'));
btnRead.addEventListener('click', () => analyzeScene('read'));

// Modal Logic Removed
