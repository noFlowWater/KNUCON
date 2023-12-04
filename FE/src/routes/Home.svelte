<script>
  import { onMount } from 'svelte';
  import { getNotificationsContext } from 'svelte-notifications';
  import { redirectedFromPublicRoute } from '../lib/store';

  const { addNotification } = getNotificationsContext();

  onMount(() => {
    const unsubscribe = redirectedFromPublicRoute.subscribe(value => {
      if (value) {
        addNotification({
          text: '이미 로그인 되어있습니다.',
          position: 'bottom-center',
          type: 'warning',
          removeAfter: 4000
        });
        redirectedFromPublicRoute.set(false);
      }
    });
    return () => {
      unsubscribe(); // 구독 해제
    };
  });
</script>

<div class="page-container">
  <h1>Welcome!</h1>

  <!-- 이미지와 중요 안내 내용을 포함하는 섹션 -->
  <div class="announcement-section">
    <img src="announcement.png" alt="Announcement" class="announcement-img" />
    <div class="announcement-text">
      <h2>중요 안내</h2>
      <p> 본 플랫폼을 통해 이어살기 연결이 완료된 후, 사용자는 법적 안정성을 확보하기 위해 해당 주거 공간의 소유주 혹은 관리자와의 공식적인 임대 계약을 체결해야 합니다.</p>
      <p>이는 이어살기가 법적 규정과 기준을 준수하며 진행될 수 있도록 보장하기 위함입니다.</p>
      <p>따라서, 이어살기를 시작하기 전에 새로운 임대 계약의 체결과 그에 따른 필요한 절차의 완료를 확인하시기 바랍니다.</p>
    </div>
  </div>
</div>

<style>
  .announcement-section {
    display: flex;
    align-items: center;
    margin-top: 20px;
    border: 1px solid #ccc; /* 경계선 추가 */
    padding: 15px;
    border-radius: 10px; /* 둥근 모서리 추가 */
    background-color: #f9f9f9; /* 배경색 추가 */
  }

  .announcement-img {
    width: 200px; /* 이미지 크기 */
    margin-right: 20px;
    border-radius: 5px; /* 이미지 둥근 모서리 추가 */
  }

  .announcement-text {
    font-size: 1em; /* 폰트 크기 조정 */
  }

  .announcement-text h2 {
    margin-top: 0;
    color: #333; /* 제목 색상 변경 */
  }

  .announcement-text p {
    margin: 0;
    text-align: justify; /* 문단 정렬 */
  }
</style>
