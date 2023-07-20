import uvicorn
from fastapi.responses import HTMLResponse

from app.core import get_application

app = get_application()


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)


# Possible improvements: move the HTML code to a separate file, use a template engine (e.g., Jinja2), etc.
@app.get("/office", response_class=HTMLResponse)
async def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Office Microwave</title>
    </head>
    <body>
        <h1>Office Microwave</h1>
        <div id="microwave-state">
            <p id="microwave-status"></p>
            <p id="microwave-power"></p>
            <p id="microwave-counter"></p>
        </div>
        <button onclick="increasePower()">Increase Power</button>
        <button onclick="decreasePower()">Decrease Power</button>
        <button onclick="increaseCounter()">Increase Counter</button>
        <button onclick="decreaseCounter()">Decrease Counter</button>
        <br>
        <label for="token-input">Authorization Token:</label>
        <input type="text" id="token-input">
        <button onclick="cancelMicrowave()">Cancel</button>
        <br>
        <button onclick="copyTokenToClipboard()">Copy Test Token</button>
        <input type="text" id="token-input" style="display: none;">
        <p id="test-token" style="display: none;">eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.4-0VSqwjSPaQE_5LPW9iyvM1O79LU4Mru70xWNjNCqA</p>

        <script>
            // Function to fetch the microwave state and update the display
            async function fetchMicrowaveState() {
                try {
                    const response = await fetch('http://localhost:8000/api/microwave');
                    const data = await response.json();

                    // Calculate the number of seconds left for the counter display
                    var isoDateString = new Date().toISOString();
                    isoDateString = isoDateString.substring(0, isoDateString.length - 1);
                    const currentTime = new Date(isoDateString);
                    const timerEndAt = new Date(data.timer_end_at);
                    const secondsLeft = Math.max(0, Math.floor((timerEndAt.getTime() - currentTime.getTime()) / 1000));

                    // Display the microwave status
                    document.getElementById('microwave-counter').innerText = `Counter: ${secondsLeft}s`;
                    document.getElementById('microwave-power').innerText = `Power: ${data.power}W`;
                    const microwaveStatus = document.getElementById('microwave-status');
                    microwaveStatus.innerText = `Microwave is ${secondsLeft > 0 ? 'on' : 'off'}`;
                } catch (error) {
                    console.error('Error fetching microwave state:', error);
                }
            }

            async function increasePower() {
                const response = await sendMicrowaveRequest('http://localhost:8000/api/microwave/power/add');
                if (response.status === 200) {
                    await fetchMicrowaveState();
                } else {
                    await handleResponseErrors(response);
                }
            }

            async function decreasePower() {
                const response = await sendMicrowaveRequest('http://localhost:8000/api/microwave/power/sub');
                if (response.status === 200) {
                    await fetchMicrowaveState();
                } else {
                    await handleResponseErrors(response);
                }
            }

            async function increaseCounter() {
                const response = await sendMicrowaveRequest('http://localhost:8000/api/microwave/timer/add');
                if (response.status === 200) {
                    await fetchMicrowaveState();
                } else {
                    await handleResponseErrors(response);
                }
            }

            async function decreaseCounter() {
                const response = await sendMicrowaveRequest('http://localhost:8000/api/microwave/timer/sub');
                if (response.status === 200) {
                    await fetchMicrowaveState();
                } else {
                    await handleResponseErrors(response);
                }
            }

            async function cancelMicrowave() {
                const token = document.getElementById('token-input').value;
                const response = await sendMicrowaveRequest('http://localhost:8000/api/microwave/cancel', 'POST', token);
                if (response.status === 200) {
                    await fetchMicrowaveState();
                } else {
                    await handleResponseErrors(response);
                }
            }

            // Function to handle response errors (e.g., 400 Bad Request, 401 Unauthorized, 403 Forbidden)
            async function handleResponseErrors(response) {
                const data = await response.json();
                if (response.status === 400) {
                    alert("Couldn't perform this action");
                } else if (response.status === 401 || response.status === 403) {
                    alert("You don't have permission to perform this action");
                } else {
                    alert("Something went wrong");
                }
            }

            // Function to send microwave requests with optional authorization token
            async function sendMicrowaveRequest(url, method = 'POST', token = null) {
                try {
                    const headers = {};
                    if (token) {
                        headers['Authorization'] = `Bearer ${token}`;
                    }

                    const response = await fetch(url, {
                        method: method,
                        headers: headers,
                    });

                    return response;
                } catch (error) {
                    console.error('Error sending microwave request:', error);
                    return error;
                }
            }

            async function copyTokenToClipboard() {
                // Get the token element
                const tokenElement = document.getElementById('test-token');

                // Create a temporary input element to hold the token value
                const tempInput = document.createElement('input');
                tempInput.value = tokenElement.textContent;

                // Append the temporary input element to the DOM
                document.body.appendChild(tempInput);

                // Select the content of the input element
                tempInput.select();

                // Copy the selected content to the clipboard
                document.execCommand('copy');

                // Remove the temporary input element from the DOM
                document.body.removeChild(tempInput);

                // Show a message to indicate that the token has been copied
                alert('Test token copied to clipboard!');
            }

            // Function to refresh microwave state
            async function cyclicRefresh() {
                fetchMicrowaveState();
            }

            // Set up cyclic refresh
            setInterval(cyclicRefresh, 333); // 333ms, 0.3s

            // Fetch the initial microwave state when the page loads
            fetchMicrowaveState();
        </script>
    </body>
    </html>
    """
