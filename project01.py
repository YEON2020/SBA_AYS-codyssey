import pandas as pd
import re
from collections import Counter, defaultdict
from datetime import datetime

# 데이터 불러오기
file_path = r'C:\Users\OWNER\Downloads\prob-0101.csv'
df = pd.read_csv(file_path)

# 데이터 분석
print("\n--- 데이터 분석 ---")
print(f"전체 영화 개수: {len(df)}")
print(f"중복 제외 배급사 수: {df['배급사'].nunique()}")
print(f"중복 제외 감독 수: {df['감독'].nunique()}")

# 출연진 중복 제거
unique_cast = set(','.join(df['출연진'].dropna()).split(','))
print(f"중복 제외 출연진 수: {len(unique_cast)}")

# 장르 중복 제거
unique_genres = set(re.split(r'[·,/]', ','.join(df['장르'].dropna())))
print(f"중복 제외 장르 수: {len(unique_genres)}")

# 중복 조건 확인
print("\n--- 중복 조건 확인 ---")
# 같은 감독의 영화
duplicate_directors = df.groupby('감독')['제목'].apply(list).loc[lambda x: x.map(len) > 1] # 감독별 영화 제목들을 리스트로 변환
print(f"같은 감독의 영화: {[f'{director}: {movies}' for director, movies in duplicate_directors.items()]}")

# 같은 출연진이 포함된 영화
actor_to_movies = defaultdict(list)
for _, row in df[['제목', '출연진']].dropna().iterrows():
    for actor in row['출연진'].split(','):
        actor_to_movies[actor.strip()].append(row['제목'])

actors_in_multiple_movies = {actor: movies for actor, movies in actor_to_movies.items() if len(movies) > 1}
print("\n같은 출연진이 포함된 영화:")
if actors_in_multiple_movies:
    for actor, movies in actors_in_multiple_movies.items():
        print(f"{actor}: {', '.join(movies)}")
else:
    print("중복되는 출연진이 없습니다.")

# 계절에 맞는 영화 추천
def get_season(date):
    month = date.month
    if month in [12, 1, 2]:
        return '겨울'
    elif month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    else:
        return '가을'

df['개봉일'] = pd.to_datetime(df['개봉일'], errors='coerce')
df['계절'] = df['개봉일'].apply(get_season)
season_genre_map = {
    '겨울': ['드라마'],
    '봄': ['액션', '스릴러'],
    '여름': ['공포', '스릴러'],
    '가을': ['로맨스']
}
current_season = '겨울'  # 계절 입력 예시
if current_season in season_genre_map:
    season_genres = season_genre_map[current_season]
    season_recommendations = df[df['장르'].apply(lambda x: any(genre in x for genre in season_genres))]
    print("--- 계절 기반 영화 추천 ---")
    print(f"{current_season} 계절에 추천하는 영화:")
    print(season_recommendations[['제목', '장르']])
else:
    print(f"{current_season} 계절에 대한 추천이 없습니다.")

# 사용자 맞춤형 가중치 기반 추천
user_weights = {'장르': 0.4, '출연진': 0.3, '개봉일': 0.3}
df['사용자_추천점수'] = (
    df['장르'].apply(lambda x: user_weights['장르'] if '드라마' in x else 0) +
    ((df['출연진'].apply(lambda cast: sum(Counter(','.join(df['출연진'].dropna()).split(','))[actor.strip()] for actor in cast.split(',')) if pd.notnull(cast) else 0)) / df['출연진'].apply(lambda x: max(df['출연진'].apply(lambda y: len(y.split(',')) if pd.notnull(y) else 0))) * user_weights['출연진']) +
    ((df['개봉일'] - df['개봉일'].min()).dt.days / (df['개봉일'].max() - df['개봉일'].min()).days * user_weights['개봉일'])
)
user_recommendations = df.sort_values(by='사용자_추천점수', ascending=False).head(5)
print("--- 임의의 가중치 설정 기반 추천 ---")
print("사용자 맞춤형 추천 영화:")
print(user_recommendations[['제목', '사용자_추천점수']])

# 하루에 2편 이상 개봉한 날짜 출력
release_count = df['개봉일'].value_counts()
multiple_releases = release_count[release_count > 1]
print("--- 하루에 2편 이상 개봉날짜 ---")
print("하루에 2편 이상 개봉한 날짜:")
print(multiple_releases.to_string(index=True))

# 동시 개봉 영화 가장 많은 날짜
most_releases_date = release_count.idxmax().date()
most_releases_count = release_count.max()
print("--- 동시 개봉 영화날짜 ---")
print(f"동시 개봉 영화 가장 많은 날짜: {most_releases_date} ({most_releases_count}편)")