import pandas as pd
import string
from collections import Counter
from nltk.corpus import words
from Word_Analyzer import analyze_word

#csv found when inspecting element on website
url = 'https://stuckonwordle.s3.amazonaws.com/wordle/history.csv'
solutions_df = pd.read_csv(url)

#keeps just solution and date
wordles_df = solutions_df[['solution','print_date']]
wordles_df.rename(columns={'solution':'solution','print_date':'date'},inplace=True,)

#list of wordle solutions
solutions = wordles_df['solution']

#setups counter
letter_counts = Counter()

#for each character that is ascii lowercse in each word update letter_counts dict
for sol in solutions:
    letter_counts.update([ch for ch in sol if ch in string.ascii_lowercase])

#turns letter counts into a dataframe
    # .items returns key value pairs
    # list converts key value pairs into a list of tuples      
    # sort dataframe by letter count and filter to top 10      
letter_counts_df = pd.DataFrame(list(letter_counts.items()), columns=['letter','count'])
letter_counts_df = letter_counts_df.sort_values(by='count', ascending=False)
top_10_letters_df = letter_counts_df.head(10)

# concat top 10 letters into a single string
letters_string = str(''.join(top_10_letters_df['letter'].tolist()))

#word list from nltk package/download
word_list = words.words()

#filter word_list to five letter words
five_letter_words = [w for w in word_list if len(w)==5]

#create emtpy list to house valid words
valid_words = []
#check what words can be made from letters
for word in five_letter_words:
    valid=True
    for l in word:
        if l not in letters_string or word.count(l) > letters_string.count(l):
            valid=False
            break
    if valid:
        valid_words.append(word)

#create Excel writer and save location
#/ used at end of save path so as not be read as an escape sequence
save_path = "G:\My Drive\Python\Wordle Project/"

rows = [analyze_word(word) for word in valid_words]
final_df = pd.DataFrame(rows)

#add dataframes to excel
final_df.to_excel(save_path+'words.xlsx', index=False, engine='openpyxl')
top_10_letters_df.to_excel(save_path+'top 10 wordle letters.xlsx', index=False, engine='openpyxl')
wordles_df.to_excel(save_path+'wordle solutions.xlsx', index=False, engine='openpyxl')

print("Done")
