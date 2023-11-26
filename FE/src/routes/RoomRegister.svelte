<script>
    import { onMount } from 'svelte';
    import { push } from 'svelte-spa-router';
    import request from "../lib/request";

    let roomDetails = {
        room_nickname: '',
        address: '',
        area: 0.0,
        deposit: 0,
        price: 0,
        room_type: '', // 라디오 버튼을 위한 단일 값
        direction: { east: false, west: false, south: false, north: false },
        floor: '', // 라디오 버튼을 위한 단일 값
        gate: '', // 라디오 버튼을 위한 단일 값
        is_contract: '', // 라디오 버튼을 위한 단일 값
        option: {
            rent_aid: false,
            preview: false,
            extension: false,
            elec_bill: false,
            water_bill: false,
            gas_bill: false,
            kit_sep: false,
            stove_type: false,
            fridge: false,
            ac: false,
            mw: false,
            balcony: false,
            dryer: false
        }
    };

    let hasExistingRoom = false; // This will hold the status of existing room check

    // This function will be called when the component is first created
    onMount(async () => {
        try {
            const user_id = "user-id-from-context-or-storage"; // Get the current user's ID
            const response = await request('get', '/rooms/check', { params: { user_id } });
            hasExistingRoom = response.data; // Assuming the endpoint returns a boolean
            if (hasExistingRoom) {
                alert('기존에 등록된 방이 있습니다.');
            }
        } catch (err) {
            console.error('Error checking existing room:', err);
        }
    });
    
    let directionSelections = 0;
    const maxDirectionSelections = 2;

    function handleDirectionChange(event) {
        const currentDirection = event.target.id; // 현재 변경된 체크박스의 ID (예: "east", "west" 등)
        roomDetails.direction[currentDirection] = event.target.checked; // 현재 방향의 선택 상태를 갱신

        // 현재 체크된 방향 개수를 계산
        const checkedDirections = Object.values(roomDetails.direction).filter(Boolean).length;

        if (checkedDirections > maxDirectionSelections) {
            // 사용자에게 경고 메시지를 표시
            alert('최대 두 개의 방향만 선택할 수 있습니다.');

            // 가장 최근의 선택을 취소
            roomDetails.direction[currentDirection] = false;
            event.target.checked = false;
        }
    }
    
    let error = { detail: [] };

    async function registerRoom(event) {
        event.preventDefault();
        let url = "/rooms";
        try {
            const response = await request('post', url, roomDetails);
            if (response) {
                // 서버로부터 성공적인 응답을 받았을 경우
                alert('방 등록이 완료되었습니다.'); // 사용자에게 알림
                push('/home'); // 사용자를 홈 화면으로 리다이렉트
            }
        } catch (err) {
            console.error('Room Registration Error:', err);
            error = JSON.parse(err.message);
            alert('방 등록에 실패했습니다.'); // 에러 메시지를 사용자에게 보여줌
        }
    }

</script>


  
<style>
    .page-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr); /* 4개의 동일한 너비 컬럼 */
    grid-gap: 20px; /* 그리드 사이의 간격 */
    max-width: 1280px;
    margin: 50px auto; /* 위아래 여백과 가운데 정렬 */
    padding: 20px;
    background: #FFFFFF;
    box-sizing: border-box;
    }

    .input-field, .input-label {
    background: #F0F0F0;
    border-radius: 10px;
    border: 1px solid #D3D3D3;
    padding: 12px;
    font-size: 16px;
    }

    .input-label {
    grid-column: span 1; /* 라벨은 하나의 컬럼을 차지합니다. */
    background: transparent;
    border: none;
    text-align: right; /* 텍스트를 오른쪽으로 정렬 */
    padding-right: 20px; /* 라벨과 필드 사이의 간격 */
    }

    .input-field {
    grid-column: span 3 /* 입력 필드는 세 개의 컬럼을 차지합니다. */
    }

    .button {
    grid-column: 2 / span 2; /* 버튼을 중앙에 배치 */
    width: 100%; /* 버튼 너비를 그리드 컬럼에 맞춥니다. */
    padding: 12px 0; /* 상하 패딩 */
    background: #FFBFBF;
    border-radius: 10px;
    border: none;
    cursor: pointer;
    font-size: 18px;
    color: #333;
    text-align: center;
    }

    .button:hover {
    background: #FFAFAF;
    }

    .checkbox-group {
    grid-column: span 3 /* 입력 필드는 세 개의 컬럼을 차지합니다. */
    }

    .checkbox-option {
    display: inline-block; /* 인라인 블록 요소로 설정 */
    width: 24%; /* 전체 너비의 약 25% (4개가 한 줄에 들어감) */
    margin-right: 1%; /* 각 옵션 사이의 간격 */
    box-sizing: border-box; /* 패딩과 보더가 너비에 포함되도록 설정 */
    }

    .checkbox-group label {
        margin-right: 5px; /* 레이블과 체크박스 사이의 간격 */
        white-space: nowrap; /* 레이블이 줄바꿈 되지 않도록 설정 */
    }

    .checkbox-group input[type="checkbox"] {
    margin-right: 5px; /* 체크박스의 오른쪽 마진 */
    }
    

</style>

