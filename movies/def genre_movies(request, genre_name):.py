def genre_movies(request, genre_name):
    # 장르별 딕셔너리
    genre_dict = {
        '액션'         : '28',
        '어드벤처'     : '12',
        '애니메이션'   : '16',
        '코미디'       : '35',
        '범죄'         : '80',
        '다큐멘터리'   : '99',
        '드라마'       : '18',
        '가족'         : '10751',
        '판타지'       : '14',
        '역사'         : '36',
        '공포'         : '27',
        '음악'         : '10402',
        '미스터리'     : '9648',
        '로맨스'       : '10749',
        'SF'           : '878',
        'TV'           : '10770',
        '스릴러'       : '53',
        '전쟁'         : '10752',
        '서부'         : '37'
    }
    
    # 페이지 정보를 받아올 URL
    params = {
        'api_key'    : api_key,
        'language'   : 'ko-KR',
        'region'     : 'kr',
        'with_genres': genre_dict[genre_name]
    }
    path = '/discover/movie'

    # JSON 응답에서 총 페이지 수를 추출
    response = requests.get(base_url + path, params=params).json()
    
    # 파라미터 가져오기
    page    = request.GET.get('page', 1)
    # 기본: 인기순
    sort_by = request.GET.get('sort_by', 'popularity.desc')

    movies            = []
    params['page']    = page
    params['sort_by'] = sort_by
    response          = requests.get(base_url + path, params=params).json()
    total_pages       = response['total_pages']
    total_results     = response['total_results']
    
    # 페이지네이터 객체 생성
    paginator = Paginator(range(1, total_pages+1), 1)
    # ex) 1 of 109 page
    pages = paginator.page(page)

    movies += response['results']
    
    context = {
        'genre_name'   : genre_name,
        'movies'       : movies,
        'pages'        : pages,
        'total_results': total_results,
    }

    return render(request, 'movies/genre_movies.html', context)