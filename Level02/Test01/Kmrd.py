import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

movies_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/kmrd-small/movies.txt'
peoples_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/kmrd-small/peoples.txt'
genres_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/kmrd-small/genres.csv'
countries_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/kmrd-small/countries.csv'
castings_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/kmrd-small/castings.csv'
rates_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/kmrd-small/rates.csv'

# 각 데이터 불러오기
movies_df = pd.read_csv(movies_path, delimiter='\t')
peoples_df = pd.read_csv(peoples_path, delimiter='\t')
genres_df = pd.read_csv(genres_path)
countries_df = pd.read_csv(countries_path)
castings_df = pd.read_csv(castings_path)
rates_df = pd.read_csv(rates_path)

# 데이터 구조 확인
print("Movies Data:")
print(movies_df.head())
print(movies_df.info())
print("Peoples Data:")
print(peoples_df.head())
print("Genres Data:")
print(genres_df.head())
print("Countries Data:")
print(countries_df.head())
print("Castings Data:")
print(castings_df.head())
print("Rates Data:")
print(rates_df.head())

# 영화 데이터 열 항목 확인
print("Movies Columns:", movies_df.columns)

# 장르 데이터와 영화 데이터를 병합하여 분석
if 'movie' in movies_df.columns and 'movie' in genres_df.columns:
    merged_df = pd.merge(movies_df, genres_df, on='movie')
    print("Merged Data (Movies and Genres):")
    print(merged_df.head())

    # 장르별 영화 수 시각화
    plt.figure(figsize=(12, 6))
    sns.countplot(y=merged_df['genre'], order=merged_df['genre'].value_counts().index, palette='viridis')
    plt.title('Number of Movies by Genre')
    plt.xlabel('Count')
    plt.ylabel('Genre')
    plt.show()
else:
    print("The 'genre' or 'movie' column is missing in one of the dataframes.")

# 영화 개봉 연도 분포 시각화
if 'year' in movies_df.columns:
    plt.figure(figsize=(10, 6))
    sns.histplot(movies_df['year'], bins=20, kde=False, color='blue')
    plt.title('Distribution of Movie Release Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Movies')
    plt.show()
else:
    print("The 'year' column is missing in movies_df.")

# 평점 데이터 시각화
if 'rating' in rates_df.columns:
    print("Rates Data Description:")
    print(rates_df['rating'].describe())

    plt.figure(figsize=(10, 6))
    sns.histplot(rates_df['rating'], bins=10, kde=True, color='green')
    plt.title("Distribution of Ratings")
    plt.xlabel('Rating')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("The 'rating' column is missing in rates_df.")

# 사용자 기반 평점 분석
if 'user_id' in rates_df.columns and 'rating' in rates_df.columns:
    user_ratings = rates_df.groupby('user_id')['rating'].mean()
    print("Average Ratings by Users:")
    print(user_ratings.head())

    plt.figure(figsize=(10, 6))
    sns.histplot(user_ratings, bins=20, kde=True, color='orange')
    plt.title('Average Ratings by Users')
    plt.xlabel('Average Rating')
    plt.ylabel('Frequency')
    plt.show()
else:
    print("The 'user_id' or 'rating' column is missing in rates_df.")

# 출연 배우와 영화 데이터 분석
if 'people' in castings_df.columns and 'people' in peoples_df.columns:
    castings_merged = pd.merge(castings_df, peoples_df, on='people')
    print("Merged Castings and Peoples Data:")
    print(castings_merged.head())

    # 특정 배우가 출연한 영화 개수 상위 10명 시각화
    top_actors = castings_merged['korean'].value_counts().head(10)
    print("Top 10 Actors by Movie Appearances:")
    print(top_actors)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top_actors.values, y=top_actors.index, palette='magma')
    plt.title('Top 10 Actors by Movie Appearances')
    plt.xlabel('Number of Movies')
    plt.ylabel('Actor')
    plt.show()
else:
    print("The 'people' column is missing in one of the dataframes.")