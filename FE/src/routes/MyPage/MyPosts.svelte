<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request'; 
    import { push } from 'svelte-spa-router';
    import { access_token, is_login } from '../../lib/store'; 

    let posts = [];
    let isLoading = true;
    let isError = false;

    onMount(async () => {
        if($is_login){
            try {
                // '/mypage/posts' 엔드포인트로부터 게시글 목록 가져오기
                const response = await request('GET', '/mypage/posts', {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {posts = JSON.parse(response);}
            } catch (error) {
                console.error('Error fetching posts:', error);
                isError = true;
            } finally {
                isLoading = false;
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
    <h1>내 게시글 목록</h1>
    {#if isLoading}
    <p>Loading posts...</p>
    {:else if isError}
    <p>내 게시글을 불러오는 데 문제가 발생했습니다.</p>
    {:else if posts.length > 0}
    <ul>
        {#each posts as post}
            <li>
                <button on:click={() => navigateToPostDetail(post.POST_ID)}>
                    {post.POST_TITLE} / {post.POST_DATE} / Status : {post.POST_STATUS} / WishCount : {post.WISH_COUNT}
                </button>
            </li>
        {/each}
    </ul>
    {:else}
    <p>등록된 내 게시글이 없습니다.</p>
    {/if}
</div>

<style>
    button {
        background: none;
        border: none;
        padding: 0;
        margin: 0;
        text-align: left;
        color: blue;
        text-decoration: underline;
        cursor: pointer;
    }
    button:hover {
        text-decoration: none;
    }
</style>