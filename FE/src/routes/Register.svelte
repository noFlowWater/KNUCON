<script>
  import request from "../lib/request";
  import { push } from 'svelte-spa-router';

  let name = '';
  let phoneNumber = '';
  let newId = '';
  let newPassword = '';
  let confirmPassword = '';

  let id_check_is_valid = null;

  function checkPasswordsMatch() {
    if (newPassword === confirmPassword) {
        console.log("Passwords match.");
        return true;
    } else {
        console.log("Passwords do not match.");
        return false;
    }
  }

  async function check_login_id(event) {
    event.preventDefault();
    let url = "/users/check";
    let params = {
      login_id: newId,
    };

    try {
        const response = await request('POST', url, params);
        if (response) {
            if (response.is_unique) {
                console.log("Login ID is unique");
                id_check_is_valid = true;
            } else {
                console.log("Login ID already exists");
                id_check_is_valid = false;
            }
        }
    } catch (err) {
        console.error('CheckLoginId Error:', err);
        console.error("Error detail:", JSON.parse(err.message));
    }
}


  async function handleRegistration(event) {
      event.preventDefault();
      if (!id_check_is_valid) {
        alert("Please check ID uniqueness before registering.");
        return;
      }
      if (!checkPasswordsMatch()) {
        alert("Passwords do not match.");
        return;
      }
      let url = "/users/register";
      let params = {
          name: name,
          login_id: newId,
          login_password: newPassword,
          phone_number: phoneNumber
      };
      try {
          const response = await request('POST', url, params);
          if (response) {
              console.log(response.message);
              push('/');
          }else{
            console.error('register request >>> response null');
          }
      } catch (err) {
          try {
              let errorDetails = JSON.parse(err.message);
              if (errorDetails && errorDetails.detail && errorDetails.detail.length > 0) {
                  let firstError = errorDetails.detail[0];
                  console.error("Error Type:", firstError.type);
                  console.error("Error Message:", firstError.msg);
              } else {
                  console.error("Error detail:", errorDetails);
              }
          } catch (jsonError) {
              // This catch block is for handling JSON parsing errors
              console.error("Error parsing JSON:", err.message);
          }
      }
  }
</script>

<style>
  .register-container {
    position: relative;
    width: 1280px;
    height: 832px;
    background: #FFFFFF;
    margin: 0 auto; /* 가운데 정렬 */
  }

  .input-field {
    position: absolute;
    width: 268px;
    height: 48px;
    background: #C3BEFF;
    border-radius: 10px;
    padding: 12px;
    font-size: 20px;
  }

  #name {
    left: 505px;
    top: 294px;
  }

  #phone-number {
    left: 505px;
    top: 350px;
  }

  #new-id {
    left: 505px;
    top: 406px;
  }

  #new-password {
    left: 505px;
    top: 462px;
  }

  #confirm-password {
    left: 504px;
    top: 518px;
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

  #button-id-check {
    width: 99px;
    height: 29px;
    left: 787px;
    top: 415px;
  }

  #button-register-complete {
    width: 118px;
    height: 33px;
    left: 581px;
    top: 579px;
  }

  /* 추가 스타일 생략... */
</style>

<div class="register-container">
  <input id="name" class="input-field" type="text" bind:value={name} placeholder="Name" />
  <input id="phone-number" class="input-field" type="text" bind:value={phoneNumber} placeholder="Phone Number" />
  <input id="new-id" class="input-field" type="text" bind:value={newId} placeholder="Your New ID" />
  <input id="new-password" class="input-field" type="password" bind:value={newPassword} on:input={checkPasswordsMatch} placeholder="Your New PW" />
  <input id="confirm-password" class="input-field" type="password" bind:value={confirmPassword} on:input={checkPasswordsMatch} placeholder="PW check" />
  <button id="button-id-check" class="button" on:click={check_login_id}>Check</button>
  <button id="button-register-complete" class="button" on:click={handleRegistration}>Register</button>
</div>
