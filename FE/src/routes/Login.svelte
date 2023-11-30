<script>
  import { access_token, username, is_login, redirectedToLogin } from "../lib/store"
  import request from "../lib/request";
  import { push } from 'svelte-spa-router';
  import { getNotificationsContext } from 'svelte-notifications';
  import { onMount, onDestroy } from 'svelte';

  const { addNotification } = getNotificationsContext();

  // 페이지가 로드될 때 실행되는 함수
  onMount(() => {
    // body 요소에 스타일을 동적으로 추가
    document.body.style.background = 'url(/background.png) no-repeat center';
    document.body.style.backgroundSize = 'cover';
    document.body.style.fontFamily = 'sans-serif';
    const unsubscribe = redirectedToLogin.subscribe(value => {
      if (value) {
        addNotification({
          text: '로그인이 필요한 페이지입니다. 로그인 해주세요.',
          position: 'bottom-center',
          type: 'warning',
          removeAfter: 4000
        });
        redirectedToLogin.set(false); // 상태 초기화
      }
    });
    return () => {
      unsubscribe(); // 구독 해제
    };
  });

  // 페이지가 언마운트될 때 실행되는 함수
  onDestroy(() => {
    // body 요소의 스타일을 초기 상태로 돌려놓음
    document.body.style.background = '';
    document.body.style.backgroundSize = '';
    document.body.style.fontFamily = '';
  });

  let error = {detail:[]}
  let login_id = '';
  let password = '';

  async function login(event) {
      event.preventDefault();

      // 입력값 검증
      if (!login_id || !password) {
        addNotification({
          text: '로그인 아이디와 비밀번호를 입력해주세요.',
          position: 'bottom-center',
          type: 'error',
          removeAfter: 4000
        });
        return; // 함수 실행 종료
      }
      
      let url = "/users/login";
      let params = {
          login_id: login_id,
          login_password: password,
      };

      try {
          const response = await request('login', url, params);
            if (response) {
              // Check if the response is an object (successful login)
              if (typeof response === 'object' && response.token) {
                  $access_token = response.token;
                  $username = response.user_name;
                  $is_login = true;
                  // 사용자 이름을 포함한 환영 메시지
                  const welcomeMessage = `${$username}님 환영합니다!`;

                  console.log('Access Token:', $access_token);
                  console.log('Username:', $username);
                  console.log('Is Logged In:', $is_login);

                  addNotification({
                    text: welcomeMessage,
                    position: 'bottom-center',
                    type: 'success',
                    removeAfter: 4000
                  });
                  
                  push('/home');
              } else {
                  // If the response is not an object, log the error message
                  console.error('Login Failed:', response);
                  addNotification({
                      text: response,
                      position: 'bottom-center',
                      type: 'error',
                      removeAfter: 4000
                  });
              }
            }
      } catch (err) {
          console.error('Login Error:', err);
          error = JSON.parse(err.message);
          addNotification({
              text: '로그인 오류: ' + err.message,
              position: 'bottom-center',
              type: 'error',
              removeAfter: 4000
          });
      }
  }

  function goToRegister() {
    // 회원가입 페이지로 이동
    push('/register');
  }
</script>

<style>
  .login-wrapper {
    height: 100vh;
    width: 100vw;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .form {
    margin: auto;
    margin-left: 15%; 
    position: relative;
    width: 100%;
    max-width: 380px;
    padding: 80px 40px 40px;
    background: rgba(0, 0, 0, 0.5); /* 불투명도를 1로 설정 */
    border-radius: 10px;
    color: #fff;
    box-shadow: 0 15px 25px rgba(0,0,0,0.5);
  }
  .form img {
    position: absolute;
    top: -50px;
    left: calc(50% - 50px);
    width: 100px;
    background: rgba(255,255,255, 0.8);
    border-radius: 50%;
  }
  .form h2 {
    text-align: center;
    letter-spacing: 1px;
    margin-bottom: 2rem;
    color: rgb(255, 47, 47);
  }
  .form .input-group {
    position: relative;
  }
  .form .input-group input {
    width: 100%;
    padding: 10px 0;
    font-size: 1rem;
    letter-spacing: 1px;
    margin-bottom: 30px;
    border: none;
    border-bottom: 1px solid #fff;
    outline: none;
    background-color: transparent;
    color: inherit;
  }
  .form .input-group label {
    position: absolute;
    top: 0;
    left: 0;
    padding: 10px 0;
    font-size: 1rem;
    pointer-events: none;
    transition: .3s ease-out;
  }
  .form .input-group input:focus + label,
  .form .input-group input:valid + label {
    transform: translateY(-18px);
    color: rgb(255, 47, 47);
    font-size: .8rem;
  }
  .button-container {
    display: flex;
    justify-content: space-between; /* 버튼 사이의 간격을 최대화하여 나란히 정렬 */
    margin-top: 20px; /* 버튼과 다른 내용 사이의 간격 조정 */
  }
  .submit-btn {
    display: block;
    margin-left: auto;
    border: none;
    outline: none;
    background: rgb(255, 47, 47);
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  .register-btn {
    border: none;
    outline: none;
    background: rgba(255, 255, 255, 0.3);
    font-size: 1rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }

</style>

<div class="login-wrapper">
  <form action="" class="form">
    <img src="/knu_logo.svg" alt="">
    <h2>Login</h2>
    <div class="input-group">
      <input type="text" name="loginUser" id="loginUser" autocomplete="off" required bind:value={login_id}>
      <label for="loginUser">User Name</label>
    </div>
    <div class="input-group">
      <input type="password" name="loginPassword" id="loginPassword" required bind:value={password}>
      <label for="loginPassword">Password</label>
    </div>
    <div class="button-container">
      <button class="register-btn" type="button" on:click|preventDefault={goToRegister}>Register</button>
      <input type="submit" value="Login" class="submit-btn" on:click|preventDefault={login}>
      
    </div>
  </form>
</div>