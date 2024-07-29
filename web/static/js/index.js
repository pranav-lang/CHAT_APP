$(document).ready(function() {
    $('#send').click(function() {
        var inputData = $('#msg').val();
        $.ajax({
            url: '/run',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({data: inputData}),
            success: function(response) {
                console.log('Message sent:', response);
                $('#msg').val('');  // Clear the input field
            },
            error: function(error) {
                console.log('Error sending message:', error);
            }
        });
    });

    function fetchMessages() {
        fetch('/get_messages')
            .then(function(res) {
                if (!res.ok) {
                    throw new Error('Network response was not ok ' + res.statusText);
                }
                return res.json();
            })
            .then(function(data) {
                const messageContainer = document.querySelector('#message-container');
                messageContainer.innerHTML = '';  // Clear the container before adding new messages
                data.messages.forEach(function(message) {
                    const messageDiv = document.createElement('div');
                    messageDiv.textContent = message;
                    messageContainer.appendChild(messageDiv);
                });
                messageContainer.scrollTop = messageContainer.scrollHeight;
            })
            .catch(function(error) {
                console.error('Error fetching messages:', error);
            });
    }

    setInterval(fetchMessages, 1000);
});
