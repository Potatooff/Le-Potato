/* 
BSD 3-Clause License
Copyright (c) 2024, Potatooff
*/

// Global variables   

let llmGenerating = false;
let globalFile = null; // Global variable to store the file object

const renderer = new marked.Renderer(); // marker renderer
const sendButton = document.getElementById('sendButton');
const chatHistory = document.getElementById('chatHistory');
const messageInput = document.getElementById('messageInput');
const chatComboBox = document.getElementById('chatComboBox');
const chosenFileDiv = document.getElementById('chosen-file');
const attachFileButton = document.getElementById('attachFile');


// Set marked options
marked.setOptions({renderer: renderer, gfm: true, breaks: true});


// Adjust the height of the textarea to fix the display bug
function adjustTextareaHeight() {
    messageInput.style.height = 'auto'; 
    messageInput.style.height = messageInput.scrollHeight + 'px';
} 


// Block HTML Injection
function noHTMLinjection(text) {
    return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}


// Configure marked with a custom code for Code Blocks
renderer.code = function(code, language) {
    const escapeHtml = (unsafe) => unsafe
        .replace(/&amp;/g, "&")
        .replace(/&lt;/g, "<")
        .replace(/&gt;/g, ">")
        .replace(/&quot;/g, '"')
        .replace(/&#039;/g, "'");

    const escapedCode = escapeHtml(code);
    const highlighted = language ? hljs.highlight(escapedCode, { language })
        .value : hljs.highlightAuto(escapedCode).value;

    return `
    <pre class="code-block" style="margin-bottom: 10px; margin-top: 10px;">
        <div class="code-toolbar">
            <button class="copy-button material-symbols-rounded" onclick="copyCode(this)">content_copy</button>
        </div>
        <code class="code-content hljs ${language}">${highlighted}</code>
    </pre>`;
        
};

function copyCode(button) {
    const codeElement = button.parentNode.nextElementSibling;
    const code = codeElement.textContent;
    navigator.clipboard.writeText(code)
        .then(() => {
            console.log('Code copied to clipboard');
            // Show a success message or perform any other action
        })
        .catch((error) => {
            console.error('Failed to copy code to clipboard:', error);
            // Show an error message or perform any other action
        });
}

// Copy code to clipboard
function copyCode(button) {
    const codeElement = button.parentNode.nextElementSibling;
    const code = codeElement.textContent;
    navigator.clipboard.writeText(code)
        .then(() => {
            console.log('Code copied to clipboard');
            // Show a success message or perform any other action
        })
        .catch((error) => {
            console.error('Failed to copy code to clipboard:', error);
            // Show an error message or perform any other action
        });
}


// Create a message box for the chat history
function createMessageElement(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('chat-message', 'p-2', 'rounded');

    // FUTURE PROOF CODE 

    if (sender === llm_username) {
        messageElement.innerHTML = `
            <div class="message-content">
                <div class="title-tool-bar">
                    <div class="title">${sender}</div>
                </div>
                <div class="content">${message.trim()}</div>
            </div>
        `;
    } else {
        messageElement.innerHTML = `
            <div class="message-content">
                <div class="title-tool-bar">
                    <div class="title">${sender}</div>
                </div>
                <div class="content">${message}</div>
            </div>
        `;
    }

    // Append the message element to the chat history
    chatHistory.appendChild(messageElement);

    return messageElement;
}


// Add tool bar to AI message
function addToolBar(messageElement) {
    const title_tool_bar_div = messageElement.querySelector('.title-tool-bar');

    // Check if the element already has a tool bar to prevent duplication
    if (!title_tool_bar_div.querySelector('.content-tool-bar')) {
        const toolBarDiv = document.createElement('div');
        toolBarDiv.className = 'content-tool-bar material-symbols-outlined';

        // Create the content_copy icon
        const copyIcon = document.createElement('span');
        copyIcon.className = 'material-symbols-rounded';
        copyIcon.textContent = 'stack';

        // Create the delete icon
        const deleteIcon = document.createElement('span');
        deleteIcon.className = 'material-symbols-rounded';
        deleteIcon.textContent = 'delete';

        // Append icons to the toolbar
        toolBarDiv.appendChild(copyIcon);
        toolBarDiv.appendChild(deleteIcon);

        // Find where to append the toolbar in the message element
        // Assuming you want to append it after the 'content' div
        const titleDiv = messageElement.querySelector('.title');
        if (titleDiv) {
            titleDiv.parentNode.insertBefore(toolBarDiv, titleDiv.nextSibling);
        }
        
        // Show Content Bar
        messageElement.addEventListener('mouseover', function() {
            toolBarDiv.style.opacity = '1';  // Shows the toolbar
        });
        // Hide Content Bar
        messageElement.addEventListener('mouseout', function() {
            toolBarDiv.style.opacity = '0';  // Hides the toolbar
        });

        // Delete function *Check if normal mode is enabled
        if (NormalMode === true) {
            deleteIcon.addEventListener('click', function() {
                // Assuming messageElement has a data attribute like 'data-message-id'
                const messageId = messageElement.getAttribute('data-message-id');
                deleteMessagebyID(messageId, messageElement);
            });
        } else {
            deleteIcon.addEventListener('click', function() {
                // Delete message if normal mode (*test) is disabled
                deleteMessageWihtoutID(messageElement);
            });
            // Delete message
        }

        // Copy function
        copyIcon.addEventListener('click', function() {
            const messageId = messageElement.getAttribute('data-message-id');
            copyToClipboard(messageId);
        });
    }
}


// BACK END COMMUNICATION


// Delete a message by ID
function deleteMessagebyID(messageId, messageElement) {
    // We only send one API CALL and delete both assistant and user messages because BACKEND is handling the deletion of the user message
    fetch('/delete_message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({messageID: messageId}),
    })
    .then(response => {
        if (response.ok) {
            // Delete user message if it exists
            if (messageElement.previousElementSibling) {
                messageElement.previousElementSibling.remove(); // Remove the previous element
            }
            // Remove the message element from the UI
            messageElement.remove();
        } else {
            throw new Error('Failed to delete the message');
        }
    })
    .catch(error => {
        console.error('Error deleting message:', error);
        alert('Error deleting message');
    });
}

