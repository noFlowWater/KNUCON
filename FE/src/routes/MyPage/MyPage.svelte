<script>
  import { onMount } from 'svelte';
  import request from '../../lib/request';
  import { access_token, is_login } from '../../lib/store';
  import { link } from 'svelte-spa-router';

  let userProfile = {};
  let isLoading = true; // 데이터 로딩 상태를 추적하는 변수

  onMount(async () => {
    if($is_login){
      try {
        const response = await request('GET', '/mypage/profile', {}, {
          'Authorization': `Bearer ${$access_token}` // 사용자 토큰 사용
        });
        console.log('Server Response:', response); // 서버 응답 로깅
        userProfile = JSON.parse(response);
        isLoading = false; // 데이터 로딩 완료
      } catch (error) {
        console.error('Error fetching user profile:', error);
      }
    }
  });
  
  
</script>

<div class="page-container">
  <h1>My Page</h1>
  {#if isLoading}
    <p>Loading profile...</p>
  {:else}
    <div>
      <p><strong>User ID:</strong> {userProfile.user_id}</p>
      <p><strong>Name:</strong> {userProfile.name}</p>
      <p><strong>Login ID:</strong> {userProfile.login_id}</p>
      <p><strong>Phone Number:</strong> {userProfile.phone_number}</p>
    </div>
  {/if}
  <!-- 기능 버튼 -->
  <div class="buttons">
    <a use:link href="/mypage/rooms" class="button">내 방 조회</a>
    <a use:link href="/mypage/posts" class="button">내 글 조회</a>
    <a use:link href="/mypage/wishlist" class="button">찜 목록 보기</a>
    <a use:link href="/mypage/withdraw" class="button">탈퇴</a>
  </div>
</div>


<style>
  .button {
    display: inline-block;
    margin: 10px;
    padding: 10px;
    text-decoration: none; /* 링크 밑줄 제거 */
    background-color: #f0f0f0; /* 버튼 배경색 */
    color: black; /* 텍스트 색상 */
    border-radius: 5px; /* 둥근 모서리 */
    /* 추가적인 버튼 스타일링 */
  }

  .button:hover {
    background-color: #e0e0e0; /* 호버 효과 */
  }
</style>