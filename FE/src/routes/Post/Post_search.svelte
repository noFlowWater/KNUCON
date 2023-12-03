<script>
    import { navigateTo } from "../../util";
    import { access_token } from "../../lib/store";
    import { push } from 'svelte-spa-router';
    import request from '../../lib/request.js';
  
    // Reactive variables for form inputs
    let roomType = [];
    let isContract = [];
    let direction = [];
    let floor = [];
    let gate = [];
    let stoveType = [];
  
    // Variables for option selection 1
    let elecBill = false;
    let waterBill = false;
    let rentAid = false;
    let gasBill = false;
  
    // Variables for option selection 2
    let fridge = false;
    let ac = false;
    let mw = false;
    let dryer = false;
    let balcony = false;
    let kitSep = false;
    let preview = false;
    let extension = false;
  
    // Initial values for the area range
    let areaRange = { start: 0.5,  end: 50 };
    let depositRange = { start: 30, end: 2000 };
    let priceRange = { start: 20, end: 100 };
    
    // Variable for orderby
    let latest_desc = false;

    // Variable for Paging
    let totalPages = 0;  // Add this as a reactive variable
    let currentPage = 1;
    let pageSize = 10;
    

    let posts = [];
    const url = "/posts/search";
  
    // Function to fetch posts based on search criteria
    async function fetchPosts() {
      let response;
      let requestBody = {};

      // handling list variables
      if (roomType.length > 0) requestBody.room_type = roomType;
      if (isContract.length > 0) requestBody.is_contract = isContract;
      if (direction.length > 0) requestBody.direction = direction;
      if (floor.length > 0) requestBody.floor = floor;
      if (gate.length > 0) requestBody.gate = gate;
      if (stoveType.length > 0) requestBody.stove_type = stoveType;
      
      // handling range variables
      requestBody.area = areaRange;
      requestBody.deposit = depositRange;
      requestBody.price = priceRange;

      // handling boolean variables
      if (elecBill) requestBody.elec_bill = 1;
      if (waterBill) requestBody.water_bill = 1;
      if (rentAid) requestBody.rent_aid = 1;
      if (gasBill) requestBody.gas_bill = 1;
      if (fridge) requestBody.fridge = 1;
      if (ac) requestBody.ac = 1;
      if (mw) requestBody.mw = 1;
      if (dryer) requestBody.dryer = 1;
      if (balcony) requestBody.balcony = 1;
      if (kitSep) requestBody.kit_sep = 1;
      if (preview) requestBody.preview = 1;
      if (extension) requestBody.extension = 1;
      if (latest_desc) requestBody.latest_desc = 1;

      // handling page parameters
      requestBody.page = currentPage;
      requestBody.pageSize = pageSize;
  
      try {
            const headers = {
                'Authorization': `Bearer ${$access_token}`
            };
            // console.log("Request body:", requestBody);
            response = await request('POST', url, requestBody, headers);
            posts = response[0].map(postDataArray => parsePostData(postDataArray));
            totalPages = response[1];  // Assuming the backend sends this value
        } catch (error) {
            console.error('Error fetching posts:', error);
        }
    }

    // Function to parse post data array into an object
    function parsePostData(postDataArray) {
        let data = {};
        data = {
            post_id: postDataArray[0],
            user_id: postDataArray[1],
            post_status: postDataArray[2],
            post_date : postDataArray[3],
            post_view_count : postDataArray[4],
            post_title: postDataArray[5],
            wish_count: postDataArray[6]
        };
        // if (data.post_status === 1) {
        //   data.post_status = "들어온나"; 
        // } else if (data.post_status === 2) { 
        //   data.post_status = "들어가께"; 
        // }
        return data;
    }

    function nextPage() {
      currentPage++;
      fetchPosts();
    }

    function previousPage() {
      if (currentPage > 1) {
        currentPage--;
        fetchPosts();
      }
    }

    function setLatestDesc(value) {
      latest_desc = value;
    }

    async function navigateToPostDetail(post_id){
        console.log("post_id: "+post_id)
        // postId를 이용하여 상세 페이지로 네비게이션
        push(`/posts/${post_id}`);
    }
</script>
  
