<script>
  let name = '';
  let phoneNumber = '';
  let newId = '';
  let newPassword = '';
  let confirmPassword = '';

  function handleRegistration() {
    // 회원가입 로직
    console.log("Registering with", name, phoneNumber, newId, newPassword, confirmPassword);
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
  <input id="new-password" class="input-field" type="password" bind:value={newPassword} placeholder="Your New PW" />
  <input id="confirm-password" class="input-field" type="password" bind:value={confirmPassword} placeholder="PW check" />

  <button id="button-id-check" class="button">Check</button>
  <button id="button-register-complete" class="button" on:click={handleRegistration}>Register</button>
</div>
