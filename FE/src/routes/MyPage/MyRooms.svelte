<script>
    import { onMount } from 'svelte';
    import request from '../../lib/request'; 
    import { access_token, is_login } from '../../lib/store'; 

    let rooms = [];
    let isLoading = true;
    let isError = false;

    onMount(async () => {
        if ($is_login) {
            try {
                // '/mypage/rooms' 엔드포인트로부터 방 목록 가져오기
                const response = await request('GET', '/mypage/rooms', {}, {
                    'Authorization': `Bearer ${$access_token}`
                });
                if (response) {
                    rooms = JSON.parse(response);
                }
                isLoading = false;
            } catch (error) {
                console.error('Error fetching rooms:', error);
                isLoading = false;
                isError = true;
            }
        }
    });
</script>

<div class="page-container">
    {#if isLoading}
    <p>Loading rooms...</p>
    {:else if isError}
    <p>내 방을 불러오는 데 문제가 발생했습니다.</p>
    {:else if rooms.length > 0}
    <ul>
        {#each rooms as room}
            <div class="room-details">
                <h3 class="room-info-head">
                    Room Information of <span class="room-name">{room.room_nickname}</span> /
                    <span class={room.room_status == 0 ? 'room-status incomplete' : 'room-status complete'}>
                        {room.room_status == 0 ? '연결 미완료' : '연결 완료'}
                    </span>
                </h3>
                <p><strong>Address:</strong> {room.address}</p>
                <p><strong>Area:</strong> {room.area}</p>
                <p><strong>Deposit:</strong> {room.deposit}</p>
                <p><strong>Price:</strong> {room.price}</p>
                <p><strong>Room Type:</strong> 
                    {#if room.room_type === 1}
                        원룸
                    {:else if room.room_type === 2}
                        투룸
                    {:else if room.room_type === 3}
                        쓰리룸 이상
                    {/if}
                </p>
                <p><strong>Direction:</strong> {room.direction}</p>
                <p><strong>Floor:</strong> {room.floor}</p>
                <p><strong>Gate:</strong> 
                    {#if room.gate === 0}
                        북문/농장문
                    {:else if room.gate === 1}
                        서문/수영장문
                    {:else if room.gate === 2}
                        솔로문/조은문
                    {:else if room.gate === 3}
                        쪽문/정문/수의대문
                    {:else if room.gate === 4}
                        테크노문/나리문/동문
                    {/if}
                </p>
                <div class="room-options">
                    <p><strong>Contract Status:</strong> 
                        {#if room.is_contract === 0}
                            월세
                        {:else if room.is_contract === 1}
                            전세
                        {/if}
                    </p>
                    <p><strong>Rent Aid:</strong> <span class="status-indicator {room.rent_aid ? 'yes' : 'no'}"></span></p>
                    <p><strong>Preview Available:</strong> <span class="status-indicator {room.preview ? 'yes' : 'no'}"></span></p>
                    <p><strong>Extension Option:</strong> <span class="status-indicator {room.extension ? 'yes' : 'no'}"></span></p>
                    <p><strong>Electricity Bill Included:</strong> <span class="status-indicator {room.elec_bill ? 'yes' : 'no'}"></span></p>
                    <p><strong>Water Bill Included:</strong> <span class="status-indicator {room.water_bill ? 'yes' : 'no'}"></span></p>
                    <p><strong>Gas Bill Included:</strong> <span class="status-indicator {room.gas_bill ? 'yes' : 'no'}"></span></p>
                    <p><strong>Kitchen Separated:</strong> <span class="status-indicator {room.kit_sep ? 'yes' : 'no'}"></span></p>
                    <p><strong>Stove Type:</strong> 
                        {#if room.stove_type === 0}
                            가스레인지
                        {:else if room.stove_type === 1}
                            인덕션
                        {/if}
                    </p>
                    <p><strong>Fridge Included:</strong> <span class="status-indicator {room.fridge ? 'yes' : 'no'}"></span></p>
                    <p><strong>Air Conditioning:</strong> <span class="status-indicator {room.ac ? 'yes' : 'no'}"></span></p>
                    <p><strong>Microwave Included:</strong> <span class="status-indicator {room.mw ? 'yes' : 'no'}"></span></p>
                    <p><strong>Balcony Available:</strong> <span class="status-indicator {room.balcony ? 'yes' : 'no'}"></span></p>
                    <p><strong>Dryer Included:</strong> <span class="status-indicator {room.dryer ? 'yes' : 'no'}"></span></p>
                </div>
                <!-- 'PICTURE' 필드는 이미지 처리가 필요하므로 별도로 처리 -->
                <!-- <img src={postDetails.PICTURE} alt="Room Image" /> -->
            </div>
        {/each}
    </ul>
    {:else}
    <p>등록된 내 방이 없습니다.</p>
    {/if}
</div>

<style>
    .room-info-head {
        font-size: 1.2em; /* Adjust the font size */
        color: #333; /* Dark text color for readability */
        margin: 10px 0; /* Margin for spacing */
        font-weight: normal; /* Normal font weight */
    }

    .room-name {
        color: #007BFF; /* Highlight color for the room name */
        font-weight: bold; /* Bold font weight for emphasis */
    }
    .room-status.incomplete {
        color: #28A745; /* Green color for incomplete status */
        font-weight: bold; /* Bold font weight for emphasis */
    }
    .room-status.complete {
        color: #DC3545; /* Red color for complete status */
        font-weight: bold; /* Bold font weight for emphasis */
    }
    .room-details {
        background-color: #f9f9f9;
        padding: 15px;
        margin-top: 20px;
        border-radius: 5px;
    }
    .room-details h3 {
        text-align: center;
        color: #333;
    }
    .status-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        margin-left: 5px;
    }

    .status-indicator.yes::after {
        content: '';
        display: block;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: green;
    }

    .status-indicator.no::after {
        content: '';
        display: block;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background-color: red;
    }
</style>
