import re
import os
import sys
import glob
import pandas as pd
from collections import Counter

def load_data(file_path: str) -> tuple[pd.DataFrame, pd.Series]:
    """Load CSV data and extract movie titles."""
    print("Loading data")
    lb_data = pd.read_csv(file_path, sep=",")
    return lb_data

def main():

    if len(sys.argv) < 2:
        print("Usage: python analyze_subs.py input_file.csv")
        sys.exit(1)
    file = sys.argv[1]

    # Load data
    lb_data = load_data(file)
    fivestar_data = lb_data[lb_data['Rating'] == 5]

    #os.makedirs("processed_text_files", exist_ok=True)

    subtitle_subfolders = os.listdir("subtitles")
    processed_count = 0
    curr_dir = os.getcwd()
    all_scripts = {}
    n_words = []
    movie_titles = []

    for folder in subtitle_subfolders:
        print(folder)
        curr_path = os.path.join(curr_dir,"subtitles",folder)
        try:
            sub_file = os.path.join("subtitles",folder,os.listdir(curr_path)[0])
        except:
            continue            

        #script_file = f"\processed_text_files\{folder}.txt"

        #script_f = open(script_file, "a")
        sub_f = open(sub_file, encoding = 'latin-1')
          

        script_word_list = []
        n_total_words = 0

        while line := sub_f.readline():

            has_letters = re.search(r"[a-zA-Z]", line) is not None
            has_time_arrow = re.search("-->", line) is not None

            if has_letters and not has_time_arrow:
                line = re.sub('[.,?!():"]', '', line)
                #script_f.write(line)
                line_word_list = line.split()
                script_word_list.extend(line_word_list)
                n_total_words += len(line_word_list)  

        sub_f.close()
        #script_f.close()
        # TODO: make list of movie title and script_word_list:  
        movie_title = re.sub("_"," ", folder)
        movie_titles.append(movie_title)
        all_scripts[movie_title] = script_word_list
        n_words.append(len(script_word_list))

        processed_count += 1

        print(f"processed: {processed_count}")

    # counts = Counter(script_word_list)
    # print(counts.most_common(50))
    # print(f"total number of words in document: {n_total_words}")
    # #print(sorted(obj.keys())) print words alphabetically

    # # calculate relative frequency (also known as Term Frequency(TF))
    # rel_freqs = counts
    # for word in rel_freqs:
    #     rel_freqs[word] = rel_freqs[word] / n_total_words

    # If TF for 5 star films: 
    # 1. make list of movie title and script_word_list like above
    # 2. read lb_data and if movie_title has rating == 5 then concatenate script_word_list lists
    # 3. run Counter and calculate TF

    # For TF/IDF:
    # idf = log(n_subtitle_files/n_subtitle_files_containing_term)
    # n_subtitle_files = number of folders in /subtitles/containing .srt files
    # 4. have n documents from loopcount 
    # 5. see loop count below
    # script_list = list of length(non5starmovies) containing full scripts in each item
    # idf_nom = len(list), idf_denom: for movie in list; if re.search(term, movie) is not None; idf_denom += 1



if __name__ == "__main__":
    main()