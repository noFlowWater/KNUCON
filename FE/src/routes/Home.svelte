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
  <!-- 여기에 페이지에 해당하는 내용 랜더링 -->
</div>
