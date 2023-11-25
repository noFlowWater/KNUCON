<script>
  import { access_token, username, is_login } from "../lib/store"
  import request from "../lib/request";
  import { push } from 'svelte-spa-router';

  let error = {detail:[]}
  let login_id = '';
  let password = '';

  function login(event) {
      event.preventDefault()
      let url = "/users/login"
      let params = {
          login_id: login_id,
          login_password: password,
      }
      request('login', url, params, 
          (json) => {
              $access_token = json.token
              $username = json.user_name
              $is_login = true
              push("/")
          },
          (json_error) => {
              error = json_error
          }
      )
  }

  function goToRegister() {
    // 회원가입 페이지로 이동
    push('/register');
  }
</script>

<style>
  .login-container {
    position: relative;
    width: 1280px;
    height: 832px;
    background: #FFFFFF;
    margin: 0 auto; /* 가운데 정렬 */
  }

  .input-field {
    position: absolute;
    width: 270px;
    height: 48px;
    background: #FFBFBF;
    border-radius: 10px;
    padding: 12px;
    font-size: 20px;
  }

  #login-id {
    left: 450px;
    top: 345px;
  }

  #login-pw {
    left: 450px;
    top: 404px;
  }

  .button {
    position: absolute;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #D9D9D9;
    border: none;
    cursor: pointer;
  }

  #button-register {
    width: 81px;
    height: 25px;
    left: 461px;
    top: 462px;
  }

  /* 추가 버튼 스타일 생략... */

  #button-login {
    width: 107px;
    height: 107px;
    left: 730px;
    top: 345px;
    background: #FFBFBF;
    border-radius: 10px;
  }

  /* 추가 스타일 생략... */
</style>

<div class="login-container">
  <input id="login-id" class="input-field" type="text" bind:value={login_id} placeholder="ID" />
  <input id="login-pw" class="input-field" type="password" bind:value={password} placeholder="PW" />

  <button id="button-register" class="button" on:click={goToRegister}>Register</button>
  <button type="submit" class="btn btn-primary" on:click="{login}">LOGIN</button>
</div>