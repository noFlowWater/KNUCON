<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request'; 
    import { access_token, is_login, username as currentUsername } from '../../lib/store'; // currentUsername 추가
    import { push } from 'svelte-spa-router';
    import { getNotificationsContext } from 'svelte-notifications';
    import { DateTimeFilter } from '../../util';

    const { addNotification } = getNotificationsContext();

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
                    console.log("Post UID:", postDetails.POST_CREATOR);
                    console.log("Current Username:", $currentUsername);

                    canLike = postDetails.POST_CREATOR !== $currentUsername;
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
                    addNotification({
                        text: '본인의 Post입니다.',
                        position: 'bottom-center',
                        type: 'warning',
                        removeAfter: 4000
                    });
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
                        addNotification({
                            text: responseData.error,
                            position: 'bottom-center',
                            type: 'warning',
                            removeAfter: 4000
                        });
                    } else {
                        addNotification({
                            text: '포스트가 위시리스트에서 제거되었습니다.',
                            position: 'bottom-center',
                            type: 'success',
                            removeAfter: 4000
                        });
                        isLiked = false;
                    }
                } catch (error) {
                    console.error('Error removing post from wish list:', error);
                    addNotification({
                        text: '위시리스트에서 제거하는 중 오류가 발생했습니다.',
                        position: 'bottom-center',
                        type: 'error',
                        removeAfter: 4000
                    });
                }
            } else {
                try {
                    const response = await request('POST', '/wishes', { pid: postDetails.POST_ID }, {
                        'Authorization': `Bearer ${$access_token}`
                    });
                    const responseData = (typeof response === 'string') ? JSON.parse(response) : response;

                    if (responseData.error) {
                        addNotification({
                            text: responseData.error,
                            position: 'bottom-center',
                            type: 'warning',
                            removeAfter: 4000
                        });
                    } else {
                        addNotification({
                            text: '포스트가 위시리스트에 추가되었습니다.',
                            position: 'bottom-center',
                            type: 'success',
                            removeAfter: 4000
                        });
                        isLiked = true;
                    }
                } catch (error) {
                    console.error('Error adding post to wish list:', error);
                    addNotification({
                        text: '위시리스트에서 추가하는 중 오류가 발생했습니다.',
                        position: 'bottom-center',
                        type: 'error',
                        removeAfter: 4000
                    });
                }
            }
        } else {
            addNotification({
                text: '내가 쓴 글은 찜할 수 없습니다.',
                position: 'bottom-center',
                type: 'warning',
                removeAfter: 4000
            });
        }
    }


    let showReportDialog = false; // 신고 대화 상자를 표시할지 여부
    let reportReasons = { // 신고 사유
        professionalSeller: false,
        fraud: false,
        abusiveLanguage: false,
        other: false
    };

    // 신고하기 버튼을 눌렀을 때 실행되는 함수
    function reportPost() {
        // 신고 사유가 선택되었는지 확인
        if (!Object.values(reportReasons).some(v => v)) {
            alert('신고 사유를 선택해주세요.');
            return;
        }
        // 서버에 신고 내용 전송 로직 추가...
        alert('신고 접수되었습니다');
        showReportDialog = false; // 대화 상자 숨기기
    }
</script>

