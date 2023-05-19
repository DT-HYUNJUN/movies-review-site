# 프로젝트 기획

## 프로젝트 개요

| 프로젝트 목적 | 영화 리뷰 사이트를 처음 이용하는 비전문적인 영화 시청자를 위한 직관적이고 사용하기 편한 영화 리뷰 공유 웹사이트 제작 |
| --- | --- |
| 프로젝트 기간 | 5/9 ~ 5/19 |
| 발표 날짜 | 5/19 |
| 팀명 | 8은 안으로 굽조 |
| 주제 | 영화 리뷰 공유 웹사이트 |

## 기술 스택

<div align="center">
	<img src="https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=HTML5&logoColor=white"/>
	<img src="https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=CSS3&logoColor=white"/>
	<img src="https://img.shields.io/badge/JAVASCRIPT-F7DF1E?style=for-the-badge&logo=Javascript&logoColor=white"/>
	<br>
	<img src="https://img.shields.io/badge/DJANGO-092E20?style=for-the-badge&logo=django&logoColor=white">
	<img src="https://img.shields.io/badge/PYTHON-3776AB?style=for-the-badge&logo=Python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=BOOTSTRAP&logoColor=white"/>
  <img src="https://img.shields.io/badge/JQUERY-0769AD?style=for-the-badge&logo=JQUERY&logoColor=white"/>
	<br>
</div>

## 개발 역할 분담

| 이름 | 역할 |
| --- | --- |
| 박현준 | 조장님, 프론트엔드 개발 |
| 서유영 | 프론트엔드 개발 |
| 노현석 | 풀스택 마에스트로(reviews) |
| 이수한 | 백엔드 개발(accounts) |
| 최수현 | 백엔드 개발(movies) |

## 주제 사전 조사 & 분석

[왓챠피디아](https://pedia.watcha.com/ko-KR)

[TMDB API](https://developer.themoviedb.org/reference)

[롯데시네마](https://www.lottecinema.co.kr/NLCHS)

[메가박스](https://www.megabox.co.kr/)

## 서비스 주요 기능

<details>
  <summary> 회원관리 </summary>
  <div>
    - 회원가입
    - 로그인
    - 로그아웃
    - 회원 프로필
    - 팔로잉
  </div>
</details>

<details>
<summary> 영화 </summary>
<div>
  - 영화 장르별 검색
  - 영화 예고편
  - 트렌드 검색
  - 리뷰 작성
  - 컬렉션
  - 좋아요
  - 비슷한 작품
</div>
</details>

<details>
<summary>리뷰</summary>
<div>
  - 별점 차트
  - 댓글
</div>
</details>

## 모델(Model) 설계

![ERD](readme_img/erd.png)

## 화면(Template) 설계

<details>
  <summary>메인</summary>
  <div>
  <img src="readme_img/Untitled%201.png">
  </div>
</details>

<details>
<summary>회원가입 / 로그인</summary>
<div>
  - 회원가입
  <img src="readme_img/Untitled%202.png">
  - 로그인
  <img src="readme_img/Untitled%203.png">
</div>
</details>

<details>
<summary>검색</summary>
<div>
  - 키워드로 검색
  <img src="readme_img/Untitled%204.png">
  - 장르로 검색
  <img src="readme_img/Untitled%205.png">
</div>
</details>

<details>
<summary>영화 상세</summary>
<div>
  <img src="readme_img/Untitled%206.png">
</div>
</details>

<details>
<summary>인물</summary>
<div>
  <img src="readme_img/Untitled%207.png">
</div>
</details>

<details>
<summary>컬렉션</summary>
<div>
  <img src="readme_img/Untitled%208.png">
</div>
</details>