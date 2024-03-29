/* 
BSD 3-Clause License
Copyright (c) 2024, Potatooff
*/


// Global variables   

const NormalMode = true; // Set to true for real inference, false for dev mode
let llmGenerating = false;
const renderer = new marked.Renderer(); // marker renderer
const sendButton = document.getElementById('sendButton');
const chatHistory = document.getElementById('chatHistory');
const messageInput = document.getElementById('messageInput');
marked.setOptions({renderer: renderer, gfm: true, breaks: true});


// Configure marked with a custom code for Code Blocks
renderer.code = function(code, language) {
    const highlighted = language ? hljs.highlight(code, { language }).value : hljs.highlightAuto(code).value;
    return `<pre class="text-white p-2 rounded" style="background: transparent; border: 1px dashed #F5F5F5; margin-bottom: 15px; margin-top: 0px; margin-left: 15px; padding: 0px;"><div style="display: flex; padding-left: 5px;">${language}</div><code style="background: transparent; padding: 7px;" class="hljs ${language}">${highlighted}</code></pre>`;
};  


// Adjust the height of the textarea to fix the display bug
function adjustTextareaHeight() {
    messageInput.style.height = 'auto'; 
    messageInput.style.height = messageInput.scrollHeight + 'px'; 
} 



// HANDLE ATTACHED FILES
document.getElementById('file-input').onchange = async function(e) {
    let files = e.target.files;
    let formData = new FormData();
  
    // Loop through the selected files and append them to formData
    for (let i = 0; i < files.length; i++) {
      formData.append('files[]', files[i]); // 'files[]' tells Flask to expect an array
    }
  
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData,
        });
        
        if (response.ok) {
            console.log('Files uploaded successfully');
        } else {
            console.error('Upload failed');
        }
    } 
    catch (error) {
        console.error('Error:', error);
    }
};
  
// Clean user query
function noHTMLinjection(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// New \ Reset Chat history
function resetChat() {
    messageInput.value = '';
    adjustTextareaHeight(); 
    chatHistory.scrollTop = chatHistory.scrollHeight; 
    chatHistory.innerHTML = '';

    fetch('/clear_history', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
    })
    return;
}


document.addEventListener('DOMContentLoaded', function() {

    // HANDLE USER TO LLM CONVERSATION
    function sendMessage() {
        const rawMessage = noHTMLinjection(messageInput.value.trim());

        if (rawMessage && !llmGenerating) {
            
            if (rawMessage === 'clearmemory') {
                resetChat();
            }

            llmGenerating = true;
            messageInput.value = ''; // Clear the textarea
            adjustTextareaHeight();
            setTimeout(() => {
                sendButton.innerHTML = 'radio_button_checked';
                sendButton.classList.remove('active')
            }, 75); // Change button to stop generation
            
            
            // Display user message
            const parsedMessage = marked.parse(rawMessage); // MESSAGE TRANSFORM FROM MARKDOWN -> HTML
            createMessageElement('Potatoe', parsedMessage.trim()); 
            chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the latest message
            

            if (NormalMode === true) {

                // Send the message to the server | API CALL
                const requestData = {
                    user_query: rawMessage
                };
                
                fetch('/llm_chat_completion', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(requestData),
                })
                
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    console.log(response);
                    return response.json(); 
                })

                .then(data => {
                    // LLM RESPONSE FOR UI
                    const ResponseMessage = marked.parse(data); // MESSAGE TRANSFORM FROM MARKDOWN -> HTML
                    createMessageElement('Julianne', ResponseMessage);
                    setTimeout(() => {sendButton.innerHTML = 'arrow_upward';}, 75); // Change stop to send icon
                    chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the latest message
                    llmGenerating = false;
                })

                .catch(error => {
                    // LLM ERROR RESPONSE
                    createMessageElement('Julianne', error);
                    setTimeout(() => {sendButton.innerHTML = 'arrow_upward';}, 75); // Change button to arrow
                    chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the latest message
                    llmGenerating = false;
                });
            }

            else {
                // LLM RESPONSE FOR CHAT HISTORY
                const ResponseMessage = "Test message..."; // MESSAGE TRANSFORM FROM MARKDOWN -> HTML
                createMessageElement('Julianne', ResponseMessage);
                setTimeout(() => {sendButton.innerHTML = 'arrow_upward';}, 75); // Change button to arrow
                chatHistory.scrollTop = chatHistory.scrollHeight; // Scroll to the latest message
                llmGenerating = false;        
            }

        }
    }
    
    // Create a message box for the chat history
    function createMessageElement(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message', 'p-2', 'rounded');
        messageElement.innerHTML = `
            <div class="title">${sender}</div>
            <div class="content">${message}</div>
        `;
        chatHistory.appendChild(messageElement);
    }

    // Send Button listeners
    sendButton.addEventListener('click', sendMessage);
    
    // Send button animation
    messageInput.addEventListener('input', function() {
        if (this.value.trim().length > 0) {
            sendButton.classList.add('active');
        } else {
            sendButton.classList.remove('active');
        }
    });

    
    // Mouse light effect
    document.addEventListener('mousemove', function(e) {
        const x = e.clientX;
        const y = e.clientY;
        const intensity = 0.4; 
        const lightRadius = 40; 

        // Note: Make sure wallpaper image is correct!
        document.body.style.backgroundImage = `
            radial-gradient(circle at ${x}px ${y}px, rgba(255, 255, 255, ${intensity}) 0, rgba(255, 255, 255, 0) ${lightRadius}px),
            url('static/images/toji.jpg')
        `;
        // Fix some wallpaper display bugs
        document.body.style.backgroundSize = 'cover';
        document.body.style.backgroundPosition = 'center';
        document.body.style.backgroundRepeat = 'no-repeat';
        document.body.style.backgroundAttachment = 'fixed';

        // Uncomment this for radial gradient background (gradient background from chat.css) and comment background image part.
        /*
        document.body.style.backgroundImage = `
            radial-gradient(circle at ${x}px ${y}px, rgba(255, 255, 255, ${intensity}) 0, rgba(255, 255, 255, 0) ${lightRadius}px),
            radial-gradient(circle at center, #09090b 60%, #18181b 100%)
        `; 
        */
    });


    // Chat Text Box listeners
    messageInput.addEventListener('input', adjustTextareaHeight);
    messageInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault(); 
            sendMessage();
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
                document.getElementById('messageInput').focus();
        }

        // Shortcut for clearing the chat (Shift + N)
        else if (e.key === 'N' && e.shiftKey && !e.altKey && !e.ctrlKey) {
            e.preventDefault(); 
            location.reload(); 
        }
        
    });


    adjustTextareaHeight(); // This fix a visual bug with text box
});
