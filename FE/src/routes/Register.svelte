<script>
  import request from "../lib/request";
  import { push } from 'svelte-spa-router';
  import { onMount, onDestroy } from 'svelte';
  import { getNotificationsContext } from 'svelte-notifications';

  const { addNotification } = getNotificationsContext();

  let name = '';
  let phoneNumber = '';
  let newId = '';
  let newPassword = '';
  let confirmPassword = '';
  let id_check_is_valid = null;
  let passwordsDoNotMatch = false; 
  let isPhoneNumberValid = false;
  // 페이지가 로드될 때 실행되는 함수
  onMount(() => {
    // body 요소에 스타일을 동적으로 추가
    document.body.style.background = 'url(/background.png) no-repeat center';
    document.body.style.backgroundSize = 'cover';
    document.body.style.fontFamily = 'sans-serif';
  });

  // 페이지가 언마운트될 때 실행되는 함수
  onDestroy(() => {
    // body 요소의 스타일을 초기 상태로 돌려놓음
    document.body.style.background = '';
    document.body.style.backgroundSize = '';
    document.body.style.fontFamily = '';
  });

  function checkPasswordsMatch() {
    passwordsDoNotMatch = newPassword !== confirmPassword;
    if (newPassword === confirmPassword) {
        console.log("Passwords match.");
        return true;
    } else {
        console.log("Passwords do not match.");
        return false;
    }
  }
  function validatePhoneNumber() {
    const phoneRegex = /^010\d{8}$/;
    isPhoneNumberValid = phoneRegex.test(phoneNumber);
  }
  function verifyFieldNotEmpty(fieldValue, fieldName) {
    if (!fieldValue) {
      console.error(`${fieldName} is required`);
      addNotification({
        text: `${fieldName} is required`,
        position: 'bottom-center',
        type: 'warning',
        removeAfter: 4000
      });
      return false;
    }
    return true;
  }
  function verifyAllFieldsFilled() {
    return verifyFieldNotEmpty(name, 'Name') &&
          verifyFieldNotEmpty(phoneNumber, 'Phone Number') &&
          verifyFieldNotEmpty(newId, 'New ID') &&
          verifyFieldNotEmpty(newPassword, 'New Password') &&
          verifyFieldNotEmpty(confirmPassword, 'Confirm Password');
  }

  function verifyNewIdFieldFilled() {
    return verifyFieldNotEmpty(newId, 'New ID');
  }

  async function check_login_id(event) {
    if (event) {
        event.preventDefault();
    }
    // Validate form fields
    if (!verifyNewIdFieldFilled()) {
      return;
    }
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
      // Validate form fields
      if (!verifyAllFieldsFilled()) {
        return;
      }
      if(!isPhoneNumberValid){
        addNotification({
          text: 'Please check Phone Number. ex) 01012345678',
          position: 'bottom-center',
          type: 'warning',
          removeAfter: 4000
        });
        return;
      }
      await check_login_id();
      if (!id_check_is_valid) {
        addNotification({
          text: 'Please check ID uniqueness before registering.',
          position: 'bottom-center',
          type: 'warning',
          removeAfter: 4000
        });
        return;
      }
      if (!checkPasswordsMatch()) {
        addNotification({
          text: 'Passwords do not match.',
          position: 'bottom-center',
          type: 'warning',
          removeAfter: 4000
        });
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
              addNotification({
                text: '회원 등록이 완료되었습니다!',
                position: 'bottom-center',
                type: 'success',
                removeAfter: 4000
              });
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
                  addNotification({
                    text: firstError.msg,
                    position: 'bottom-center',
                    type: 'error',
                    removeAfter: 4000
                  });
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
  .register-wrapper {
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

/* Style for valid/invalid input */
.form .input-group input.valid {
  border-bottom: 2px solid rgb(0, 220, 0); /* Green color for valid input */
  box-shadow: 0 1px 0 rgb(0, 220, 0); /* Adding a subtle shadow for a more distinct effect */
}

.form .input-group input.invalid {
  border-bottom: 2px solid rgb(255, 111, 111); /* Red color for invalid input */
  box-shadow: 0 1px 0 rgb(255, 111, 111); /* Adding a subtle shadow for a more distinct effect */
}

.button-container {
    display: flex;
    justify-content: space-between; /* 버튼 사이의 간격을 최대화하여 나란히 정렬 */
    margin-top: 20px; /* 버튼과 다른 내용 사이의 간격 조정 */
  }


.button {
  width: 100%;
  max-width: 380px; /* 최대 너비 설정 */
  padding: 10px 20px;
  margin: 10px 0; /* 상하 간격 */
  background: rgb(255, 47, 47);
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  border-radius: 5px;
  border: none;
  cursor: pointer;
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
.check-btn {
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
.form .input-group .validation-message {
  font-size: 1.2rem; /* Adjust size as needed */
  position: absolute; /* Positioning relative to the input group */
  right: 0; /* Align to the right */
  top: 10px; /* Vertical alignment - adjust as needed */
}

.form .input-group .valid-message {
  color: rgb(0, 220, 0); /* Green color for valid message */
}

.form .input-group .invalid-message {
  color: rgb(255, 111, 111); /* Red color for invalid message */
}


  /* 추가 스타일 생략... */
</style>

<div class="register-wrapper">
  <form action="" class="form">
    <img src="/knu_logo.svg" alt="">
    <h2>Register</h2>
    <div class="input-group">
      <input id="name" class="input-field" type="text" required bind:value={name} />
      <label for="name">Your Name</label>
    </div>
    <div class="input-group">
      <input 
        id="phone-number" 
        class="input-field {phoneNumber.length > 0 && (isPhoneNumberValid ? 'valid' : 'invalid')}" 
        type="text" 
        required
        bind:value={phoneNumber} 
        on:input={validatePhoneNumber}  />
      <label for="phone-number">Your phoneNumber</label>
    </div>
    <div class="input-group">
      <input id="new-id" name="new-id" class="input-field {id_check_is_valid === true ? 'valid' : id_check_is_valid === false ? 'invalid' : ''}" 
            type="text" required bind:value={newId} />
      <label for="new-id">Your New ID</label>
      {#if id_check_is_valid === true}
        <span class="validation-message valid-message">available! :)</span>
      {:else if id_check_is_valid === false}
        <span class="validation-message invalid-message">duplicate :(</span>
      {/if}
    </div>
    <div class="input-group">
      <input id="new-password" class="input-field" type="password" required bind:value={newPassword} on:input={checkPasswordsMatch} placeholder="Your New PW" />
      <label for="new-password">Your New Password</label>
    </div>
    <div class="input-group">
      <input 
        id="confirm-password" 
        class="input-field {confirmPassword.length > 0 && (passwordsDoNotMatch ? 'invalid' : 'valid')}" 
        type="password" 
        required
        bind:value={confirmPassword} 
        on:input={checkPasswordsMatch} />
        <label for="confirm-password">Password check</label>
        {#if confirmPassword.length > 0 && !passwordsDoNotMatch}
          <span class="validation-message valid-message">Matched!</span>
        {:else if confirmPassword.length > 0 && passwordsDoNotMatch}
          <span class="validation-message invalid-message">Not Matched!</span>
        {/if}
    </div>
    <div class="button-container">
      <button id="button-id-check" class="check-btn" type="button" on:click={check_login_id}>ID Check</button>
      <input type="submit" value="Register" id="button-register-complete" class="submit-btn" on:click={handleRegistration}/>
    </div>
  </form>
</div>
