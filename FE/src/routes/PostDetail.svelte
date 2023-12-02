<!-- PostDetail.svelte -->
<script>
    import { onMount } from 'svelte';
    import request from '../lib/request'; 
    import { access_token, is_login } from '../lib/store'; 
    export let params = {}

    let postDetails = {};
    let isLoading = true;
    let isError = false;

    onMount(async () => {
        console.log("postId: "+params.postId)
        if($is_login) {
            try {
                const response = await request('GET', `/posts/${params.postId}`, {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {postDetails = JSON.parse(response);}
            } catch (error) {
                console.error('Error fetching post details:', error);
                isError = true;
            } finally {
                isLoading = false;
            }
        }
    });

     // Function to handle chatroom creation/start
    async function startChat() {
        if($is_login) {
            try {
                const response = await request('POST', `/chatroom/start/${postDetails.POST_ID}`, {}, {
                    'Authorization': `Bearer ${$access_token}`
                });

                if (response) {
                    const { chatroomId } = JSON.parse(response);
                    // navigate to the chatroom UI, replace '/chat' with your actual chat UI route
                    window.location.href = `/chat/${chatroomId}`; 
                }
            } catch (error) {
                console.error('Error starting chat:', error);
                // handle errors appropriately
            }
        } else {
            console.log("User must be logged in to start a chat.");
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
    {/if}
</div>