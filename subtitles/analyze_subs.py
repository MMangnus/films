import re
import os
from collections import Counter

def main():

    os.makedirs("processed_text_files", exist_ok=True)

    sub_file = r""
    sub_f = open(sub_file, encoding="utf-8")

    script_file = 'script.txt'
    script_f = open(script_file, "a")

    script_word_list = []
    n_total_words = 0

    while line := sub_f.readline():

        has_letters = re.search(r"[a-zA-Z]", line) is not None
        has_time_arrow = re.search("-->", line) is not None

        if has_letters and not has_time_arrow:
            line = re.sub('[.,?!():"]', '', line)
            script_f.write(line)
            line_word_list = line.split()
            script_word_list.extend(line_word_list)
            n_total_words += len(line_word_list)  

    # TODO: make list of movie title and script_word_list

    sub_f.close()
    script_f.close()

    counts = Counter(script_word_list)
    print(counts.most_common(50))
    print(f"total number of words in document: {n_total_words}")
    #print(sorted(obj.keys())) print words alphabetically

    # calculate relative frequency (also known as Term Frequency(TF))
    rel_freqs = counts
    for word in rel_freqs:
        rel_freqs[word] = rel_freqs[word] / n_total_words

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