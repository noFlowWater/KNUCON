<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request'; 
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
                if (response) {
                    posts = JSON.parse(response);
                }
                isLoading = false;
            } catch (error) {
                console.error('Error fetching posts:', error);
                isLoading = false;
                isError = true;
            }
        }
    });
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
        <li>{post.post_title} / {post.post_date} / Status : {post.post_status}</li>
        {/each}
    </ul>
    {:else}
    <p>등록된 내 게시글이 없습니다.</p>
    {/if}
</div>

<style>
  /* 여기에 스타일링 추가 */
</style>