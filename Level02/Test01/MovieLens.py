import pandas as pd
import matplotlib.pyplot as plt

file_path = r'C:/Users/OWNER\Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/ml-latest-small/movies.csv'
ratings_file_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/ml-latest-small/ratings.csv'
tags_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/ml-latest-small/tags.csv'
links_path = r'C:/Users/OWNER/Desktop/Codyssey_AYS/SBA_AYS-codyssey/Level02/ml-latest-small/links.csv'

movies_df = pd.read_csv(file_path)
ratings_df = pd.read_csv(ratings_file_path)
tags_df = pd.read_csv(tags_path)
links_df = pd.read_csv(links_path)

#movies.csv 시각화
print('Movies data shape: ', movies_df.shape)
print(movies_df.head())
genres_count = movies_df['genres'].str.split('|').apply(pd.Series).stack().value_counts()
genres_count.plot(kind='bar')
plt.title('Number of Movies by Genre')
plt.xlabel('Genre')
plt.ylabel('Number of Movies')
plt.show()

#ratings.csv 시각화
print('Ratings data shape: ', ratings_df.shape)
print(ratings_df.head())
ratings_df['rating'].hist(bins=20)
plt.title('Distribution of Ratings')
plt.xlabel('Rating')
plt.ylabel('Number of Ratings')
plt.show()

#tags.csv 시각화
print('Tags data shape: ', tags_df.shape)
print(tags_df.head())
tag_count = tags_df['tag'].value_counts().head(10)
tag_count.plot(kind='bar')
plt.title('Top 10 Tags')
plt.xlabel('Tag')
plt.ylabel('Frequency')
plt.show()

#links.csv 형태
print('Links data shape: ', links_df.shape)
print(links_df.head())