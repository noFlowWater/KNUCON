<script>
    import { onMount } from 'svelte';
    import request from '../lib/request'; 
    import { access_token, is_login, username as currentUsername } from '../lib/store'; // currentUsername 추가
    import { push } from 'svelte-spa-router';

    export let params = {};

    let postDetails = {};
    let isLoading = true;
    let isError = false;
    let isLiked = false;
    let canLike = true; 
    

    onMount(async () => {
        if ($is_login) {
            try {
                const response = await request('GET', `/posts/${params.postId}`, {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {
                    postDetails = JSON.parse(response);
                    console.log("Post UID:", postDetails.UID);
                    console.log("Current Username:", $currentUsername);

                    canLike = postDetails.UID !== $currentUsername;
                    console.log("Can Like:", canLike);
                    if (canLike) {
                        await checkWishList();
                    }
                } else {
                    isError = true;
                }
            } catch (error) {
                console.error('Error fetching post details:', error);
                isError = true;
            } finally {
                isLoading = false;
            }
        } else {
            isLoading = false;
        }
    });

    async function startChat() {
        try {
            // 현재 사용자의 ID를 가져오는 로직
            let userId = '';
            let chatRoomId ='';
            const userResponse = await request('GET', `/users/me`, {}, {
                'Authorization': `Bearer ${$access_token}`
            });
            if (userResponse) {
                const userResult = JSON.parse(userResponse);
                userId = userResult.user_id;

                // 현재 사용자가 POST 작성자인지 확인
                if (userId === postDetails.UID) {
                    // 현재 사용자가 POST 작성자인 경우
                    // 해당 POST에 물려있는 CHATROOMLIST로 push.
                } else {
                    // 현재 사용자가 POST 작성자가 아닌 경우
                    chatRoomId = await initializeChatRoom(postDetails.POST_ID);
                    if(chatRoomId){
                        enterChatRoom(postDetails.POST_ID, chatRoomId)
                    }else{
                        console.error("ChatRoom initialize fail : chatRoomId null..")
                    }
                }
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    async function initializeChatRoom(postId) {
        try {
            let chatRoomId = ''
            const response = await request('POST', `/chatrooms/start/${postId}`, {}, {
                'Authorization': `Bearer ${$access_token}`
            });

            if (response) {
                const result = JSON.parse(response);
                console.log("Chatroom initialized:", result);
                chatRoomId = result.chatroom_id;
                return chatRoomId; // 채팅방 ID 반환
            } else {
                console.error('No response received from the server');
                return null; // 서버로부터 응답이 없는 경우
            }
        } catch (error) {
            console.error('Error initializing chatroom:', error);
            return null; // 오류 발생 시 null 반환
        }
    }
    function enterChatRoom(postId, chatRoomId) {
        // navigate 함수를 이용하여 페이지 이동과 함께 데이터 전달
        push(`/posts/${postId}/${chatRoomId}`);
    }

    async function checkWishList() {
        if ($is_login) {
            try {
                const response = await request('GET', '/wishes', {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {
                    console.log(response);
                    const wishList = JSON.parse(response);
                    const isPostInWishList = wishList.some(item => item.pid === postDetails.POST_ID);
                    if (isPostInWishList) {
                        isLiked = true;
                    }
                }
            } catch (error) {
                console.error('Error checking wish list:', error);
            }
        }
    }



    async function toggleLike() {
        if (canLike) {
            if (isLiked) {
                try {
                    const response = await request('DELETE', `/wishes/${postDetails.POST_ID}`, {}, {
                        'Authorization': `Bearer ${$access_token}`
                    });
                    const responseData = (typeof response === 'string') ? JSON.parse(response) : response;

                    if (responseData.error) {
                        alert(responseData.error);
                    } else {
                        alert('포스트가 위시리스트에서 제거되었습니다.');
                        isLiked = false;
                    }
                } catch (error) {
                    console.error('Error removing post from wish list:', error);
                    alert('위시리스트에서 제거하는 중 오류가 발생했습니다.');
                }
            } else {
                try {
                    const response = await request('POST', '/wishes', { pid: postDetails.POST_ID }, {
                        'Authorization': `Bearer ${$access_token}`
                    });
                    const responseData = (typeof response === 'string') ? JSON.parse(response) : response;

                    if (responseData.error) {
                        alert(responseData.error);
                    } else {
                        alert('포스트가 위시리스트에 추가되었습니다.');
                        isLiked = true;
                    }
                } catch (error) {
                    console.error('Error adding post to wish list:', error);
                    alert('위시리스트에 추가하는 중 오류가 발생했습니다.');
                }
            }
        } else {
            alert('내가 쓴 글은 찜할 수 없습니다.');
        }
    }

</script>
<div class="page-container">
    <h1>Post Detail</h1>
    {#if isLoading}
        <p>Loading...</p>
    {:else if isError}
        <p>Error loading post details.</p>
    {:else}
        <p>POST_ID : {postDetails.POST_ID}</p>
        <p>RID : {postDetails.RID}</p>
        <p>UID : {postDetails.UID}</p>
        <p>POST_STATUS : {postDetails.POST_STATUS}</p>
        <p>POST_DATE : {postDetails.POST_DATE}</p>
        <p>POST_VIEW_COUNT : {postDetails.POST_VIEW_COUNT}</p>
        <p>POST_CONTENT : {postDetails.POST_CONTENT}</p>
        <p>WISH_COUNT : {postDetails.WISH_COUNT}</p>
        <!-- ROOM 관련 데이터 추가 -->
        <!-- 조건부 렌더링을 사용하여 ROOM 데이터가 있는 경우에만 표시 -->
        {#if postDetails.RID}
            <!-- <p>ROOM_ID : {postDetails.ROOM_ID}</p>
            <p>ROOM_UID : {postDetails.ROOM_UID}</p> -->
            <p>ROOM_DATE : {postDetails.ROOM_DATE}</p>
            <p>ROOM_STATUS : {postDetails.ROOM_STATUS}</p>
            <p>ROOM_NICKNAME : {postDetails.ROOM_NICKNAME}</p>
            <p>ADDRESS : {postDetails.ADDRESS}</p>
            <p>AREA : {postDetails.AREA}</p>
            <p>DEPOSIT : {postDetails.DEPOSIT}</p>
            <p>PRICE : {postDetails.PRICE}</p>
            <p>ROOM_TYPE : {postDetails.ROOM_TYPE}</p>
            <p>DIRECTION : {postDetails.DIRECTION}</p>
            <p>FLOOR : {postDetails.FLOOR}</p>
            <p>GATE : {postDetails.GATE}</p>
            <p>IS_CONTRACT : {postDetails.IS_CONTRACT}</p>
            <p>RENT_AID : {postDetails.RENT_AID}</p>
            <p>PREVIEW : {postDetails.PREVIEW}</p>
            <p>EXTENSION : {postDetails.EXTENSION}</p>
            <p>ELEC_BILL : {postDetails.ELEC_BILL}</p>
            <p>WATER_BILL : {postDetails.WATER_BILL}</p>
            <p>GAS_BILL : {postDetails.GAS_BILL}</p>
            <p>KIT_SEP : {postDetails.KIT_SEP}</p>
            <p>STOVE_TYPE : {postDetails.STOVE_TYPE}</p>
            <p>FRIDGE : {postDetails.FRIDGE}</p>
            <p>AC : {postDetails.AC}</p>
            <p>MW : {postDetails.MW}</p>
            <p>BALCONY : {postDetails.BALCONY}</p>
            <p>DRYER : {postDetails.DRYER}</p>
            <!-- 'PICTURE' 필드는 이미지 처리가 필요하므로 별도로 처리 -->
            <!-- <img src={postDetails.PICTURE} /> -->
        {/if}
        <button on:click={startChat}>Start Chat</button>
        {#if $access_token && canLike}
        <div class="like-button" on:click={toggleLike}>
            {#if isLiked}
                <img src="/full-heart.png" alt="Liked"/>
            {:else}
                <img src="/empty-heart.png" alt="Not Liked"/>
            {/if}
        </div>
        {/if}
    {/if}
</div>

<style>
    .like-button img {
        width: 30px;
        height: auto;
        cursor: pointer;
    }
</style>
