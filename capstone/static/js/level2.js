document.addEventListener("DOMContentLoaded", () => {
    const inputField = document.getElementById("cipher-input");
    const feedback = document.getElementById("feedback");
    const submitButton = document.getElementById("submit-answer");

    // Define the correct modulo-37 sequence
    const correctSequence = [1, 2, 10]; // Example sequence for the modulo challenge
    let currentIndex = 0; // Tracks the player's progress

    // Function to get CSRF token
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            return csrfToken.value;
        } else {
            console.error("CSRF token not found.");
            return null;
        }
    }

    // Example fetch request
    submitButton.addEventListener("click", () => {
        const userInput = parseInt(inputField.value);

        fetch("/level-two-validate/", {
            method: "POST",
            headers: {
                "X-CSRFToken": getCSRFToken(),
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ input: userInput }),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    feedback.textContent = "Correct! Proceeding to the next level...";
                    feedback.className = "text-green-500 mt-4";
                    window.location.href = "/level-three/";
                } else {
                    feedback.textContent = "Incorrect. Try again!";
                    feedback.className = "text-red-500 mt-4";
                }
            })
            .catch(err => {
                console.error("Error:", err);
                feedback.textContent = "Error communicating with the server.";
                feedback.className = "text-red-500 mt-4";
            });
        });
    });