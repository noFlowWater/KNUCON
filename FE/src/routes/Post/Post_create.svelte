<script>
    import request from '../../lib/request.js';
    import { access_token } from "../../lib/store"
  
    const url1 = "/posts/create";
    let username = 'your_username'; // 사용자 이름
    let password = 'your_password'; // 비밀번호
  
    let posts = [];
    let postContent = '';
    let selectedPostId = null;
    
  
  </script>
  
async function createPost() {
    try {
      await request('POST', url1, { content: postContent }, {}, username, password);
      postContent = '';
      await fetchPosts();
    } catch (error) {
      console.error('Error creating post', error);
    }
  }


<style>
/* Which post do you want to write? */

position: absolute;
width: 474px;
height: 36px;
left: 407px;
top: 242px;

font-family: 'Inter';
font-style: normal;
font-weight: 400;
font-size: 30px;
line-height: 36px;
display: flex;
align-items: center;
text-align: center;

color: #000000;



/* button_들어간디작성 */

/* Auto layout */
display: flex;
flex-direction: row;
justify-content: center;
align-items: center;
padding: 0px;
gap: 10px;

position: absolute;
width: 250px;
height: 191px;
left: 670px;
top: 315px;

background: #AFD08F;
border-radius: 37px;


/* button_들어간디 */

width: 111px;
height: 36px;

font-family: 'Inter';
font-style: normal;
font-weight: 400;
font-size: 30px;
line-height: 36px;
display: flex;
align-items: center;
text-align: center;

color: #000000;


/* Inside auto layout */
flex: none;
order: 0;
flex-grow: 0;


/* button_들어온나작성 */

/* Auto layout */
display: flex;
flex-direction: row;
justify-content: center;
align-items: center;
padding: 0px;
gap: 10px;

position: absolute;
width: 250px;
height: 191px;
left: 360px;
top: 315px;

background: #FFD568;
border-radius: 34px;


/* button_들어온나 */

width: 111px;
height: 36px;

font-family: 'Inter';
font-style: normal;
font-weight: 400;
font-size: 30px;
line-height: 36px;
display: flex;
align-items: center;
text-align: center;

color: #000000;


/* Inside auto layout */
flex: none;
order: 0;
flex-grow: 0;


/* button_back */

/* Auto layout */
display: flex;
flex-direction: row;
justify-content: center;
align-items: center;
padding: 0px;

position: absolute;
width: 130px;
height: 41px;
left: 580px;
top: 549px;

background: #D9D9D9;


/* undo

arrow, backward, mail, previous, redo, repeat, rotate, undo
*/

width: 24px;
height: 24px;


/* Inside auto layout */
flex: none;
order: 0;
flex-grow: 0;


/* Vector */

position: absolute;
left: 7.35%;
right: 7.35%;
top: 31.25%;
bottom: 31.25%;

background: #000000;


/* back */

width: 91px;
height: 34px;

font-family: 'Inter';
font-style: normal;
font-weight: 400;
font-size: 30px;
line-height: 36px;
display: flex;
align-items: center;
text-align: center;

color: #000000;


/* Inside auto layout */
flex: none;
order: 1;
flex-grow: 0;
</style>