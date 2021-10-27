# preonboarding


#회원가입(SignUp)
- 회원가입은 이메일과 패스워드를 필수 작성으로 두고 이메일과 패스워드는 정규식을 이용하여 형식을 구현했습니다.
- 프로플에 사진을 삽입할수 있게 구현 하였습니다. 
- 패스워드는 bcrypt를 사용하여 암호화하여 사용하게 구현했습니다.

#로그인(SignIn)
- 로그인시 토큰이 발생하며 decorator를 이용하여 앞으로 이용할 게시물에대한 사용권한을 제한하게 구현했습니다.

#게시물(board)
- 게시물 조회는 모든 유저가 사용 가능하며 조회는 limit, offest 0부터 10까지 조회가 가능한 페이징네이션을 하게 구현하였습니다.
- 게시물 삭제, 수정, 상세페이지 게시물은 로그인한 유저만 사용하게 구현했습니다.

#엔드포인트
- 회원가입 - POST/users/signup
- 로그인  - POST/users/singin
- 게시물 생성 - POST/board (only Signin user)
- 게시물 조회 - GET/board
- 상세 페이지 게시물 조회 - GET/board/int:board_id
- 상세 페이지 게시물 삭제 - DELETE/board/int:board_id
- 상페 페이지 게시물 수정 - PATCH/board/int:board_id
