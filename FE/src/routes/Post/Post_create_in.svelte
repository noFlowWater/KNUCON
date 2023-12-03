<script>
    import { onMount } from 'svelte';
    import { access_token, is_login } from '../../lib/store'; 
    import request from '../../lib/request.js';
    import { navigateTo } from "../../util";
    import { getNotificationsContext } from 'svelte-notifications';
    import { pop } from 'svelte-spa-router';
    
    const { addNotification } = getNotificationsContext();

    let stat = '';
    let isLoading = true;
    let isError = false;
    
    onMount(async () => {
        if($is_login){
            try {
                const response = await request('GET', '/posts/checkstatus1', {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {
                    stat = JSON.parse(response);
                    if(stat.status === "exists"){
                        addNotification({
                            text: '이미 들어갈레유 글을 작성했습니다.',
                            position: 'bottom-center',
                            type: 'warning',
                            removeAfter: 4000
                        });
                        pop();
                    }
                }
            } catch (error) {
                console.error('Error fetching posts:', error);
                isError = true;
            } finally {
                isLoading = false;
            }
        }
    });

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        
        const formObject = {
            room_id: null,
            post_status: 1,
            post_title: formData.get('post_title'),
            post_content: formData.get('post_content')
        };

        console.log(formObject);
        try {
            const headers = {
            'Authorization': `Bearer ${$access_token}`
            };
            const response = await request('post', '/posts/create', formObject, headers);
            console.log('Post submission successful', response);
            addNotification({
                text: '글 작성 완료!',
                position: 'bottom-center',
                type: 'success',
                removeAfter: 4000
            });
            navigateTo('/home')
        } catch (error) {
            console.error('Error in submitting post', error);
            // Additional logic for handling errors
        }
    }
</script>

<div class="container mx-auto" style="margin-top: 80px;">
    <h2 class="text-center">포스트 작성(들어갈래유)</h2>
    {#if isLoading}
    <p>Loading...</p>
    {:else if isError}
    <p>포스트 작성 페이지를 불러오는 데 문제가 발생했습니다.</p>
    {:else}
    <form on:submit={handleSubmit}>
        <table class="table table-hover table-sm">
            <tbody>
                <tr>
                    <td>제목</td>
                    <td>
                        <input type="text" class="form-control" name="post_title" placeholder="Enter title">
                    </td>
                </tr>
                <tr>
                    <td>내용</td>
                    <td>
                        <textarea class="form-control" name="post_content" placeholder="Enter Content" rows="6" style="resize: none;"></textarea>
                    </td>
                </tr>
            </tbody>
        </table>
        <div class="text-center">
            <button type="reset" class="btn btn-secondary">등록 취소</button>
            <button type="submit" class="btn btn-primary">글 등록하기</button>
        </div>
    </form>
    {/if}
</div>