<div class="page-container">


    <label for="room-nickname" class="input-label"> 방 닉네임 </label>
    <input id="room-nickname" class="input-field" type="text" bind:value={roomDetails.room_nickname} />

    <label for="address" class="input-label"> 주소 </label>
    <input id="address" class="input-field" type="text" bind:value={roomDetails.address} />

    <label for="area" class="input-label"> 평수 </label>
    <input id="area" class="input-field" type="number" bind:value={roomDetails.area} />

    <label for="deposit" class="input-label"> 보증금 (만원)</label>
    <input id="deposit" class="input-field" type="number" bind:value={roomDetails.deposit} />

    <label for="price" class="input-label"> 월세 (만원)</label>
    <input id="price" class="input-field" type="number" bind:value={roomDetails.price} />

    <label for="room_type" class="input-label">방 개수</label>
    <div class="checkbox-group">
        <input type="radio" bind:group={roomDetails.room_type} value="oneroom" id="oneroom"><label for="oneroom">원룸</label>
        <input type="radio" bind:group={roomDetails.room_type} value="tworoom" id="tworoom"><label for="tworoom">투룸</label>
        <input type="radio" bind:group={roomDetails.room_type} value="threeroom_plus" id="threeroom_plus"><label for="threeroom_plus">쓰리룸 이상</label>
    </div>

    <label for="direction" class="input-label">방향</label>
    <div class="checkbox-group">
        <input type="checkbox" bind:checked={roomDetails.direction.east} id="east" on:change={handleDirectionChange}><label for="east">동향</label>
        <input type="checkbox" bind:checked={roomDetails.direction.west} id="west" on:change={handleDirectionChange}><label for="west">서향</label>
        <input type="checkbox" bind:checked={roomDetails.direction.south} id="south" on:change={handleDirectionChange}><label for="south">남향</label>
        <input type="checkbox" bind:checked={roomDetails.direction.north} id="north" on:change={handleDirectionChange}><label for="north">북향</label>
    </div>

    <label for="floor" class="input-label">층수</label>
    <div class="checkbox-group">
        <input type="radio" bind:group={roomDetails.floor} value="first" id="first"><label for="first">1층</label>
        <input type="radio" bind:group={roomDetails.floor} value="second" id="second"><label for="second">2층</label>
        <input type="radio" bind:group={roomDetails.floor} value="third" id="third"><label for="third">3층</label>
        <input type="radio" bind:group={roomDetails.floor} value="fourth" id="fourth"><label for="fourth">4층</label>
        <input type="radio" bind:group={roomDetails.floor} value="etc" id="etc"><label for="etc">기타</label>
    </div>

    <label for="gate" class="input-label">가까운 문</label>
    <div class="checkbox-group">
        <input type="radio" bind:group={roomDetails.gate} value="gate1" id="gate1"><label for="gate1">북문/농장문/수영장문</label>
        <input type="radio" bind:group={roomDetails.gate} value="gate2" id="gate2"><label for="gate2">서문</label>
        <input type="radio" bind:group={roomDetails.gate} value="gate3" id="gate3"><label for="gate3">솔로문/조은문</label>
        <input type="radio" bind:group={roomDetails.gate} value="gate4" id="gate4"><label for="gate4">쪽문/정문/수의대문</label>
        <input type="radio" bind:group={roomDetails.gate} value="gate5" id="gate5"><label for="gate5">테크노문/나리문/동문</label>
    </div>

    <label for="is_contract" class="input-label">계약형태</label>
    <div class="checkbox-group">
        <input type="radio" bind:group={roomDetails.is_contract} value="monthly" id="monthly"><label for="monthly">월세</label>
        <input type="radio" bind:group={roomDetails.is_contract} value="jeonse" id="jeonse"><label for="jeonse">전세</label>
        <input type="radio" bind:group={roomDetails.is_contract} value="etc" id="contract_etc"><label for="contract_etc">기타</label>
    </div>

    <label for="option" class="input-label">상세옵션</label>
    <div class="checkbox-group">
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.rent_aid} id="rent_aid"><label for="rent_aid">월세 지원</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.preview} id="preview"><label for="preview">방 구경 가능</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.extension} id="extension"><label for="extension">계약 연장 가능</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.elec_bill} id="elec_bill"><label for="elec_bill">전기세 별도 부담</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.water_bill} id="water_bill"><label for="water_bill">수도세 별도 부담</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.gas_bill} id="gas_bill"><label for="gas_bill">가스비 별도 부담</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.kit_sep} id="kit_sep"><label for="kit_sep">주방 분리</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.stove_type} id="stove_type"><label for="stove_type">인덕션</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.fridge} id="fridge"><label for="fridge">냉장고 있음</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.ac} id="ac"><label for="ac">에어컨 있음</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.mw} id="mw"><label for="mw">전자레인지 있음</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.balcony} id="balcony"><label for="balcony">베란다 있음</label>
        </div>
        <div class="checkbox-option">
            <input type="checkbox" bind:checked={roomDetails.option.dryer} id="dryer"><label for="dryer">건조기 있음</label>
        </div>
    </div>
    

    <button class="button" on:click={registerRoom}>Save Room</button>
</div>
