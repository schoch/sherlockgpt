document.addEventListener('DOMContentLoaded', async function () {
    const chatWindow = document.getElementById('chatWindow');

    try {
        const response = await fetch('/get_chat_history');
        if (!response.ok) throw new Error('Netzwerkantwort war nicht ok');

        const data = await response.json();
        chatWindow.innerHTML = data.chat.map(message => 
            `<div class="chat-message ${message.sender === 'user' ? 'user-message' : 'character-message'}">${message.text}</div>`
        ).join('');

        chatWindow.scrollTop = chatWindow.scrollHeight;
    } catch (error) {
        console.error('Fehler beim Abrufen des Chatverlaufs:', error);
        chatWindow.innerHTML += '<div class="chat-message error-message">Fehler beim Abrufen des Chatverlaufs. Bitte versuchen Sie es später erneut.</div>';
    }
});

document.getElementById('chatForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    const userInput = document.getElementById('userInput').value;
    const chatWindow = document.getElementById('chatWindow');

    chatWindow.innerHTML += `<div class="chat-message user-message">${userInput}</div>`;
    document.getElementById('userInput').value = '';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput })
        });

        if (!response.ok) throw new Error('Netzwerkantwort war nicht ok');

        const data = await response.json();
        chatWindow.innerHTML += `<div class="chat-message character-message">${data.answer}</div>`;
    } catch (error) {
        console.error('Fehler beim Abrufen der Antwort:', error);
        chatWindow.innerHTML += '<div class="chat-message error-message">Fehler beim Abrufen der Antwort. Bitte versuchen Sie es später erneut.</div>';
    }

    chatWindow.scrollTop = chatWindow.scrollHeight;
});

document.getElementById('backButton').addEventListener('click', () => {
    window.location.href = '/'; // URL zur Übersicht
});

document.getElementById('scenarioForm').addEventListener('submit', async function (event) {
    event.preventDefault();
    const keywords = document.getElementById('keywords').value;
    const button = document.getElementById('generateButton');
    
    button.disabled = true;

    try {
        const response = await fetch('/new_scenario', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keywords })
        });

        if (!response.ok) throw new Error('Netzwerkantwort war nicht ok');

        const data = await response.json();
        displayScenario(data.scenario);
    } catch (error) {
        console.error('Es gab ein Problem mit der Fetch-Operation:', error);
        document.getElementById('result').innerHTML = '<p>Fehler beim Generieren des Szenarios. Bitte versuchen Sie es später erneut.</p>';
    } finally {
        button.disabled = false;
    }
});

function displayScenario(scenario) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = formatDataIteratively(scenario);
    addInterrogateButton();
}

function formatDataIteratively(data) {
    let html = '';
    const stack = [{ data, level: 0, key: null }];
    
    while (stack.length) {
        const { data, level, key } = stack.pop();
        
        if (key !== null) {
            html += `<div style="margin-left: ${level * 20}px;"><strong>${formatKey(key)}:</strong> `;
        }

        if (Array.isArray(data)) {
            html += '<ul>';
            data.forEach((item, index) => stack.push({ data: item, level: level + 1, key: index }));
            html += '</ul>';
        } else if (typeof data === 'object' && data !== null) {
            html += '<div>';
            Object.keys(data).forEach(key => stack.push({ data: data[key], level: level + 1, key }));
            html += '</div>';
        } else {
            html += data;
        }

        if (key !== null) {
            html += '</div>';
        }
    }

    return html;
}

function formatKey(key) {
    return typeof key === 'string' ? key.replace(/_/g, ' ').replace(/\b\w/g, char => char.toUpperCase()) : key;
}

function addInterrogateButton() {
    const container = document.getElementById('additionalButtonContainer');
    container.innerHTML = '';

    const interrogateButton = document.createElement('button');
    interrogateButton.textContent = 'Zur Vernehmung';
    interrogateButton.id = 'interrogateButton';
    interrogateButton.addEventListener('click', () => {
        window.location.href = '/interrogate';
    });

    container.appendChild(interrogateButton);
}