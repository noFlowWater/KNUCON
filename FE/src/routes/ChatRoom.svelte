<script>
    import { onMount, onDestroy } from 'svelte';
    import request from '../lib/request'; 
    import { access_token } from '../lib/store';
    import { pop } from 'svelte-spa-router';

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
        };
        websocket.onopen = (event) => {
            console.log('WebSocket connection established', event);
        };

        websocket.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        websocket.onclose = (event) => {
            console.log('WebSocket connection closed', event);
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
    function formatDateTime(dateTimeString) {
        // ISO 형식의 문자열을 받아 변환
        return dateTimeString
            .replace('T', ' ')  // 'T'를 공백으로 대체
            .slice(0, -1);      // 마지막 문자 ('Z') 제거
    }
    // 메시지가 현재 사용자에 의해 보내졌는지 확인하는 함수
    function isMessageFromCurrentUser(message) {
        return (isPostCreator && !message.IS_CREATOR) || 
               (isChatRoomCreator && message.IS_CREATOR);
    }
</script>


<div>
    <h1>Chat Room</h1>
    <div>Post ID: {postId}</div>
    <div>Chat Room ID: {chatRoomId}</div>

    <div class="messages">
        {#each messages as message}
            <div class="message">
                <div>
                    {isMessageFromCurrentUser(message) ? 'You' : 'Other'}
                    <div>{message.MSG_CONTENT}</div>
                    <div>{message.TIME}</div>
                </div>
            </div>
        {/each}
    </div>

    <div class="message-input">
        <input type="text" bind:value={newMessage} placeholder="Type a message..." />
        <button on:click={sendMessage}>Send</button>
    </div>
</div>

<style>
    /* 여기에 스타일을 추가할 수 있습니다. */
</style>
