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

    while line := sub_f.readline():

        has_letters = re.search(r"[a-zA-Z]", line) is not None
        has_time_arrow = re.search("-->", line) is not None

        if has_letters and not has_time_arrow:
            script_f.write(line)
            line_word_list = line.split()
            script_word_list.extend(line_word_list)  

    sub_f.close()
    script_f.close()

    print("Counter")
    print(Counter(script_word_list).most_common(100))

if __name__ == "__main__":
    main()