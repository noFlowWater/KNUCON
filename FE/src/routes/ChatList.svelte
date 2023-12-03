<script>
    import { onMount } from 'svelte';
    import { push } from 'svelte-spa-router';
    import request from '../lib/request'; 
    import { access_token, is_login } from '../lib/store'; 

    let chatRooms = []; // This will hold the list of chat rooms
    let isLoading = true;
    let isError = false;

    onMount(async () => {
        if($is_login){
            try {
                // '/mypage/posts' 엔드포인트로부터 게시글 목록 가져오기
                const response = await request('GET', '/chatrooms/list', {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {chatRooms = JSON.parse(response);}
            } catch (error) {
                console.error('Error fetching posts:', error);
                isError = true;
            } finally {
                isLoading = false;
            }
        }
    });
    function enterChatRoom(postId, chatRoomId) {
        // navigate 함수를 이용하여 페이지 이동과 함께 데이터 전달
        push(`/posts/${postId}/${chatRoomId}`);
    }
</script>

<div class="page-container">
    <div class="chat-list">
        <h1>채팅방 List</h1>
        {#if isLoading}
            <p>Loading chatrooms...</p>
        {:else if isError}
            <p>채팅방 리스트를 불러오는 데 문제가 발생했습니다.</p>
        {:else if chatRooms.length > 0}
            <div class="chatroom-list">
                {#each chatRooms as chatRoom}
                    <div class="chatroom" on:click={enterChatRoom(chatRoom.POST_ID, chatRoom.CHATROOM_ID)}>
                        <h2>{chatRoom.POST_TITLE}</h2>
                        <p class="user-name">User: {chatRoom.OTHER_USER_NAME}</p>
                        <p class="latest-message">Last message: {chatRoom.LATEST_MESSAGE}</p>
                        <p class="message-time">{chatRoom.LATEST_MESSAGE_TIME}</p>
                    </div>
                {/each}
            </div>
        {:else}
            <p>내가 속한 채팅방이 없습니다.</p>
        {/if}
    </div>
</div>

<style>
  .chat-list {
    font-family: 'Arial', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.chat-list h1 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
}

.chatroom-list {
    display: grid;
    grid-gap: 15px;
}

.chatroom {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    padding: 15px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.chatroom:hover {
    background-color: #eaeaea;
}

.chatroom h2 {
    margin-top: 0;
    color: #007bff;
}

.user-name, .latest-message, .message-time {
    color: #666;
    margin: 5px 0;
}

</style>