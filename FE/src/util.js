import { push } from 'svelte-spa-router';

export async function navigateTo(url) {
    push(url);
}