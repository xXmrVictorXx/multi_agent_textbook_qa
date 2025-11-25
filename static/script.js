document.addEventListener('DOMContentLoaded', () => {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    // Auto-resize textarea
    userInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        if (this.value === '') {
            this.style.height = 'auto';
        }
    });

    // Send message on Enter (without Shift)
    userInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendBtn.addEventListener('click', sendMessage);

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Disable input
        userInput.value = '';
        userInput.style.height = 'auto';
        userInput.disabled = true;
        sendBtn.disabled = true;

        // Add user message
        appendMessage(message, 'user-message');

        // Add loading indicator
        const loadingId = 'loading-' + Date.now();
        appendLoading(loadingId);

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Remove loading
            removeLoading(loadingId);

            // Add Answerer response
            if (data.answer) {
                appendMessage(data.answer, 'answerer-message');
            }

            // Add Checker response
            if (data.check) {
                // Add a small delay for effect
                setTimeout(() => {
                    appendMessage(data.check, 'checker-message');
                }, 500);
            }

        } catch (error) {
            console.error('Error:', error);
            removeLoading(loadingId);
            appendMessage('系统故障: 无法连接到核心引擎。请稍后再试。', 'system-message');
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    function appendMessage(content, className) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${className}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = content; // Use textContent for safety, or innerHTML if markdown parsing is needed later
        
        messageDiv.appendChild(contentDiv);
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }

    function appendLoading(id) {
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message system-message';
        loadingDiv.id = id;
        loadingDiv.innerHTML = `
            <div class="loading-gears">
                <div class="gear one"></div>
                <div class="gear two"></div>
            </div>
            <div style="margin-top: 5px; font-size: 0.8rem;">正在处理...</div>
        `;
        chatContainer.appendChild(loadingDiv);
        scrollToBottom();
    }

    function removeLoading(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
});
