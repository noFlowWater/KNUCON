<script>
  import { navigateTo } from "../../util";
</script>
  
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="text-center">
      <h1>어떤 게시글을 작성하시겠어요?</h1>
      <button class="btn btn-warning btn-lg" on:click={() =>navigateTo('/posts/create1')}>들어갈래유</button>
      <button class="btn btn-success btn-lg" on:click={() =>navigateTo('/posts/create2')}>들어오세유</button>
    </div>
  </div>