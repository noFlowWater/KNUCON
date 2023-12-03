<script>
    import { onMount } from 'svelte';
    import { access_token } from "../../lib/store"; // access_token import
    import request from '../../lib/request.js';

    let rooms = [];
    let selectedRoomId;

    onMount(async () => {
        try {
            const headers = {
            'Authorization': `Bearer ${$access_token}`
            };
            const response = await request('get', '/rooms/list', {}, headers);
            rooms = response.rooms.filter(room => room.room_status === 0);
        } catch (error) {
            console.error('Error fetching rooms', error);
        }
    });

    async function handleSubmit(event) {
        event.preventDefault();
        const formData = new FormData(event.target);
        
        const formObject = {
            room_id: selectedRoomId,
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
            // Additional logic for handling successful submission
        } catch (error) {
            console.error('Error in submitting post', error);
            // Additional logic for handling errors
        }
    }
</script>

<div class="container mx-auto" style="margin-top: 80px;">
    <h2 class="text-center">포스트 작성(들어오세유)</h2>
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
                    <td>방</td>
                    <td> 
                        {#each rooms as room}
                        <div>
                            {room.room_nickname} - {room.address}
                        </div>
                        {/each}
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
</div>
