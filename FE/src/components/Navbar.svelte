<script>
  import { link } from 'svelte-spa-router';
  import { access_token, username, is_login } from "../lib/store"
</script>

<nav class="navbar fixed-top navbar-expand-sm navbar-light">
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
      {#if $is_login }
          <li class="nav-item">
              <a use:link href="/" class="nav-link" on:click={() => {
                  $access_token = ''
                  $username = ''
                  $is_login = false
              }}>로그아웃 ({$username})</a>
          </li>
      {:else}
          <li class="nav-item">
              <a use:link href="/register" class="nav-link" >회원가입</a>
          </li>
          <li class="nav-item">
              <a use:link href="/" class="nav-link" >로그인</a>
          </li>
      {/if}
    </ul>
  </div>
</nav>

<style>
  .navbar {
    background-color: #4A4E69;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  }

  .navbar-brand {
    background-color: #ff5f5f; /* Bright red background */
    color: #fff; /* White text */
    padding: 5px 10px; /* Padding inside the rectangle */
    border-radius: 15px; /* Rounded corners */
    text-decoration: none; /* Remove underline from links */
    transition: background-color 0.3s ease-in-out;
    margin-left: 20px; /* Space from the left edge */
  }

  .navbar-brand:hover {
    background-color: #e45555; /* Slightly darker red on hover */
  }

  .navbar-nav .nav-item .nav-link {
    color: #9A8C98;
    transition: color 0.3s ease-in-out;
  }

  .navbar-nav .nav-item .nav-link:hover {
    color: #F2E9E4;
  }

  .nav-item {
    margin-left: 20px;
  }

  @media (max-width: 768px) {
    .navbar-collapse {
      background-color: #4A4E69;
    }

    .navbar-nav .nav-item {
      margin-left: 0;
      margin-bottom: 10px;
    }

    .navbar-brand {
      margin-left: 10px; /* Adjust margin for smaller screens */
    }
  }
</style>

