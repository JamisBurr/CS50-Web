document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript is connected!");

    // Event listener for the header
    document.querySelector("header").addEventListener("click", () => {
        alert("Welcome to My Portfolio!");
    });

    // Event listeners for project titles
    document.querySelectorAll(".project-title").forEach(title => {
        title.addEventListener("click", (e) => {
            alert(`More about ${e.target.textContent}!`);
        });
    });
});