<div class="page-container">
    <div class="post-detail">
        {#if isLoading}
            <p>Loading...</p>
        {:else if isError}
            <p>Error loading post details.</p>
        {:else}
            <div class="post-header">
                <h2>{postDetails.POST_TITLE}</h2>
                <div class="post-meta">
                    <span> {#if postDetails.POST_STATUS === 0}
                          들어오세유
                      {:else if postDetails.POST_STATUS === 1}
                          들어갈래유
                      {:else if postDetails.POST_STATUS === 2}
                          끝났뿌따
                      {/if}</span> | 
                    <span><strong>글쓴이:</strong> {postDetails.POST_CREATOR}</span> | 
                    <span><strong>날짜:</strong> {DateTimeFilter(postDetails.POST_DATE)}</span> | 
                    <span><strong>조회수:</strong> {postDetails.POST_VIEW_COUNT}</span>
                </div>
            </div>
            <div class="post-body">
                <p>{postDetails.POST_CONTENT}</p>
            </div>
            {#if postDetails.RID}
                <div class="room-details">
                    <h3 class="room-info-head">
                        Room Information of <span class="room-name">{postDetails.ROOM_NICKNAME}</span> /
                        <span class={postDetails.ROOM_STATUS == 0 ? 'room-status incomplete' : 'room-status complete'}>
                            {postDetails.ROOM_STATUS == 0 ? '연결 미완료' : '연결 완료'}
                        </span>
                    </h3>
                    <p><strong>Address:</strong> {postDetails.ADDRESS}</p>
                    <p><strong>Area:</strong> {postDetails.AREA}</p>
                    <p><strong>Deposit:</strong> {postDetails.DEPOSIT}</p>
                    <p><strong>Price:</strong> {postDetails.PRICE}</p>
                    <p><strong>Room Type:</strong> 
                        {#if postDetails.ROOM_TYPE === 1}
                            원룸
                        {:else if postDetails.ROOM_TYPE === 2}
                            투룸
                        {:else if postDetails.ROOM_TYPE === 3}
                            쓰리룸 이상
                        {/if}
                    </p>
                    <p><strong>Direction:</strong> {postDetails.DIRECTION}</p>
                    <p><strong>Floor:</strong> {postDetails.FLOOR}</p>
                    <p><strong>Gate:</strong> 
                        {#if postDetails.GATE === 0}
                            북문/농장문
                        {:else if postDetails.GATE === 1}
                            서문/수영장문
                        {:else if postDetails.GATE === 2}
                            솔로문/조은문
                        {:else if postDetails.GATE === 3}
                            쪽문/정문/수의대문
                        {:else if postDetails.GATE === 4}
                            테크노문/나리문/동문
                        {/if}
                    </p>
                    <div class="room-options">
                        <p><strong>Contract Status:</strong> 
                            {#if postDetails.IS_CONTRACT === 0}
                                월세
                            {:else if postDetails.IS_CONTRACT === 1}
                                전세
                            {/if}
                        </p>
                        <p><strong>Rent Aid:</strong> <span class="status-indicator {postDetails.RENT_AID ? 'yes' : 'no'}"></span></p>
                        <p><strong>Preview Available:</strong> <span class="status-indicator {postDetails.PREVIEW ? 'yes' : 'no'}"></span></p>
                        <p><strong>Extension Option:</strong> <span class="status-indicator {postDetails.EXTENSION ? 'yes' : 'no'}"></span></p>
                        <p><strong>Electricity Bill Included:</strong> <span class="status-indicator {postDetails.ELEC_BILL ? 'yes' : 'no'}"></span></p>
                        <p><strong>Water Bill Included:</strong> <span class="status-indicator {postDetails.WATER_BILL ? 'yes' : 'no'}"></span></p>
                        <p><strong>Gas Bill Included:</strong> <span class="status-indicator {postDetails.GAS_BILL ? 'yes' : 'no'}"></span></p>
                        <p><strong>Kitchen Separated:</strong> <span class="status-indicator {postDetails.KIT_SEP ? 'yes' : 'no'}"></span></p>
                        <p><strong>Stove Type:</strong> 
                            {#if postDetails.STOVE_TYPE === 0}
                                가스레인지
                            {:else if postDetails.STOVE_TYPE === 1}
                                인덕션
                            {/if}
                        </p>
                        <p><strong>Fridge Included:</strong> <span class="status-indicator {postDetails.FRIDGE ? 'yes' : 'no'}"></span></p>
                        <p><strong>Air Conditioning:</strong> <span class="status-indicator {postDetails.AC ? 'yes' : 'no'}"></span></p>
                        <p><strong>Microwave Included:</strong> <span class="status-indicator {postDetails.MW ? 'yes' : 'no'}"></span></p>
                        <p><strong>Balcony Available:</strong> <span class="status-indicator {postDetails.BALCONY ? 'yes' : 'no'}"></span></p>
                        <p><strong>Dryer Included:</strong> <span class="status-indicator {postDetails.DRYER ? 'yes' : 'no'}"></span></p>
                    </div>
                    <!-- 'PICTURE' 필드는 이미지 처리가 필요하므로 별도로 처리 -->
                    <!-- <img src={postDetails.PICTURE} alt="Room Image" /> -->
                </div>
            {/if}
            <div class="post-actions">
                {#if $access_token && canLike}
                    <button class="chat-button" on:click={startChat}>Start Chat</button>
                    <div class="like-button" on:click={toggleLike}>
                        {#if isLiked}
                            <img src="/full-heart.png" alt="Liked" />
                        {:else}
                            <img src="/empty-heart.png" alt="Not Liked" />
                        {/if}
                    </div>
                {/if}
            </div>
        {/if}
    </div>
</div>

<style>
    .post-detail {
        font-family: 'Arial', sans-serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
        background-color: #fff;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    }

    .post-detail h1, .post-header h2, .room-details h3 {
        text-align: center;
        color: #333;
    }

    .post-header {
        background-color: #f8f9fa;
        padding: 15px;
        border-bottom: 1px solid #ddd;
    }

    .post-meta {
        text-align: center;
        color: #666;
        font-style: italic;
        margin-top: 10px;
    }

    .post-body {
        padding: 20px;
        line-height: 1.6;
    }
    .room-info-head {
        font-size: 1.2em; /* Adjust the font size */
        color: #333; /* Dark text color for readability */
        margin: 10px 0; /* Margin for spacing */
        font-weight: normal; /* Normal font weight */
    }

    .room-name {
        color: #007BFF; /* Highlight color for the room name */
        font-weight: bold; /* Bold font weight for emphasis */
    }
    .room-status.incomplete {
        color: #28A745; /* Green color for incomplete status */
        font-weight: bold; /* Bold font weight for emphasis */
    }
    .room-status.complete {
        color: #DC3545; /* Red color for complete status */
        font-weight: bold; /* Bold font weight for emphasis */
    }

    .room-details {
        background-color: #f9f9f9;
        padding: 15px;
        margin-top: 20px;
        border-radius: 5px;
    }

    .post-actions {
        text-align: center;
        padding: 20px;
        border-top: 1px solid #ddd;
        margin-top: 20px;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-left: 5px;
    }

    .status-indicator.yes::after {
        content: '';
        display: block;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: green;
    }

    .status-indicator.no::after {
        content: '';
        display: block;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: red;
    }

    .chat-button {
        background-color: #007bff; /* 밝은 파란색 */
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 5px;
        font-weight: bold;
        cursor: pointer;
        transition: background-color 0.3s ease;
    }

    .chat-button:hover {
        background-color: #0056b3; /* 좀 더 어두운 파란색 */
    }
</style>
