// src/lib/routingGuard.js
import { get } from 'svelte/store';
import { is_login, redirectedFromPublicRoute, redirectedToLogin } from './store';
import { push } from 'svelte-spa-router';
/**
 * 현재 경로와 private 경로를 확인하여 로그인 여부를 체크하는 함수
 * @param {string} currentPath - 현재 브라우저의 경로
 * @param {Function} isPrivateRoute - 주어진 경로가 private 경로인지 확인하는 함수
 */
export function checkLogin(currentPath, isPrivateRoute) {
    const loggedIn = get(is_login);

    // 주어진 경로가 private 경로인지 확인
    const isPrivate = isPrivateRoute(currentPath);

    // 비로그인 상태에서 private 경로에 접근 시 로그인 페이지로 리다이렉트
    if (isPrivate && !loggedIn) {
        redirectedToLogin.set(true); // 리다이렉트되었음을 표시
        push('/');
    }
}
export function checkPublicRouteAccess(currentPath, isPublicRoute) {
    const isPublic = isPublicRoute(currentPath);
    const loggedIn = get(is_login);
    if (isPublic && loggedIn) {
        redirectedFromPublicRoute.set(true);  // 리다이렉트되었음을 표시
        push('/home');
    }
}