import { Color } from  '../Utils/Color'

/*
    * Shows an alert message on the top right of the screen
    * @param {string} message - The message to display in the alert
    * @param {number} duration - The duration in milliseconds to display the alert
    * 
*/
export function showAlert(message, duration = 1000) {
    // Create the alert div
    if (document.getElementById('alertDiv')) {
        document.getElementById('alertDiv').remove();
    }
    const alertDiv = document.createElement('div');
    alertDiv.id = 'alertDiv';
    alertDiv.style.position = 'absolute';
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.padding = '10px';
    alertDiv.style.color = 'white';
    alertDiv.style.backdropFilter = 'blur(10px)';
    alertDiv.style.backgroundColor = Color.RGBToRGBA(150, 150, 150, 0.1);
    alertDiv.style.boxShadow = '0 0 30px rgba(0, 0, 0, 0.1)';
    alertDiv.style.border = '1px solid rgba(0, 0, 0, 0.1)';
    alertDiv.style.borderRadius = '5px';
    alertDiv.style.zIndex = '1000'; // Ensure it's on top of other elements
    alertDiv.innerText = message;

    // Append the alert div to the body
    document.body.appendChild(alertDiv);

    // Remove the alert div after 'duration' milliseconds
    setTimeout(() => {
        alertDiv.remove();
    }, duration);
}