<script>
import { onMount } from 'svelte';
import request from '../lib/request'; 
import { access_token, is_login, username as currentUsername } from '../lib/store'; // currentUsername 추가

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

async function checkWishList() {
    if ($is_login) {
        try {
            const response = await request('GET', '/wishes', {}, {
                'Authorization': `Bearer ${$access_token}`
            });
            if (response) {
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
    {/if}

    {#if $access_token && canLike}
        <div class="like-button" on:click={toggleLike}>
            {#if isLiked}
                <img src="/full-heart.png" alt="Liked"/>
            {:else}
                <img src="/empty-heart.png" alt="Not Liked"/>
            {/if}
        </div>
    {/if}
</div>

<style>
    .like-button img {
        width: 30px;
        height: auto;
        cursor: pointer;
    }
</style>
