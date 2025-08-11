let currentSessionId = null;
let currentQuestion = null;

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    // File upload handler
    document.getElementById('fileInput').addEventListener('change', handleFileUpload);
    
    // Context file upload handler
    document.getElementById('contextFileInput').addEventListener('change', handleContextFileUpload);
    
    // Upload method switcher
    document.querySelectorAll('.upload-method').forEach(method => {
        method.addEventListener('click', function() {
            document.querySelectorAll('.upload-method').forEach(m => m.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Context method switcher
    document.querySelectorAll('.context-method').forEach(method => {
        method.addEventListener('click', function() {
            document.querySelectorAll('.context-method').forEach(m => m.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    // Enter key handler for question input
    document.getElementById('questionInput').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            askQuestion();
        }
    });
    
    // Modal click outside to close
    document.getElementById('addContextModal').addEventListener('click', function(e) {
        if (e.target === this) {
            hideAddContextModal();
        }
    });
});

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    showProcessing();
    
    const formData = new FormData();
    formData.append('file', file);
    
    fetch('/api/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideProcessing();
        if (data.success) {
            currentSessionId = data.session_id;
            showContentInfo(data.summary);
        } else {
            showError(data.error || 'Failed to upload file');
        }
    })
    .catch(error => {
        hideProcessing();
        showError('Upload failed: ' + error.message);
    });
}

function processUrl() {
    const url = document.getElementById('urlInput').value.trim();
    if (!url) {
        showError('Please enter a valid URL');
        return;
    }
    
    showProcessing();
    
    fetch('/api/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        hideProcessing();
        if (data.success) {
            currentSessionId = data.session_id;
            showContentInfo(data.summary);
        } else {
            showError(data.error || 'Failed to process URL');
        }
    })
    .catch(error => {
        hideProcessing();
        showError('URL processing failed: ' + error.message);
    });
}

function processText() {
    const text = document.getElementById('textInput').value.trim();
    if (!text) {
        showError('Please enter some text');
        return;
    }
    
    showProcessing();
    
    fetch('/api/upload', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        hideProcessing();
        if (data.success) {
            currentSessionId = data.session_id;
            showContentInfo(data.summary);
        } else {
            showError(data.error || 'Failed to process text');
        }
    })
    .catch(error => {
        hideProcessing();
        showError('Text processing failed: ' + error.message);
    });
}

function askQuestion() {
    const question = document.getElementById('questionInput').value.trim();
    if (!question || !currentSessionId) return;
    
    currentQuestion = question;
    
    // Add user message to chat
    addMessage(question, 'user');
    
    // Clear input and disable button
    document.getElementById('questionInput').value = '';
    const askButton = document.getElementById('askButton');
    askButton.disabled = true;
    askButton.textContent = 'Thinking...';
    
    fetch('/api/query', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            session_id: currentSessionId,
            question: question
        })
    })
    .then(response => response.json())
    .then(data => {
        askButton.disabled = false;
        askButton.textContent = 'Ask';
        
        if (data.success) {
            addMessage(data.answer, 'assistant', data.source);
            
            if (data.not_found && data.can_search_web) {
                showWebSearchPrompt();
            }
        } else {
            showError(data.error || 'Failed to get answer');
        }
    })
    .catch(error => {
        askButton.disabled = false;
        askButton.textContent = 'Ask';
        showError('Query failed: ' + error.message);
    });
}

function searchWeb() {
    if (!currentQuestion) return;
    
    hideWebSearchPrompt();
    
    // Show searching message
    const searchMessage = addMessage('🔍 Searching the web...', 'assistant', 'web-search');
    
    fetch('/api/search-web', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            question: currentQuestion
        })
    })
    .then(response => response.json())
    .then(data => {
        // Remove searching message
        searchMessage.remove();
        
        if (data.success) {
            let messageClass = 'assistant';
            if (data.source === 'google_search') {
                messageClass = 'web-search';
            } else if (data.source === 'gemini_fallback') {
                messageClass = 'gemini-fallback';
            }
            
            addMessage(data.answer, messageClass, data.source, data.message);
        } else {
            showError(data.error || 'Web search failed');
        }
    })
    .catch(error => {
        searchMessage.remove();
        showError('Web search failed: ' + error.message);
    });
}

function showProcessing() {
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('processing').style.display = 'block';
    document.getElementById('contentInfo').style.display = 'none';
}

function showContextProcessing() {
    document.getElementById('processing').style.display = 'block';
    // Don't hide contentInfo when adding context
}

function hideProcessing() {
    document.getElementById('processing').style.display = 'none';
}

