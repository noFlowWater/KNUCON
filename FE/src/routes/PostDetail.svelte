<!-- PostDetail.svelte -->
<script>
    import { onMount } from 'svelte';
    import request from '../lib/request'; 
    import { access_token, is_login } from '../lib/store'; 
    export let params = {}

    let postDetails = {};
    let isLoading = true;
    let isError = false;

    onMount(async () => {
        console.log("postId: "+params.postId)
        if($is_login) {
            try {
                const response = await request('GET', `/posts/${params.postId}`, {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {postDetails = JSON.parse(response);}
            } catch (error) {
                console.error('Error fetching post details:', error);
                isError = true;
            } finally {
                isLoading = false;
            }
        }
    });
</script>

<div class="page-container">
    <h1>Post Detail</h1>
    {#if isLoading}
        <p>Loading...</p>
    {:else if isError}
        <p>Error loading post details.</p>
    {:else}
        <p>POST_ID : {postDetails.POST_ID}</p>
        <p>RID : {postDetails.RID}</p>
        <p>UID : {postDetails.UID}</p>
        <p>POST_STATUS : {postDetails.POST_STATUS}</p>
        <p>POST_DATE : {postDetails.POST_DATE}</p>
        <p>POST_VIEW_COUNT : {postDetails.POST_VIEW_COUNT}</p>
        <p>POST_CONTENT : {postDetails.POST_CONTENT}</p>
        <p>WISH_COUNT : {postDetails.WISH_COUNT}</p>

    {/if}
</div>