<script>
  import request from '../../lib/request.js';
  import { onMount } from 'svelte';

  const url1 = "/posts";

  let posts = [];
  let postContent = '';
  let selectedPostId = null;
  let username = 'your_username'; // 사용자 이름
  let password = 'your_password'; // 비밀번호

  onMount(async () => {
    await fetchPosts();
  });

  async function fetchPosts() {
    try {
      const response = await request('GET', url1, {}, {}, username, password);
      posts = response.map(postString => parsePostData(postString));
    } catch (error) {
      console.error('Error fetching posts', error);
    }
  }

  async function createPost() {
    try {
      await request('POST', url1, { content: postContent }, {}, username, password);
      postContent = '';
      await fetchPosts();
    } catch (error) {
      console.error('Error creating post', error);
    }
  }

  async function deletePost(postId) {
    try {
      await request('DELETE', `/posts/${postId}`, {}, {}, username, password);
      await fetchPosts();
    } catch (error) {
      console.error('Error deleting post', error);
    }
  }
  function parsePostData(postDataString) {
    const dataObject = {};
    const dataPairs = postDataString.split(',').map(pair => pair.trim());
    
    dataPairs.forEach(pair => {
      const [key, value] = pair.split('=').map(part => part.trim());
      dataObject[key] = value;
    });

    return dataObject;
  }
</script>

<div class="page-container">
  <!-- 게시글 작성 폼 -->
  <form on:submit|preventDefault={createPost}>
    <textarea bind:value={postContent} placeholder="Write your post here..."></textarea>
    <button type="submit">Create Post</button>
  </form>

  <!-- 게시글 목록 -->
  {#if posts.length > 0}
    <ul>
      {#each posts as post (post.post_id)}
        <li>
          <strong>{post.post_title}</strong>
          <p>{post.post_content}</p>
          <button on:click={() => deletePost(post.post_id)}>Delete</button>
        </li>
      {/each}
    </ul>
  {:else}
    <p>No posts to display.</p>
  {/if}
</div>