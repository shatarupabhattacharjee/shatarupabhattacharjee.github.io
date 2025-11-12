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

    // Generate image using our backend API
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
                throw new Error(data.error || 'Failed to generate image');
            }
            
            hideTypingIndicator();
            return data.imageUrl;
            
        } catch (error) {
            console.error('Error generating image:', error);
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
        
        // Generate image based on user's prompt
        const imageUrl = await generateImage(prompt);
        
        if (imageUrl) {
            // Create image element
            const img = document.createElement('img');
            img.src = imageUrl;
            img.alt = `Generated art: ${prompt}`;
            img.className = 'generated-image';
            
            // Create download button
            const downloadBtn = document.createElement('button');
            downloadBtn.className = 'btn';
            downloadBtn.style.marginTop = '10px';
            downloadBtn.innerHTML = '<i class="fas fa-download"></i> Download Image';
            downloadBtn.onclick = function() {
                const link = document.createElement('a');
                link.href = imageUrl;
                link.download = `art-reference-${Date.now()}.jpg`;
                link.click();
            };
            
            // Create container for image and button
            const container = document.createElement('div');
            container.appendChild(img);
            container.appendChild(document.createElement('br'));
            container.appendChild(downloadBtn);
            
            // Add bot message with generated image
            addMessage(container, false);
            
            // Add some helpful text
            const text = document.createElement('div');
            text.innerHTML = `Here's your generated reference image for: <strong>${prompt}</strong>. Feel free to download it or ask for another one!`;
            addMessage(text, false);
        } else {
            addMessage("I'm sorry, I couldn't generate an image for that. Could you try a different description?", false);
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
