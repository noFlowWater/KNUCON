import { push } from 'svelte-spa-router';

export async function navigateTo(url) {
    push(url);
}

export function DateTimeFilter(dateTimeStr) {
    const date = new Date(dateTimeStr);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    
    return `${year}-${month}-${day} ${hours}:${minutes}`;
}

export function getPostStatusClass(status) {
    switch (status) {
        case 0:
            return 'post-status status-coming';
        case 1:
            return 'post-status status-going';
        case 2:
            return 'post-status status-ended';
        default:
            return 'post-status';
    }
}