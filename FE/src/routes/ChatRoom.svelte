<script>
    import { onMount, onDestroy } from 'svelte';
    import request from '../lib/request'; 
    import { access_token } from '../lib/store';
    import { pop } from 'svelte-spa-router';
    import { getNotificationsContext } from 'svelte-notifications';

    const { addNotification } = getNotificationsContext();

    export let params = {};

    let postId = params.postId;
    let chatRoomId = params.chatRoomId;
    
    let messages = [];
    let isPostCreator = false; // 현재 사용자가 POST의 작성자인지 여부
    let isChatRoomCreator = false; // 현재 사용자가 채팅방의 CREATOR인지 여부

    let websocket;
    let newMessage = ''; // 사용자가 입력하는 새 메시지

    onMount(async () => {
        try {
            // 현재 사용자의 User_ID GET
            const userResponse = await request('GET', `/users/me`, {}, {
                'Authorization': `Bearer ${$access_token}`
            });
            const currentUser = userResponse ? JSON.parse(userResponse).user_id : null;

            // 현재 사용자가 post작성자인지 확인
            const postResponse = await request('GET', `/posts/${postId}/creator`, {}, {
                'Authorization': `Bearer ${$access_token}`
            });
            const postCreator = postResponse ? JSON.parse(postResponse).UID : null;
            isPostCreator = currentUser === postCreator;

            // 현재 사용자가 Chatroom Creator인지 확인
            const chatRoomResponse = await request('GET', `/chatrooms/${postId}/${chatRoomId}/creator`, {}, {
                'Authorization': `Bearer ${$access_token}`
            });
            const chatRoomCreator = chatRoomResponse ? JSON.parse(chatRoomResponse).CREATOR_UID : null;
            isChatRoomCreator = currentUser === chatRoomCreator;
            console.log(isPostCreator,isChatRoomCreator)
            if (isPostCreator || isChatRoomCreator) {
                // 진행
                const messagesResponse = await request('GET', `/chatrooms/${postId}/${chatRoomId}/messages`, {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (messagesResponse) {
                    const messagesResult = JSON.parse(messagesResponse);
                    messages = messagesResult;
                }
            } else {
                console.error('잘못된 접근입니다.');
                pop(); // 잘못된 접근 - 페이지 뒤로 이동
            }
        } catch (error) {
            console.error('Error:', error);
            pop(); // 에러 발생 - 페이지 뒤로 이동
        }

        websocket = new WebSocket(`ws://localhost:8000/chatrooms/ws/${postId}/${chatRoomId}`);
        
        websocket.onmessage = (event) => {
            const message = JSON.parse(event.data);
            console.log(message);
            messages = [...messages, message];

            // 새 메시지를 추가한 후에 페이지 스크롤을 맨 아래로 이동
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight);
            },0); // 적절한 지연 시간 설정
        };
        websocket.onopen = (event) => {
            console.log('WebSocket connection established', event);
            addNotification({
                text: '채팅방에 입장했습니다!',
                position: 'bottom-center',
                type: 'success',
                removeAfter: 4000
            });
            setTimeout(() => {
                window.scrollTo(0, document.body.scrollHeight);
            },0); // 적절한 지연 시간 설정
        };

        websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        websocket.onclose = (event) => {
            console.log('WebSocket connection closed', event);
            addNotification({
                text: '채팅방 소캣 연결이 끊겼습니다.',
                position: 'bottom-center',
                type: 'warning',
                removeAfter: 6000
            });
        };
    });
    // 컴포넌트 파괴 시 웹소켓 연결 해제
    onDestroy(() => {
        if (websocket) {
            websocket.close();
        }
    });
    // 메시지 전송 함수
    function sendMessage() {
        if (newMessage.trim() !== '') {
            const isoString = new Date().toISOString();
            const formattedString = formatDateTime(isoString);
            const message = {
                PID: postId,
                CID: chatRoomId,
                TIME: formattedString,
                IS_CREATOR: isChatRoomCreator ? 1 : 0, // 채팅방의 CREATOR 기준으로 설정
                MSG_CONTENT: newMessage
            };
            websocket.send(JSON.stringify(message));
            newMessage = ''; // 입력 필드 초기화
        }
    }
    function handleSubmit(event) {
        event.preventDefault();
        sendMessage();
    }
    function formatDateTime(dateTimeString) {
        // ISO 형식의 문자열을 받아 변환
        return dateTimeString
            .replace('T', ' ')  // 'T'를 공백으로 대체
            .slice(0, -1);      // 마지막 문자 ('Z') 제거
    }
    function DateTimeFilter(dateTimeStr) {
        const date = new Date(dateTimeStr);
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        
        return `${year}-${month}-${day} ${hours}:${minutes}`;
    }
    // 메시지가 현재 사용자에 의해 보내졌는지 확인하는 함수
    function isMessageFromCurrentUser(message) {
        return (isPostCreator && !message.IS_CREATOR) || 
               (isChatRoomCreator && message.IS_CREATOR);
    }
