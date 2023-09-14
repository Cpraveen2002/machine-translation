import os

####### tokenization ########

special_chars = [".", "•", "'", '"', "|", "।", "!", "(", ")", ",", "&", "@", "-", "“", "”", "—", "-", ":", ";", "‘", "’", "\xa0", "\u200c", "\u200d", "\n"]

def tokens_of_word(word):
    word = word.lower()
    for char in special_chars:
        word = word.replace(char, " ")
    return_words = []
    for split in word.split(" "):
        # try:
        #     if split[-2:] == "’s" or split[-2:] == "'s":
        #         split = split[:-1]
        # except:
        #     split = split
        if split == "" or split == " ":
            continue
        # if split in stop_list:
        #     continue
        return_words.append(split)
    return return_words

def tokens_of_sentences(sentence_one, sentence_two):
    first_set = set()
    first_arr = []
    for word in sentence_one.split(" "):
        tokens = tokens_of_word(word)
        for token in tokens:
            if token not in first_set:
                first_set.add(token)
                first_arr.append(token)
    second_set = set()
    second_arr = []
    for word in sentence_two.split(" "):
        tokens = tokens_of_word(word)
        for token in tokens:
            if token not in second_set:
                second_set.add(token)
                second_arr.append(token)
    ## area to perform lemmatization, stemming, ... stuff
    print(first_set)
    print(second_set)
    first_arr.extend(second_arr)
    return first_arr

def handle_tokenization(file_one, file_two):
    return_tokens = []
    first_file = open(file_one, "r", encoding = "utf8")
    second_file = open(file_two, "r", encoding = "utf8")
    first_lines = first_file.readlines()
    second_lines = second_file.readlines()
    for iterr in range(len(first_lines)):
        tokens_arr = tokens_of_sentences(first_lines[iterr], second_lines[iterr])
        for token in tokens_arr:
            return_tokens.append([token, iterr+1])
    # return_tokens.sort(key = lambda x: (x[0], x[1]))
    return return_tokens

handle_tokenization("./data/test.hi", "./data/test.te")