<!-- Post Search Format -->
<div class="container mx-auto" style="margin-top: 80px;">
  <form on:submit|preventDefault={fetchPosts}>
    <table class="table table-bordered border-dark">
      <!-- Room Type -->
      <tr>
        <td><label>방 개수:</label></td>
        <td>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="roomType1" value="1" bind:group={roomType}>
            <label class="form-check-label" for="roomType1">원룸</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="roomType2" value="2" bind:group={roomType}>
            <label class="form-check-label" for="roomType2">투룸</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="roomType3" value="3" bind:group={roomType}>
            <label class="form-check-label" for="roomType3">쓰리룸 이상</label>
          </div>
        </td>
      </tr>

    <!-- Contract Type -->
      <tr>
        <td><label>계약 형태: </label></td>
        <td>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="isContract0" value="0" bind:group={isContract}>
            <label class="form-check-label" for="isContract0">월세</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="isContract1" value="1" bind:group={isContract}>
            <label class="form-check-label" for="isContract1">전세</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="isContract2" value="2" bind:group={isContract}>
            <label class="form-check-label" for="isContract2">기타</label>
          </div>
        </td>
      </tr>

    <!-- Direction -->
    <tr>
        <td><label>방향:</label></td>
        <td>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction0" value="0" bind:group={direction}>
            <label class="form-check-label" for="direction0">북향</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction1" value="1" bind:group={direction}>
            <label class="form-check-label" for="direction1">북동향</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction2" value="2" bind:group={direction}>
            <label class="form-check-label" for="direction2">동향</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction3" value="3" bind:group={direction}>
            <label class="form-check-label" for="direction3">남동향</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction4" value="4" bind:group={direction}>
            <label class="form-check-label" for="direction4">남향</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction5" value="5" bind:group={direction}>
            <label class="form-check-label" for="direction5">남서향</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction6" value="6" bind:group={direction}>
            <label class="form-check-label" for="direction6">서향</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction7" value="7" bind:group={direction}>
            <label class="form-check-label" for="direction7">북서향</label>
          </div>
        </td>
      </tr>

    <!-- Floor -->
    <tr>
        <td><label>층:</label></td>
        <td>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction1" value="1" bind:group={floor}>
            <label class="form-check-label" for="direction1">1층</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction2" value="2" bind:group={floor}>
            <label class="form-check-label" for="direction2">2층</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction3" value="3" bind:group={floor}>
            <label class="form-check-label" for="direction3">3층</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction4" value="4" bind:group={floor}>
            <label class="form-check-label" for="direction4">4층</label>
          </div>
          <div class="form-check form-check-inline">
            <input class="form-check-input" type="checkbox" id="direction5" value="5" bind:group={floor}>
            <label class="form-check-label" for="direction5">기타</label>
          </div>
        </td>
      </tr>

    <!-- Area -->
    <tr>
      <td><label>평:</label></td>
      <td>
        <input type="number" id="areaStart" bind:value={areaRange.start} min="0.5" max={areaRange.end} step="0.5">
        <input type="number" id="areaEnd" bind:value={areaRange.end} min={areaRange.start} max="50" step="0.5">
        <input type="range" id="areaStart" bind:value={areaRange.start} min="0.5" max={areaRange.end} step="0.5">
        <input type="range" id="areaEnd" bind:value={areaRange.end} min={areaRange.start} max="50" step="0.5">
        <span>{areaRange.start}평 - {areaRange.end}평</span>
      </td>
    </tr>

    <!-- Gate -->
    <tr>
      <td><label style="margin-right: 60px;">위치:</label></td>
      <td>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="gate0" value="0" bind:group={gate}>
          <label class="form-check-label" for="gate0">북문</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="gate1" value="1" bind:group={gate}>
          <label class="form-check-label" for="gate1">서문</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="gate2" value="2" bind:group={gate}>
          <label class="form-check-label" for="gate2">쪽문</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="gate3" value="3" bind:group={gate}>
          <label class="form-check-label" for="gate3">수의대문</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="gate4" value="4" bind:group={gate}>
          <label class="form-check-label" for="gate4">나리문</label>
        </div>
      </td>
    </tr>

    <!-- Stove Type -->
    <tr>
      <td><label>가스 타입:</label></td>
      <td>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="stoveType0" value="0" bind:group={stoveType}>
          <label class="form-check-label" for="door0">인덕션</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="stoveType1" value="1" bind:group={stoveType}>
          <label class="form-check-label" for="door1">가스레인지</label>
        </div>
      </td>
    </tr>

    <!-- Deposit -->
    <tr>
      <td><label>보증금:</label></td>
      <td>
        <input type="number" id="depositStart" bind:value={depositRange.start} min="30" max={depositRange.end} step="10">
        <input type="number" id="depositEnd" bind:value={depositRange.end} min={depositRange.start} max="2000" step="10">
        <input type="range" id="depositStart" bind:value={depositRange.start} min="30" max={depositRange.end} step="10">
        <input type="range" id="depositEnd" bind:value={depositRange.end} min={depositRange.start} max="2000" step="10">
        <span>{depositRange.start}만원 - {depositRange.end}만원</span>
      </td>
    </tr>
    <!-- Amount (Price) -->
    <tr>
      <td><label>금액:</label></td>
      <td>
        <input type="number" id="priceStart" bind:value={priceRange.start} min="20" max={priceRange.end} step="1">
        <input type="number" id="priceEnd" bind:value={priceRange.end} min={priceRange.start} max="100" step="1">
        <input type="range" id="priceStart" bind:value={priceRange.start} min="20" max={priceRange.end} step="1">
        <input type="range" id="priceEnd" bind:value={priceRange.end} min={priceRange.start} max="100" step="1">
        <span>{priceRange.start}만원 - {priceRange.end}만원</span>
      </td>
    </tr>

    <!-- Additional1 -->
    <tr>
      <td><label style="margin-right: 60px;">선택 사항1:</label></td>
      <td>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="elecBill" value="1" bind:checked={elecBill}>
          <label class="form-check-label" for="elecBill">전기세 X</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="waterBill" value="1" bind:checked={waterBill}>
          <label class="form-check-label" for="waterBill">수도세 X</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="rentAid" value="1" bind:checked={rentAid}>
          <label class="form-check-label" for="rentAid">월세 지원</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="gasBill" value="1" bind:checked={gasBill}>
          <label class="form-check-label" for="gasBill">가스비 X</label>
        </div>
      </td>
    </tr>


    <!-- Additional2 -->
    <tr>
      <td><label style="margin-right: 60px;">선택 사항2:</label></td>
      <td>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="fridge" value="1" bind:checked={fridge}>
          <label class="form-check-label" for="fridge">냉장고</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="ac" value="1" bind:checked={ac}>
          <label class="form-check-label" for="ac">에어컨</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="mw" value="1" bind:checked={mw}>
          <label class="form-check-label" for="mw">전자레인지</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="dryer" value="1" bind:checked={dryer}>
          <label class="form-check-label" for="dryer">건조기</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="balcony" value="1" bind:checked={balcony}>
          <label class="form-check-label" for="balcony">발코니</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="kitSep" value="1" bind:checked={kitSep}>
          <label class="form-check-label" for="kitSep">주방 분리</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="preview" value="1" bind:checked={preview}>
          <label class="form-check-label" for="preview">방 미리보기 가능</label>
        </div>
        <div class="form-check form-check-inline">
          <input class="form-check-input" type="checkbox" id="extension" value="1" bind:checked={extension}>
          <label class="form-check-label" for="extension">계약 연장 가능</label>
        </div>
      </td>
    </tr>
    <!-- Orderby -->
    <tr>
      <td><label style="margin-right: 60px;">정렬:</label></td>
      <td>
        <!-- 찜순 (Wish Order) -->
        <input type="radio" id="wish_order" name="latest_desc" value="false" checked on:change={() => setLatestDesc(false)} />
        <label for="wish_order">찜순</label>

        <input type="radio" id="latest_order" name="latest_desc" value="true" on:change={() => setLatestDesc(true)} />
        <label for="latest_order">최신순</label>
      </td>  
    </tr>

  </table>

  <!-- 필터 요청 및 게시글 작성 버튼 -->
  <div class="buttons-container">
    <button class="btn-filter">필터링 검색</button>
    <button class="btn-create" on:click={() => navigateTo(`/posts/create`)}>게시글 작성</button>
  </div>

  <!-- Post Display Section -->
  <div class="display-container">
    {#if posts.length > 0}
      <div class="post-container">
        <strong> Post Details:</strong>
        {#each posts as post}
          <div class="post" on:click={() => navigateToPostDetail(post.post_id)}>
              <div class="post-header">
                  <h2 class="post-title">{post.post_title}</h2>
                  <span class="post-status">
                      {#if post.post_status === 0}
                          들어오세유
                      {:else if post.post_status === 1}
                          들어갈래유
                      {:else if post.post_status === 2}
                          끝났뿌따
                      {/if}
                  </span>
              </div>
              <div class="post-details">
                  <span class="post-id">ID: {post.post_id}</span>
                  <span class="post-author">글쓴이: {post.user_id}</span>
                  <span class="post-date">{post.post_date}</span>
                  <span class="post-views">조회수: {post.post_view_count}</span>
                  <span class="post-wishes">찜: {post.wish_count}</span>
              </div>
          </div>
        {/each}
      </div>
    {/if}
  </div>

  <!-- Page Controls -->
  <div class="pagination-container">
    {#if currentPage > 1}
      <button on:click={previousPage} class="btn-pagination">이전 페이지</button>
    {/if}

    <p class="page-info">Page: {currentPage}/{totalPages}</p>

    {#if currentPage < totalPages}
      <button on:click={nextPage} class="btn-pagination">다음 페이지</button>
    {/if}
  </div>
</div>




<style>
.buttons-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.btn-filter, .btn-create {
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.btn-filter {
    background-color: #007bff;
    color: white;
}

.btn-create {
    background-color: #28a745;
    color: white;
}

.display-container {
    margin-top: 20px;
}

.post-container {
    margin-left: 30px;
}

.post {
    background-color: #f9f9f9;
    border: 1px solid #ddd;
    padding: 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    cursor: pointer;
}

.post-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 5px;
}

.post-title {
    font-size: 18px;
    color: #007bff;
    margin: 0;
}

.post-status {
    background-color: #28a745;
    color: white;
    padding: 3px 6px;
    border-radius: 4px;
    font-size: 14px;
}

.post-details {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    font-size: 14px;
    color: #666;
}

.post-id, .post-author, .post-date, .post-views, .post-wishes {
    white-space: nowrap;
}


.pagination-container {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
}

.btn-pagination {
    padding: 5px 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    cursor: pointer;
    background-color: #6c757d;
    color: white;
}

.page-info {
    margin: 0 15px;
}

</style>