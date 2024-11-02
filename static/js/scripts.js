function playSound(filename) {
    const audio = document.getElementById('audio-player');
    audio.src = `/audio/${filename}`;
    audio.play();
}
