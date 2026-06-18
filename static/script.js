document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userInput = document.getElementById('userInput');
    const sendBtn = document.getElementById('sendBtn');

    // Load stats on page load
    if (document.querySelector('.stats-panel')) {
        updateStats();
    }

    // Send message on button click
    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }

    // Send message on Enter key
    if (userInput) {
        userInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Reset stats
    const resetBtn = document.getElementById('resetStats');
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            fetch('/reset_stats', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            })
            .then(response => response.json())
            .then(data => {
                updateStats();
                // Show system message
                addMessage('system', '📊 Statistics have been reset!');
            });
        });
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage('user', message);
        userInput.value = '';
        userInput.focus();

        // Send to server
        fetch('/get_response', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            addMessage('bot', data.response);
            updateStats(data.stats);
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('bot', '⚠️ Sorry, there was an error. Please try again.');
        });
    }

    function addMessage(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content;

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        const now = new Date();
        timeDiv.textContent = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageDiv.appendChild(contentDiv);
        messageDiv.appendChild(timeDiv);
        chatMessages.appendChild(messageDiv);

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function updateStats(statsData) {
        fetch('/stats')
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalQuestions').textContent = data.total_questions || 0;
            document.getElementById('knownQueries').textContent = data.known_queries || 0;
            document.getElementById('unknownQueries').textContent = data.unknown_queries || 0;

            const unknownList = document.getElementById('unknownList');
            if (data.unknown_list && data.unknown_list.length > 0) {
                unknownList.innerHTML = data.unknown_list.map(q => 
                    `<li>❓ "${q}"</li>`
                ).join('');
            } else {
                unknownList.innerHTML = '<li style="color:#999; font-size:14px;">No unknown queries yet</li>';
            }
        });
    }
});