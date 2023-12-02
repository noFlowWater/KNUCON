// src/lib/routingGuard.js
import { get } from 'svelte/store';
import { is_login, redirectedFromPublicRoute, redirectedToLogin } from './store';
import { push } from 'svelte-spa-router';
/**
 * 현재 경로를 확인하여 라우터 엑세스 유효성 여부를 체크하는 함수
 * @param {string} currentPath - 현재 브라우저의 경로
 * @param {Function} isPrivateRoute - 주어진 경로가 private 경로인지 확인하는 함수
 */
export function checkRouteAccess(currentPath, private_access_check) {
    const isPrivate = private_access_check(currentPath);
    const loggedIn = get(is_login);
    
    if (!isPrivate && loggedIn) {
        redirectedFromPublicRoute.set(true);  // 리다이렉트되었음을 표시
        push('/home');
    }
    if (isPrivate && !loggedIn) {
        redirectedToLogin.set(true);  // 리다이렉트되었음을 표시
        push('/');
    }
}