function deleteMessageWihtoutID(messageElement) {
    // For the test mode specifically
    if (messageElement.previousElementSibling) {messageElement.previousElementSibling.remove();}
    messageElement.remove();
}

function copyToClipboard(messageID) {
    // Copy a LLM message to the clipboard
    fetch('/copy_message', {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({messageID: messageID}),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        if (navigator.clipboard) { // Checks if the Clipboard API is available
            navigator.clipboard.writeText(data)
            .then(() => {
                null; // Do nothing
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
                alert('Failed to copy text');
            });
        } else {
            // Fallback for older browsers
            const textarea = document.createElement('textarea');
            textarea.value = data;
            document.body.appendChild(textarea);
            textarea.select(); // Selects the text inside the textarea
            document.execCommand('copy'); // Executes the copy command
            document.body.removeChild(textarea);
            alert('Text copied to clipboard!');
        }
    })
    .catch(error => {
        console.error('Error deleting message:', error);
        alert('Error deleting message');
    });

}

// Reset Chat history
function resetChat() {
    messageInput.value = '';
    adjustTextareaHeight(); 
    chatHistory.innerHTML = '';
    chatHistory.scrollTop = chatHistory.scrollHeight; 

    fetch('/clear_history', {
        method: 'POST',
        headers: {'Content-Type': 'application/json',},
        body: JSON.stringify({}),
    })

    return;
}



// This section handles file uploads


// Only display file

function handleFileUpload() {

    // Create a file input element
    const fileInput = document.createElement('input');
    fileInput.type = 'file';
    fileInput.accept = '*';

    // Listen for file selection
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        globalFile = file; // Store the file globally

        if (file) {
            const chosenFileDiv = document.getElementById('chosen-file');
            chosenFileDiv.innerHTML = `<div style="display: flex; align-items: center; font-weight: 500;">
                <span class="material-symbols-outlined" style="font-size: 20px; margin-left: 15px;margin-right: 5px;">
                    description
                </span>
                <span style="font-size: 14px; font-family: "Lexend", sans-serif;">${file.name}</span>
            </div>`;
        }
    });

    fileInput.click();
}

// Handle sending the message or file to the server
function handleSendMessage() {
    
    // Check if there's a file to send
    if (globalFile) {
        const formData = new FormData();
        formData.append('file', globalFile);
        alert('File uploading to the server... now embedding the file... PLEASE WAIT!');

        fetch('/upload-file', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            alert('Embeddings done... use -rag at your next query to query through the file then follows with the model query on a new line!');
            chosenFileDiv.innerHTML = ''; // Clear the file display after sending
            globalFile = null; // Clear the global file reference
        })
        .catch(error => {
            console.error('Error uploading file:', error);
        });
    }

    chosenFileDiv.innerHTML = ''; // Clear the file display
}