</script>

<div class="page-container">
    <div class="chatingroom-page">
        <header class="chat-header">
            <div>Post ID: {postId}</div>
            <div>Chat Room ID: {chatRoomId}</div>
        </header>
        <div class="chat-container">
            <section class="chat-room">
                {#each messages as message}
                    <article class="message {isMessageFromCurrentUser(message) ? 'user-message' : 'other-message'}">
                        <header class="message-header">
                            <time datetime="{message.TIME}">{DateTimeFilter(message.TIME)}</time>
                        </header>
                        <p class="content">{message.MSG_CONTENT}</p>
                    </article>
                {/each}
            </section>

            
            <form on:submit={handleSubmit} class="message-form">
                <footer class="message-input">
                    <input type="text" id="text" bind:value={newMessage} placeholder="Type a message..." autocomplete="off"/>
                    <button type="submit" class="send-button">Send</button>
                </footer>
            </form>
            
        </div>
    </div>
</div>

<style>
    .chatingroom-page {
        font-family: 'Arial', sans-serif;
        margin: 0 auto;
        padding: 20px;
        padding-bottom: 70px; /* 메시지 입력 폼의 높이에 따라 조정 */
        background-color: #fff;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        position: relative; /* 상대적 위치 설정 */
    }
    
    .chat-header {
        text-align: center;
        margin-bottom: 20px;
    }

    .chat-header h1 {
        color: #333;
    }

    .chat-container {
        display: flex;
        flex-direction: column;
        margin: auto;
        overflow: hidden;
    }

    .chat-room {
        flex-grow: 1; /* 채팅 내용이 공간을 채움 */
        overflow-y: auto; /* 세로 스크롤 활성화 */
        align-items: flex-start; /* 기본 정렬을 왼쪽으로 설정 */
        padding: 10px;
        margin-bottom: 10px; /* 폼과의 간격 조정 */
        display: flex;
        flex-direction: column;
    }
    .message {
        margin: 10px 0;
        padding: 10px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .user-message, .other-message {
        max-width: 70%; /* 메시지의 최대 너비 제한 */
        width: fit-content; /* 메시지 내용에 맞게 너비 조정 */
        margin: 10px 0;
        padding: 10px;
        border-radius: 20px;
        color: white;
        box-shadow: 0 13px 12px rgba(0, 0, 0, 0.2);
    }
    .user-message {
        align-self: flex-end;
        background-color: #007bff;
    }

    .other-message {
        align-self: flex-start;
        background-color: #6c757d;
    }
    
    .message-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 5px;
    }

    .message-header h2 {
        margin: 0;
        font-size: 14px;
    }

    .content {
        font-size: 16px;
        margin: 0;
    }

    time {
        font-size: 12px;
        color: rgba(255, 255, 255, 0.6);
    }
    
.chat-header {
    text-align: center;
    margin-bottom: 20px;
}

.chat-header h1 {
    color: #333;
}
.message-form {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px;
    background-color: #f9f9f9;
    border-top: 1px solid #ddd;
    position: fixed;
    bottom: 0;
    width: calc(100% - 40px); /* 페이지 컨테이너의 패딩에 맞춤 */
}
.message-input {
    width: 100%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.message-input input[type="text"] {
    width: 85%;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-right: 10px;
}

.send-button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.send-button:hover {
    background-color: #45a049;
}

</style>
