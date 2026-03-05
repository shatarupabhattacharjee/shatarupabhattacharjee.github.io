document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const typingIndicator = document.getElementById('typing-indicator');

    // Add message to chat
    function addMessage(content, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        
        if (typeof content === 'string') {
            messageContent.innerHTML = content;
        } else if (content.nodeType === Node.ELEMENT_NODE) {
            messageContent.appendChild(content);
        }
        
        messageDiv.appendChild(messageContent);
        chatMessages.insertBefore(messageDiv, typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Show typing indicator
    function showTypingIndicator() {
        typingIndicator.style.display = 'block';
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Hide typing indicator
    function hideTypingIndicator() {
        typingIndicator.style.display = 'none';
    }

    // Generate art reference using Ollama backend
    async function generateImage(prompt) {
        showTypingIndicator();
        
        try {
            const response = await fetch('http://localhost:3000/api/generate-image', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    prompt: prompt
                })
            });
            
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'Failed to generate art reference');
            }
            
            hideTypingIndicator();
            
            // Add cache-busting parameter for non-placeholder images
            const imageUrl = data.isPlaceholder ? 
                data.imageUrl : 
                `${data.imageUrl}${data.imageUrl.includes('?') ? '&' : '?'}t=${Date.now()}`;
            
            return {
                imageUrl: imageUrl,
                textResponse: data.textResponse,
                prompt: data.prompt,
                timestamp: data.timestamp,
                isPlaceholder: data.isPlaceholder || false
            };
            
        } catch (error) {
            console.error('Error generating art reference:', error);
            hideTypingIndicator();
            addMessage(`I'm sorry, I encountered an error: ${error.message}`, false);
            return null;
        }
    }

    // Handle user input
    async function handleUserInput() {
        const prompt = userInput.value.trim();
        if (!prompt) return;
        
        // Add user message to chat
        addMessage(prompt, true);
        userInput.value = '';
        userInput.disabled = true;
        
        try {
            // Show loading message
            const loadingMessage = document.createElement('div');
            loadingMessage.className = 'message bot';
            loadingMessage.innerHTML = `
                <div class="message-content">
                    <p>Generating your art reference... This may take a moment.</p>
                    <div class="typing-indicator">
                        <span class="typing-dot"></span>
            
            // Generate art reference based on user's prompt
            const result = await generateImage(prompt);
            
            // Remove typing indicator
            const messages = document.querySelectorAll('.message:not(.user)');
            if (messages.length > 0) {
                messages[messages.length - 1].remove();
            }
            
            if (result) {
                // Create and append the art card
                const artCard = createArtCard(result);
                addMessage(artCard, false);
            } else {
                addMessage("I'm sorry, I couldn't generate a reference for that. Could you try a different description?", false);
            }
        } catch (error) {
            console.error('Error handling user input:', error);
            addMessage(`I'm sorry, something went wrong: ${error.message}`, false);
        } finally {
            userInput.disabled = false;
            userInput.focus();
        }
    }

    // Event listeners
    sendButton.addEventListener('click', handleUserInput);
    
    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            handleUserInput();
        }
    });
    
    // Mobile menu toggle (copied from main script.js)
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');
    
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }
});