// SEND USER QUERY TO THE SERVER
function sendMessage() {
    const rawMessage = messageInput.value.trim();
    const curedRawMessage = noHTMLinjection(messageInput.value.trim());
    
    if (rawMessage && !llmGenerating) {
        
        if (rawMessage === '-clear') {
            resetChat();
        }

        llmGenerating = true;
        messageInput.value = ''; // Clear the textarea
        adjustTextareaHeight();

        setTimeout(() => {
            sendButton.innerHTML = 'check_box_outline_blank';
            sendButton.classList.remove('active');
        }, 100);
        
        
        // Transform user input, display the message and scroll to the latest message | lag with html -> md
        const parsedMessage = marked.parse(curedRawMessage); 
        createMessageElement(user_username, parsedMessage.trim()); 
        chatHistory.scrollTop = chatHistory.scrollHeight; 
        
        // Create LLM Title while waiting for the response
        llm_current_message_div = createMessageElement(llm_username, "") 
        llm_current_message_content_div = llm_current_message_div.querySelector('.content');

        if (NormalMode === true) {


            // Send the message to the server | API CALL
            fetch('/llm_chat_completion', {
                method: 'POST',
                headers: {'Content-Type': 'application/json',},
                body: JSON.stringify({
                    user_query: rawMessage
                }),
            })

            .then(response => {
                if (!response.ok) {throw new Error('Network response was not ok');}
                return response.json(); 
            })

            .then(data => {
                // LLM RESPONSE FOR UI
                let ResponseMessage = marked.parse(data[1]);
                llm_current_message_div.setAttribute('data-message-id', data[0]);
                
                llm_current_message_content_div.innerHTML = ResponseMessage;
                addToolBar(llm_current_message_div)

                // LLM RESPONSE FOR UI
                setTimeout(() => {
                    sendButton.classList.remove('active')
                    sendButton.innerHTML = 'arrow_upward_alt';
                }, 200);

                llmGenerating = false;
                chatHistory.scrollTop = chatHistory.scrollHeight; 
            })

            .catch(error => {
                // LLM ERROR RESPONSE
                llm_current_message_content_div.innerHTML = error;
                addToolBar(llm_current_message_div)

                setTimeout(() => {
                    sendButton.classList.remove('active')
                    sendButton.innerHTML = 'arrow_upward_alt';
                }, 200);

                chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the latest message
                llmGenerating = false;
            });

        } else {
            // LLM RESPONSE FOR CHAT HISTORY
            let  ResponseMessage = marked.parse("Test message... I love you <3"); 
            llm_current_message_content_div.innerHTML = ResponseMessage;
            addToolBar(llm_current_message_div)

            setTimeout(() => {
                sendButton.classList.remove('active')
                sendButton.innerHTML = 'arrow_upward_alt';
            }, 200);
            llmGenerating = false;   
            
            // Scroll to the latest message
            chatHistory.scrollTop = chatHistory.scrollHeight;
        }
    }
}



// UI FEATURES 


// Make all link open to a new tab
document.addEventListener('click', function(e) {
    if (e.target.tagName === 'A') {
        e.target.setAttribute('target', '_blank');
    }
});

// Send button animation
messageInput.addEventListener('input', function() {
    if (this.value.trim().length > 0) {
        sendButton.classList.add('active');
    } else {
        sendButton.classList.remove('active');
    }
});

// Send button to send a message
sendButton.addEventListener('click', sendMessage); 

// Send files from send button
sendButton.addEventListener('click', handleSendMessage); 


// Attach file button command
attachFileButton.addEventListener('click', handleFileUpload); 


// Adjust height listener and send message listener
messageInput.addEventListener('input', adjustTextareaHeight);
messageInput.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault(); 
        sendMessage(); // Send message from enter key
        handleSendMessage(); // Send file from enter key
    }
});


// Chat Page Shortcuts
document.addEventListener('keydown', function(e) {
    const tagName = document.activeElement.tagName.toLowerCase();
    const isEditable = document.activeElement.isContentEditable;
    const isInInputOrTextarea = tagName === 'messageInput' || tagName === 'textarea';

    if (isInInputOrTextarea || isEditable) {
        return; 
    }

    // Shortcut for focusing chat box (Shift + F)
    else if (e.key === 'F' && e.shiftKey && !e.altKey && !e.ctrlKey) { 
            e.preventDefault();
            messageInput.focus();
    }

    // Shortcut for clearing the chat (Shift + N)
    else if (e.key === 'N' && e.shiftKey && !e.altKey && !e.ctrlKey) {
        e.preventDefault(); 
        location.reload(); 
    }
});  

// Adjust height at the start!
adjustTextareaHeight(); // This fix a visual bug with text box