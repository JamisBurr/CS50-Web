document.addEventListener("DOMContentLoaded", () => {
    const grid = document.getElementById("grid");
    const feedback = document.getElementById("feedback");
    const currentSumElement = document.getElementById("current-sum");
    const submitButton = document.getElementById("submit");

    // Function to retrieve CSRF token
    function getCSRFToken() {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]');
        if (csrfToken) {
            return csrfToken.value;
        } else {
            console.error("CSRF token not found in the document.");
            return null;
        }
    }

    const numbers = Array.from({ length: 25 }, () => Math.floor(Math.random() * 999) + 1);
    const selectedNumbers = new Set();

    numbers.forEach(num => {
        const cell = document.createElement("div");
        cell.textContent = num;
        cell.className = "bg-gray-700 text-white p-4 rounded text-center cursor-pointer";
        cell.dataset.value = num;

        cell.addEventListener("click", () => {
            const value = parseInt(cell.dataset.value);
            if (selectedNumbers.has(value)) {
                selectedNumbers.delete(value);
                cell.classList.remove("bg-green-500");
                cell.classList.add("bg-gray-700");
            } else {
                selectedNumbers.add(value);
                cell.classList.add("bg-green-500");
                cell.classList.remove("bg-gray-700");
            }
            updateSum();
        });

        grid.appendChild(cell);
    });

    function updateSum() {
        const currentSum = Array.from(selectedNumbers)
            .map(num => num.toString().split("").reduce((sum, digit) => sum + parseInt(digit), 0))
            .reduce((sum, digitSum) => sum + digitSum, 0);

        currentSumElement.textContent = currentSum;
    }

    submitButton.addEventListener("click", () => {
        const currentSum = parseInt(currentSumElement.textContent);
    
        feedback.classList.remove("hidden");
        if (currentSum === 37) {
            feedback.textContent = "Correct! Proceeding to the next level...";
            feedback.className = "text-green-500 mt-2";
    
            // Notify the backend about progress
            fetch("/advance-level/", { method: "POST", headers: { "X-CSRFToken": getCSRFToken() } })
            .then(() => window.location.href = "/level-two/")
            .catch(err => console.error("Error advancing level:", err));
        } else {
            feedback.textContent = "Incorrect. Try again!";
            feedback.className = "text-red-500 mt-2";
        }
    });    
});