function showContentInfo(summary) {
    document.getElementById('uploadSection').style.display = 'none';
    document.getElementById('summaryContent').textContent = summary;
    document.getElementById('contentInfo').style.display = 'block';
    
    // Clear previous chat messages
    document.getElementById('chatMessages').innerHTML = '';
    
    // Focus on question input
    document.getElementById('questionInput').focus();
}

function formatMarkdown(text) {
    // Simple markdown formatting for common elements
    let formatted = text
        // First handle ** bold ** 
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        // Then handle bullet points (make sure they don't conflict with bold)
        .replace(/^\* (.*$)/gim, '<li>$1</li>')
        // Wrap consecutive list items in <ul>
        .replace(/(<li>.*<\/li>\s*)+/gs, '<ul>$&</ul>')
        // Convert line breaks to proper breaks
        .replace(/\\\n/g, '<br>')
        .replace(/\n/g, '<br>');
    
    return formatted;
}

function addMessage(text, type, source = null, additionalMessage = null) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    
    // Format text based on source
    let formattedText = text;
    if (source === 'google_search' || source === 'gemini_fallback') {
        formattedText = formatMarkdown(text);
    }
    
    messageDiv.innerHTML = `
        <div class="message-content">${formattedText}</div>
        ${source ? `<div class="message-source">Source: ${getSourceLabel(source)}</div>` : ''}
        ${additionalMessage ? `<div class="message-source">${additionalMessage}</div>` : ''}
    `;
    
    messagesContainer.appendChild(messageDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return messageDiv;
}

function getSourceLabel(source) {
    const labels = {
        'document': '📄 Your Document',
        'google_search': '🌐 Google Search',
        'gemini_fallback': '🤖 Gemini Knowledge',
        'web-search': '🔍 Web Search'
    };
    return labels[source] || source;
}

function showWebSearchPrompt() {
    document.getElementById('webSearchPrompt').style.display = 'block';
}

function hideWebSearchPrompt() {
    document.getElementById('webSearchPrompt').style.display = 'none';
}

function showError(message) {
    // Remove existing error messages
    document.querySelectorAll('.error').forEach(err => err.remove());
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.textContent = message;
    
    // Insert after the container header
    const header = document.querySelector('header');
    header.insertAdjacentElement('afterend', errorDiv);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Restart session function
function restartSession() {
    currentSessionId = null;
    currentQuestion = null;
    
    // Clear all inputs
    document.getElementById('fileInput').value = '';
    document.getElementById('urlInput').value = '';
    document.getElementById('textInput').value = '';
    document.getElementById('questionInput').value = '';
    
    // Clear context inputs
    document.getElementById('contextFileInput').value = '';
    document.getElementById('contextUrlInput').value = '';
    document.getElementById('contextTextInput').value = '';
    
    // Reset active states
    document.querySelectorAll('.upload-method').forEach(m => m.classList.remove('active'));
    document.querySelectorAll('.context-method').forEach(m => m.classList.remove('active'));
    document.querySelector('.upload-method[data-method="file"]').classList.add('active');
    document.querySelector('.context-method[data-method="file"]').classList.add('active');
    
    // Show upload section and hide content info
    document.getElementById('uploadSection').style.display = 'block';
    document.getElementById('contentInfo').style.display = 'none';
    document.getElementById('processing').style.display = 'none';
    
    // Hide modal if open
    hideAddContextModal();
    hideWebSearchPrompt();
    
    // Clear any error messages
    document.querySelectorAll('.error').forEach(err => err.remove());
}

// Modal functions
function showAddContextModal() {
    document.getElementById('addContextModal').style.display = 'flex';
}

function hideAddContextModal() {
    document.getElementById('addContextModal').style.display = 'none';
    // Clear context inputs
    document.getElementById('contextFileInput').value = '';
    document.getElementById('contextUrlInput').value = '';
    document.getElementById('contextTextInput').value = '';
}

// Context upload handlers
function handleContextFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    if (!currentSessionId) {
        showError('Please start a session first');
        return;
    }
    
    hideAddContextModal();
    showContextProcessing();
    
    const formData = new FormData();
    formData.append('file', file);
    formData.append('session_id', currentSessionId);
    
    fetch('/api/add-context', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        hideProcessing();
        if (data.success) {
            // Update summary and ensure content info is visible
            const summaryElement = document.getElementById('summaryContent');
            summaryElement.textContent = data.summary;
            
            // Add visual indication that summary was updated
            summaryElement.classList.add('summary-updated');
            setTimeout(() => {
                summaryElement.classList.remove('summary-updated');
            }, 2000);
            document.getElementById('uploadSection').style.display = 'none';
            document.getElementById('contentInfo').style.display = 'block';
            
            // Add enhanced message with preview
            if (data.added_content) {
                const preview = data.added_content.preview;
                const previewHtml = `
                    <div class="added-content-preview">
                        <strong>📄 Added: ${data.added_content.name}</strong><br>
                        <div class="preview-stats">
                            ${preview.document_count} document(s), ${preview.character_count.toLocaleString()} characters
                        </div>
                        <div class="preview-text">${preview.text_preview}</div>
                    </div>
                `;
                addMessage(previewHtml, 'assistant', 'system');
            } else {
                addMessage(`📄 Added new file: ${file.name}`, 'assistant', 'system');
            }
        } else {
            document.getElementById('contentInfo').style.display = 'block';
            showError(data.error || 'Failed to add context');
        }
    })
    .catch(error => {
        hideProcessing();
        document.getElementById('contentInfo').style.display = 'block';
        showError('Failed to add context: ' + error.message);
    });
}

