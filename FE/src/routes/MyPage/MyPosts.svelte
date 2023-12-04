<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request'; 
    import { push } from 'svelte-spa-router';
    import { access_token, is_login } from '../../lib/store'; 
    import { DateTimeFilter, getPostStatusClass } from "../../util";

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
    <div class="myPosts">
        <h1>내 게시글 목록</h1>
        {#if isLoading}
        <p>Loading posts...</p>
        {:else if isError}
        <p>내 게시글을 불러오는 데 문제가 발생했습니다.</p>
        {:else if posts.length > 0}
        {#each posts as post}
          <div class="post" on:click={() => navigateToPostDetail(post.POST_ID)}>
              <div class="post-header">
                  <h2 class="post-title">{post.POST_TITLE}</h2>
                  <span class={getPostStatusClass(post.POST_STATUS)}>
                    {#if post.POST_STATUS === 0}
                        들어오세유
                    {:else if post.POST_STATUS === 1}
                        들어갈래유
                    {:else if post.POST_STATUS === 2}
                        끝났뿌따
                    {/if}
                </span>
              </div>
              <div class="post-details">
                  <span class="post-id">ID: {post.POST_ID}</span>
                  <span class="post-author">글쓴이: {post.UID}</span>
                  <span class="post-date">{DateTimeFilter(post.POST_DATE)}</span>
                  <span class="post-views">조회수: {post.POST_VIEW_COUNT}</span>
                  <span class="post-wishes">찜: {post.WISH_COUNT}</span>
              </div>
          </div>
        {/each}
        {:else}
        <p>등록된 내 게시글이 없습니다.</p>
        {/if}
    </div>
</div>

<style>
.myPosts {
    font-family: 'Arial', sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
.myPosts h1 {
    text-align: center;
    color: #333;
    margin-bottom: 20px;
}
.myPosts p {
    text-align: center;
    color: #666;
}
.post {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    cursor: pointer;
}

.post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.post-title {
    font-size: 18px;
    color: #007bff;
    margin: 0;
}

    .post-status {
        color: white;
        padding: 3px 6px;
        border-radius: 4px;
        font-size: 14px;
    }

    .status-coming {
        background-color: #28a745; /* Green for coming */
    }

    .status-going {
        background-color: #ffc107; /* Yellow for going */
    }

    .status-ended {
        background-color: #dc3545; /* Red for ended */
    }

.post-details {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 14px;
    color: #666;
}

.post-id, .post-author, .post-date, .post-views, .post-wishes {
    white-space: nowrap;
}

</style>