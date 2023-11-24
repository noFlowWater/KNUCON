<script>
  import { link } from 'svelte-spa-router';
</script>

<nav class="navbar fixed-top navbar-expand-sm navbar-light bg-light">
  <a use:link href="/home" class="navbar-brand">KNUCON</a>
  <div class="collapse navbar-collapse">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item">
        <a use:link href="/post" class="nav-link">Post</a>
      </li>
      <li class="nav-item">
        <a use:link href="/room-register" class="nav-link">Room Register</a>
      </li>
      <li class="nav-item">
        <a use:link href="/chatroom" class="nav-link">Chatroom</a>
      </li>
      <li class="nav-item">
        <a use:link href="/mypage" class="nav-link">MyPage</a>
      </li>
    </ul>
  </div>
</nav>

<style>
  /* 여기에 네비게이션 바 스타일을 정의합니다. */
</style>
