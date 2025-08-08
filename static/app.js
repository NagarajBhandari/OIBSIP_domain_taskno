// app.js - browser-side: uses Web Speech API for recognition and Web Speech Synthesis for playback
const startBtn = document.getElementById('startBtn');
const stopBtn = document.getElementById('stopBtn');
const status = document.getElementById('status');
const transcriptEl = document.getElementById('transcript');
const responseEl = document.getElementById('response');

let recognition;
if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
  status.innerText = "SpeechRecognition API not supported in this browser.";
  startBtn.disabled = true;
} else {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  recognition.onstart = () => {
    status.innerText = "Listening...";
    startBtn.disabled = true;
    stopBtn.disabled = false;
  };

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript;
    transcriptEl.innerText = text;
    status.innerText = "Processing...";
    // send to server
    fetch('/query', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({text})
    })
    .then(r => r.json())
    .then(data => {
      if (data && data.response) {
        responseEl.innerText = data.response;
        speak(data.response);
      } else {
        responseEl.innerText = "No response from server.";
      }
    }).catch(err => {
      responseEl.innerText = "Error: " + err;
    }).finally(() => {
      status.innerText = "Ready.";
      startBtn.disabled = false;
      stopBtn.disabled = true;
    });
  };

  recognition.onerror = (e) => {
    status.innerText = "Recognition error: " + e.error;
    startBtn.disabled = false;
    stopBtn.disabled = true;
  };

  recognition.onend = () => {
    status.innerText = "Stopped.";
    startBtn.disabled = false;
    stopBtn.disabled = true;
  };
}

startBtn.onclick = () => {
  if (recognition) recognition.start();
};

stopBtn.onclick = () => {
  if (recognition) recognition.stop();
};

function speak(text) {
  if (!('speechSynthesis' in window)) return;
  const utter = new SpeechSynthesisUtterance(text);
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utter);
}
