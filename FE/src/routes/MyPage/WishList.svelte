<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request';
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
</script>

<div class="page-container">
    <h1>찜한 게시글 목록</h1>

    {#if isLoading}
    <p>Loading wishes...</p>
    {:else if isError}
    <p>찜한 게시글을 불러오는 데 문제가 발생했습니다.</p>
    {:else if wishes.length > 0}
    <ul>
        {#each wishes as wish}
        <li>{wish.post_title} / {wish.post_date} / Status : {wish.post_status}</li>
        {/each}
    </ul>
    {:else}
    <p>찜한 게시글이 없습니다.</p>
    {/if}
</div>

<style>
  /* 여기에 스타일링 추가 */
</style>
