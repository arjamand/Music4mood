function getSystemTheme() {
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        return 'dark';
    } else {
        return 'light';
    }
}

// Function to set the initial theme based on system preference
function setInitialTheme() {
    const systemTheme = getSystemTheme();
    const body = document.body;
    const toggleIcon = document.querySelector('.theme-toggle');

    if (systemTheme === 'dark') {
        body.classList.add('dark-mode');
        toggleIcon.textContent = '🌙';
    } else {
        toggleIcon.textContent = '☀️';
    }
}
   // Call setInitialTheme on page load
setInitialTheme();

 // Function to toggle the theme
function toggleTheme() {
    const body = document.body;
    body.classList.toggle('dark-mode');
    const toggleIcon = document.querySelector('.theme-toggle');
    toggleIcon.textContent = body.classList.contains('dark-mode') ? '🌙' : '☀️';
}

document.getElementById("moodForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const languageSelect = document.getElementById("languageSelect");
    const selectedLanguage = languageSelect.value;

    const moodText = document.getElementById("moodText").value;
    const loading = document.querySelector(".loading");
    const moodResult = document.getElementById("moodResult");
    const recommendedSongs = document.querySelector(".recommended-songs");
    const songList = document.querySelector(".song-list");
    const submitButton = this.querySelector("button");

    // Show loading animation, disable button
    loading.style.display = "flex";
    submitButton.disabled = true;
    submitButton.style.opacity = "0.7";

    try {
        // Make a request to the server with the user's mood text
        const response = await fetch("/get-mood", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ mood: moodText , language:selectedLanguage })
        });

        // Receive mood category and songs data from server
        const { moodCategory, songs } = await response.json();

        // Display detected mood
        moodResult.style.display = "block";
        moodResult.textContent = `Mood / Feeling Detected: ${moodCategory}`;

        // Clear previous song list
        songList.innerHTML = "";

        // Display recommended songs
        songs.forEach(song => {
            const li = document.createElement("li");
            li.className = "song-item";
            li.innerHTML = `
                <span class="song-title">${song.title}</span>
                <button class="play-button" onclick="window.open('${song.link}', '_blank')">Play</button>
            `;
            songList.appendChild(li);
        });


        recommendedSongs.style.display = "block";
    } catch (error) {
        console.error("Error:", error);
        alert("Sorry, there was an error processing your request. Please try again.");
    } finally {
        // Hide loading animation, enable button
        loading.style.display = "none";
        submitButton.disabled = false;
        submitButton.style.opacity = "1";
    }
});

// Function to handle playing songs
function playSong(link) {
    // Create an audio element if it doesn't exist
    let audioPlayer = document.querySelector('audio');
    if (!audioPlayer) {
        audioPlayer = document.createElement('audio');
        audioPlayer.controls = true;
        audioPlayer.style.display = 'none';
        document.body.appendChild(audioPlayer);
    }

    // Set the source and play
    audioPlayer.src = link;
    audioPlayer.play();
}