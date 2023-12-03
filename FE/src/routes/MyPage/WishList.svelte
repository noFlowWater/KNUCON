<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request';
    import { push } from 'svelte-spa-router';
    import { access_token, is_login } from '../../lib/store';

    let wishes = [];
    let isLoading = true;
    let isError = false;

    onMount(async () => {
        if ($is_login) {
            try {
                const response = await request('GET', '/mypage/wishes', {}, {
                    'Authorization': `Bearer ${$access_token}`
                });

                if (response) {
                    wishes = JSON.parse(response);
                }
                isLoading = false;
            } catch (error) {
                console.error('Error fetching wishes:', error);
                isLoading = false;
                isError = true;
            }
        }
    });
    async function navigateToPostDetail(post_id){
        console.log("post_id: "+post_id)
        // postId를 이용하여 상세 페이지로 네비게이션
        push(`/posts/${post_id}`);
    }
</script>

<div class="page-container">
    <div class="wishList">
        <h1>찜한 게시글 목록</h1>

        {#if isLoading}
        <p>Loading wishes...</p>
        {:else if isError}
        <p>찜한 게시글을 불러오는 데 문제가 발생했습니다.</p>
        {:else if wishes.length > 0}
        <ul>
            {#each wishes as wish}
            <li>
                <button on:click={() => navigateToPostDetail(wish.POST_ID)}>
                    {wish.POST_TITLE} / {wish.POST_DATE} / Status : {wish.POST_STATUS} / WishCount : {wish.WISH_COUNT}
                </button>
            </li>
            {/each}
        </ul>
        {:else}
        <p>찜한 게시글이 없습니다.</p>
        {/if}
    </div>
</div>
<style>
.wishList {
    font-family: 'Arial', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
.wishList h1 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
}
.wishList p {
    text-align: center;
    color: #666;
}
.wishList ul {
    list-style-type: none;
    padding: 0;
}

.wishList li {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    margin-bottom: 10px;
    padding: 10px;
    border-radius: 5px;
}
.wishList button {
    background-color: #007bff;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    text-align: left;
    width: 100%;
    cursor: pointer;
}

.wishList button:hover {
    background-color: #0056b3;
}

</style>
