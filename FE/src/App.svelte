<script>
  import Router, { location } from 'svelte-spa-router';
  import Notifications from 'svelte-notifications';
  import Navbar from './components/Navbar.svelte';
  import Home from './routes/Home.svelte';
  import Login from './routes/Login.svelte';
  import Register from './routes/Register.svelte';
  import Post from './routes/Post.svelte';
  // import PostLike from './routes/PostLike.svelte'; // PostLike 추가
  import Mypage from './routes/MyPage/MyPage.svelte';
  import MyRooms from './routes/MyPage/MyRooms.svelte';
  import MyPosts from './routes/MyPage/MyPosts.svelte';
  import WishList from './routes/MyPage/WishList.svelte';
  import PostDetail from './routes/PostDetail.svelte';
  import { checkRouteAccess } from './lib/routingGuard';
  import RoomRegister from './routes/RoomRegister.svelte';

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
    '/posts/:postId': PostDetail,
    '/room-register': RoomRegister
  };

  const routes = {
    ...publicRoutes,
    ...privateRoutes
  };

  // 현재 경로가 주어진 라우트 타입에 속하는지 확인하는 함수
  function private_access_check(path) {
    for (const route in privateRoutes) {
      if (route.includes(':')) { // 동적 라우트인 경우
        const baseRoute = route.split('/:')[0];
        if (path.startsWith(baseRoute)) {
          return true; 
        }
      } else if (route === path) { // 정적 라우트인 경우
        return true;
      }
    }
    return false; 
  }

  // 라우트 변경 시 로그인 및 경로 접근 확인
  $: location.subscribe(($location) => {
    checkRouteAccess($location, private_access_check);
  });
</script>

<Notifications>
  <Navbar />
  <Router {routes} />
</Notifications>
