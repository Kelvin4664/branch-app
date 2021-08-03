let currentRecipient = '';
let chatInput = $('#chat-input');
let chatButton = $('#btn-send');
let userList = $('#user-list');
let messageList = $('#messages');

function updateTicketList() {
    $.getJSON('api/v1/tickets/', function (data) {
        userList.children('.user').remove();
        for (let i = 0; i < data.length; i++) {
            const userItem = `<a class="list-group-item user" data-ticketid=${data[i]['id']}>${data[i]['title']}</a>`;
            $(userItem).appendTo('#user-list');
        }
        $('.user').click(function (event) {
            userList.children('.active').removeClass('active');
            let selected = event.target;
            $(selected).addClass('active');
            setCurrentTicket($(selected).data("ticketid"));
        });
    });
}

function drawMessage(message) {
    let position = 'left';
    const date = new Date(message.date_sent);
    if (message.sender === currentUser) position = 'right';
    const messageItem = `
            <li class="message ${position}">
                <div class="avatar">${message.user}</div>
                    <div class="text_wrapper">
                        <div class="text">${message.body}<br>
                            <span class="small">${date}</span>
                    </div>
                </div>
            </li>`;
    $(messageItem).appendTo('#messages');
}

function getConversation(currentTicket) {
    $.getJSON(`api/v1/tickets/${currentTicket}/messages`, function (data) {
        messageList.children('.message').remove();
        for (let i = data.length - 1; i >= 0; i--) {
            drawMessage(data[i]);
        }
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });

}

function getMessageById(message) {
    id = JSON.parse(message).message
    $.getJSON(`api/v1/tickets/${currentTicket}/messages/${id}/`, function (data) {
        drawMessage(data)
        messageList.animate({scrollTop: messageList.prop('scrollHeight')});
    });
}

function sendMessage(recipient, body) {
    $.post(`api/v1/tickets/${recipient}/messages/`, {body}).fail(function () {
        alert('Error! Check console!');
    });
}

function setCurrentTicket(ticketId) {
    currentTicket = ticketId;
    getConversation(currentTicket);
    enableInput();
}


function enableInput() {
    chatInput.prop('disabled', false);
    chatButton.prop('disabled', false);
    chatInput.focus();
}

function disableInput() {
    chatInput.prop('disabled', true);
    chatButton.prop('disabled', true);
}

$(document).ready(function () {
    updateTicketList();
    disableInput();

//    let socket = new WebSocket(`ws://127.0.0.1:8000/?session_key=${sessionKey}`);
    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var socket = new WebSocket(
        ws_scheme + window.location.host +
        '/ws?session_key=${sessionKey}')

    chatInput.keypress(function (e) {
        if (e.keyCode == 13)
            chatButton.click();
    });

    chatButton.click(function () {
        if (chatInput.val().length > 0) {
            sendMessage(currentTicket, chatInput.val());
            chatInput.val('');
        }
    });

    socket.onmessage = function (e) {
        data = JSON.parse(e.data)
        if (data.type === 'new_ticket'){
            updateTicketList()
        }else{
            getMessageById(e.data);
        }
        
    };
});