function addContextUrl() {
    const url = document.getElementById('contextUrlInput').value.trim();
    if (!url) {
        showError('Please enter a valid URL');
        return;
    }
    
    if (!currentSessionId) {
        showError('Please start a session first');
        return;
    }
    
    hideAddContextModal();
    showContextProcessing();
    
    fetch('/api/add-context', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            url: url,
            session_id: currentSessionId 
        })
    })
    .then(response => response.json())
    .then(data => {
        hideProcessing();
        if (data.success) {
            // Update summary and ensure content info is visible
            const summaryElement = document.getElementById('summaryContent');
            summaryElement.textContent = data.summary;
            
            // Add visual indication that summary was updated
            summaryElement.classList.add('summary-updated');
            setTimeout(() => {
                summaryElement.classList.remove('summary-updated');
            }, 2000);
            document.getElementById('uploadSection').style.display = 'none';
            document.getElementById('contentInfo').style.display = 'block';
            
            // Add enhanced message with preview
            if (data.added_content) {
                const preview = data.added_content.preview;
                const previewHtml = `
                    <div class="added-content-preview">
                        <strong>🌐 Added: ${data.added_content.name}</strong><br>
                        <div class="preview-stats">
                            ${preview.document_count} document(s), ${preview.character_count.toLocaleString()} characters
                        </div>
                        <div class="preview-text">${preview.text_preview}</div>
                    </div>
                `;
                addMessage(previewHtml, 'assistant', 'system');
            } else {
                addMessage(`🌐 Added content from: ${url}`, 'assistant', 'system');
            }
        } else {
            document.getElementById('contentInfo').style.display = 'block';
            showError(data.error || 'Failed to add context');
        }
    })
    .catch(error => {
        hideProcessing();
        document.getElementById('contentInfo').style.display = 'block';
        showError('Failed to add context: ' + error.message);
    });
}

function addContextText() {
    const text = document.getElementById('contextTextInput').value.trim();
    if (!text) {
        showError('Please enter some text');
        return;
    }
    
    if (!currentSessionId) {
        showError('Please start a session first');
        return;
    }
    
    hideAddContextModal();
    showContextProcessing();
    
    fetch('/api/add-context', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            text: text,
            session_id: currentSessionId 
        })
    })
    .then(response => response.json())
    .then(data => {
        hideProcessing();
        if (data.success) {
            // Update summary and ensure content info is visible
            const summaryElement = document.getElementById('summaryContent');
            summaryElement.textContent = data.summary;
            
            // Add visual indication that summary was updated
            summaryElement.classList.add('summary-updated');
            setTimeout(() => {
                summaryElement.classList.remove('summary-updated');
            }, 2000);
            document.getElementById('uploadSection').style.display = 'none';
            document.getElementById('contentInfo').style.display = 'block';
            
            // Add enhanced message with preview
            if (data.added_content) {
                const preview = data.added_content.preview;
                const previewHtml = `
                    <div class="added-content-preview">
                        <strong>📝 Added: ${data.added_content.name}</strong><br>
                        <div class="preview-stats">
                            ${preview.document_count} document(s), ${preview.character_count.toLocaleString()} characters
                        </div>
                        <div class="preview-text">${preview.text_preview}</div>
                    </div>
                `;
                addMessage(previewHtml, 'assistant', 'system');
            } else {
                addMessage(`📝 Added additional text content`, 'assistant', 'system');
            }
        } else {
            document.getElementById('contentInfo').style.display = 'block';
            showError(data.error || 'Failed to add context');
        }
    })
    .catch(error => {
        hideProcessing();
        document.getElementById('contentInfo').style.display = 'block';
        showError('Failed to add context: ' + error.message);
    });
}