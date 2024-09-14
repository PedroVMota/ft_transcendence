export default class Alert {
    constructor() {
        this.BootstrapWarn = "alert alert-warning alert-dismissible fade show";
        this.BootstrapSuccess = "alert alert-success alert-dismissible fade show";
        this.BootstrapDanger = "alert alert-danger alert-dismissible fade show";
        this.BootstrapInfo = "alert alert-info alert-dismissible fade show";
    }

    static ShowAlert(message, type = "alert alert-info alert-dismissible fade show") {
        // Create the alert div
        let alert = document.createElement("div");
        alert.className = type;
        alert.innerHTML = `
            <span>${message}</span>
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        `;

        // Apply styles to the alert
        alert.style.position = "fixed";
        alert.style.bottom = "20px";
        alert.style.right = "20px";
        alert.style.zIndex = "1050";

        // Append alert to the body
        document.body.appendChild(alert);

        // Automatically remove the alert after 5 seconds
        setTimeout(() => {
            alert.classList.remove("show");
            alert.classList.add("hide");
            alert.addEventListener("transitionend", () => alert.remove());
        }, 5000);
    }
}