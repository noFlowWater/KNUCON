<script>
  import Router, { location } from 'svelte-spa-router';
  import Navbar from './components/Navbar.svelte';
  import Home from './routes/Home.svelte';
  import Login from './routes/Login.svelte';
  import Register from './routes/Register.svelte';
  import Post from './routes/Post.svelte';
  import RoomRegister from './routes/RoomRegister.svelte';

  const routes = {
    '/': Login,
    '/register': Register,
    '/home': Home,
    '/post': Post,
    '/room-register': RoomRegister
  };
</script>

<!-- 현재 경로를 추적하고, 네비게이션 바를 조건부로 렌더링합니다. -->
{#if $location !== '/' && $location !== '/register'}
  <Navbar />
{/if}

<Router {routes} />