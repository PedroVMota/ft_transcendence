import { color } from 'three/examples/jsm/nodes/Nodes.js';
import { Color } from  '../Utils/Color'

/*
    * Shows an alert message on the top right of the screen
    * @param {string} message - The message to display in the alert
    * @param {number} duration - The duration in milliseconds to display the alert
    * 
*/
export function showAlert(message, duration = 1000, backgroundColor = Color.RGBToRGBA(200, 75, 75, .5), color = Color.RGBToRGBA(200,200,200,1), borderColor = Color.RGBToRGBA(200, 100, 100, .5)) {
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
    alertDiv.style.color = `${color}`;
    alertDiv.style.backdropFilter = 'blur(10px)';
    alertDiv.style.backgroundColor = `${backgroundColor}`;
    alertDiv.style.boxShadow = '0 0 30px rgba(0, 0, 0, 0.1)';
    alertDiv.style.border = `1px solid ${borderColor}`
    alertDiv.style.borderRadius = '5px';
    alertDiv.style.zIndex = '1000'; // Ensure it's on top of other elements
    alertDiv.innerText = message;
    // Append the alert div to the body
    alertDiv.classList.add('fade-in');

    document.body.appendChild(alertDiv);
    // Remove the alert div after 'duration' milliseconds
    setTimeout(() => {
        alertDiv.classList.add('fade-out');
        setTimeout(() => {
            alertDiv.classList.add('hidden');
            alertDiv.classList.remove('fade-out');
        }, 500);

    }, duration);
}