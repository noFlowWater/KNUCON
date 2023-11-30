<script>
  import Router, { location } from 'svelte-spa-router';
  import Notifications from 'svelte-notifications';
  import Navbar from './components/Navbar.svelte';
  import Home from './routes/Home.svelte';
  import Login from './routes/Login.svelte';
  import Register from './routes/Register.svelte';
  import Post from './routes/Post.svelte';
  import Mypage from './routes/MyPage/MyPage.svelte';
  import MyRooms from './routes/MyPage/MyRooms.svelte';
  import MyPosts from './routes/MyPage/MyPosts.svelte';
  import WishList from './routes/MyPage/WishList.svelte';
  import { checkLogin, checkPublicRouteAccess } from './lib/routingGuard';

  // 로그인이 필요하지 않은 기본 경로
  const publicRoutes = {
    '/': Login,
    '/register': Register,
  };

  // 로그인이 필요한 경로
  const privateRoutes = {
    '/home': Home,
    '/post': Post,
    '/mypage': Mypage,
    '/mypage/rooms': MyRooms,
    '/mypage/posts': MyPosts,
    '/mypage/wishlist': WishList,
  };

  const routes = {
    ...publicRoutes,
    ...privateRoutes
  };

  // 현재 경로가 공개 경로인지 확인하는 함수
  function isPublicRoute(path) {
    return Object.keys(publicRoutes).includes(path);
  }

  // 현재 경로가 비공개 경로인지 확인하는 함수
  function isPrivateRoute(path) {
    return Object.keys(privateRoutes).includes(path);
  }

  // 라우트 변경 시 로그인 및 경로 접근 확인
  $: location.subscribe(($location) => {
    checkPublicRouteAccess($location, isPublicRoute);
    checkLogin($location, isPrivateRoute);
  });
</script>

<Notifications>
  <Navbar />
  <Router {routes} />
</Notifications>
