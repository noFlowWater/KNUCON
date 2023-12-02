<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request'; 
    import { access_token, is_login } from '../../lib/store'; 

    let rooms = [];
    let isLoading = true;
    let isError = false;

    onMount(async () => {
        if ($is_login) {
            try {
                // '/mypage/rooms' 엔드포인트로부터 방 목록 가져오기
                const response = await request('GET', '/mypage/rooms', {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {
                    rooms = JSON.parse(response);
                }
                isLoading = false;
            } catch (error) {
                console.error('Error fetching rooms:', error);
                isLoading = false;
                isError = true;
            }
        }
    });
</script>

<div class="page-container">
    <h1>내 방 목록</h1>
    {#if isLoading}
    <p>Loading rooms...</p>
    {:else if isError}
    <p>내 방을 불러오는 데 문제가 발생했습니다.</p>
    {:else if rooms.length > 0}
    <ul>
        {#each rooms as room}
        <li>{room.room_nickname} / {room.room_date} / Status: {room.room_status}</li>
        {/each}
    </ul>
    {:else}
    <p>등록된 내 방이 없습니다.</p>
    {/if}
</div>

<style>
  /* 여기에 스타일링 추가 */
</style>
