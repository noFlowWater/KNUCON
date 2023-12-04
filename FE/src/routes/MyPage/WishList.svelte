<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request';
    import { push } from 'svelte-spa-router';
    import { access_token, is_login } from '../../lib/store';
    import { DateTimeFilter, getPostStatusClass } from "../../util";

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
        {#each wishes as wish}
          <div class="post" on:click={() => navigateToPostDetail(wish.POST_ID)}>
              <div class="post-header">
                  <h2 class="post-title">{wish.POST_TITLE}</h2>
                  <span class={getPostStatusClass(wish.POST_STATUS)}>
                      {#if wish.POST_STATUS === 0}
                          들어오세유
                      {:else if wish.POST_STATUS === 1}
                          들어갈래유
                      {:else if wish.POST_STATUS === 2}
                          끝났뿌따
                      {/if}
                  </span>
              </div>
              <div class="post-details">
                  <span class="post-id">ID: {wish.POST_ID}</span>
                  <span class="post-author">글쓴이: {wish.UID}</span>
                  <span class="post-date">{DateTimeFilter(wish.POST_DATE)}</span>
                  <span class="post-views">조회수: {wish.POST_VIEW_COUNT}</span>
                  <span class="post-wishes">찜: {wish.WISH_COUNT}</span>
              </div>
          </div>
        {/each}
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
