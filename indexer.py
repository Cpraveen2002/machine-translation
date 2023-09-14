import os
import re
import sys
import unsupervised

####################################################################################################################

special_chars = [".", "•", "'", '"', "।", "|", "।", "!", "(", ")", ",", "&", "@", "-", "“", "”", "—", "-", ":", ";", "‘", "’", "\xa0", "\u200c", "\u200d", "\n"]

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
    # print(first_set)
    # print(second_set)
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
    return_tokens.sort(key = lambda x: (x[0], x[1]))
    first_file.close()
    second_file.close()
    return return_tokens, first_lines, second_lines

####################################################################################################################

####################################################################################################################

class LLNode:
    def __init__(self, val, next=None):
        self.val = val
        self.next = next

def indexer(tokens):
    return_dict = {}
    prev_node = None
    for token in tokens:
        if token[0] in return_dict:
            prev_node.next = LLNode(token[1])
            prev_node = prev_node.next
            return_dict[token[0]][0] += 1
        else:
            return_dict[token[0]] = [1, None]
            return_dict[token[0]][1] = LLNode(token[1])
            prev_node = return_dict[token[0]][1]
    return return_dict

####################################################################################################################

def print_inverted_index(index):
    print("term [doc_freq] -> posting_list")
    for key, value in index.items():
        print(key, " [", value[0], "] -> ", end="")
        values = []
        currNode = value[1]
        while currNode != None:
            values.append(currNode.val)
            currNode = currNode.next
        for iterrr in range(len(values)):
            if iterrr == len(values)-1:
                print(values[iterrr])
            else:
                print(values[iterrr], " -> ", end="")

print(" ====== Loading dataset and tokenizing ==========")
total_tokens, hindi_lines, telugu_lines = handle_tokenization("./data/test.hi", "./data/test.te")
print("\n Completed Tokenization")
print(" \n =========== Creating Inverted Index =========== \n")
inverted_index = indexer(total_tokens)
# print_inverted_index(inverted_index)

print("term [doc_freq] -> posting_list")

####################################################################################################################

# print_inverted_index(inverted_index)
# print(inverted_index.keys())

def make_query(inverted_index, query_str):
    strings = query_str.split(" ")
    total_words = []
    for string in strings:
        total_words.extend(tokens_of_word(string))
    doc_ids_dict = {}
    for word in total_words:
        if word in inverted_index:
            curr_node = inverted_index[word][1]
            while curr_node != None:
                if curr_node.val in doc_ids_dict:
                    doc_ids_dict[curr_node.val] += 1
                else:
                    doc_ids_dict[curr_node.val] = 1
                curr_node = curr_node.next
    doc_id_freq = []
    for key in doc_ids_dict:
        doc_id_freq.append([key, doc_ids_dict[key]])
    doc_id_freq.sort(key = lambda x: -x[1])
    # print(doc_id_freq)
    most_matched_line = doc_id_freq[0][0]
    # print(most_matched_line)
    # print(hindi_lines[most_matched_line])
    return hindi_lines[most_matched_line]

####################################################################################################################

def index_pos_training(file_path):
    file = open(file_path, 'r', encoding='utf-8')
    tag_dict = {}
    for line in file.readlines():
        words = line.replace("\n", "").split(" ")
        if "<" in line:
            continue
        if words[0] not in tag_dict:
            tag_dict[words[0]] = words[1]
    return tag_dict

def get_pos_tagging(tag_dict, input):
    return_string = ""
    return_matrix = []
    for word in input.split(" "):
        if word in tag_dict:
            return_string += word + "_" + tag_dict[word] + " \n"
            return_matrix.append([word, tag_dict[word]])
        else:
            return_string += word + "_" + "\n"
    # print(return_string)
    return return_matrix

tel_tag_dict = index_pos_training('./data/telugu_training.txt')
hin_tag_dict = index_pos_training('./data/hindi_training.txt')

####################################################################################################################

## NER IDENTIFICATION (NAMED ENTITY RECOGNITION)

# identify numbers or emails
def identify_ner_rule_one(input_text):
    words = []
    return_one = []
    for word in input_string.split(" "):
        words.extend(tokens_of_word(word))
    for word in words:
        returned = re.findall('[0-9]+', word)
        if len(returned) > 0:
            return_one.append(word)
        # returned = re.findall(r'[\w\.-]+@[\w\.-]+', word)
        returned = re.findall(r'^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+$', word)
        if len(returned) > 0:
            return_one.append(word)
    return return_one

# identify locations in telugu words
def identify_ner_rule_two(input_text):
    words = []
    return_two = []
    for word in input_text.split(" "):
        words.extend(tokens_of_word(word))
    location = ['పురం', 'పుట్నం', 'నగరం', 'మహానగరం', 'గ్రామం', 'వీధి', 'పట్టణం']
    for word in words:
        for loc in location:
            if word.find(loc) != -1:
                return_two.append(word)
                break
    return return_two

####################################################################################################################

####################################################################################################################

####################################################################################################################

# make_query(inverted_index, "వారి స్థిరమైన సాహసం మరియు దేశభ‌క్తి మ‌న దేశం సుర‌క్షితం గా ఉండేటట్టు చూశాయి.")

# input_string = ""
# curr_count = 0
# for line in telugu_lines:
#     words = []
#     for word in line.split(" "):
#         words.extend(tokens_of_word(word))
#     # input_string += line + " "
#     for word in words:
#         input_string += word + " "
#     curr_count += 1
#     if curr_count >= 40:
#         break

# input_string = "మ‌న భ‌ద్ర‌త ద‌ళాల యొక్క సాహ‌సం పట్ల, ప‌రాక్ర‌మం ప‌ట్ల మ‌న‌ కు పూర్తి న‌మ్మ‌కం ఉంది."
input_string = str(sys.argv[1])
# hin_input_string = "हमें अपने सैनिकों के शोर्य पर, उनकी बहादुरी पर पूरा भरोसा है।"


returned_line = make_query(inverted_index, input_string)
returned_line_seq = []
for word in returned_line.split(" "):
    for k in tokens_of_word(word):
        returned_line_seq.append(k)

print("\n ========= POS TAGGING ========= \n")
telugu_tags = get_pos_tagging(tel_tag_dict, input_string)
print(telugu_tags)
print("\n")
hindi_tags = get_pos_tagging(hin_tag_dict, returned_line)
print(hindi_tags)
# print("\n =============================== \n")


print("\n\n ============= Identify NER ===============\n")
ner_one = identify_ner_rule_one(input_string)
print(ner_one)
print("\n")
ner_two = identify_ner_rule_two(input_string)
print(ner_two)
# print("\n =================================== \n")

seq_of_words = []
for word in input_string.split(" "):
    for k in tokens_of_word(word):
        seq_of_words.append(k)

# print(seq_of_words)
output_seq = []
for i, word in enumerate(seq_of_words):
    if word in ner_one:
        output_seq.append(word)
    elif word in ner_two:
        output_seq.append(word)
    else:
        found_similar = False
        for te_arr in telugu_tags:
            if te_arr[0] == word:
                for hi_arr in hindi_tags:
                    if hi_arr[1] == te_arr[1]:
                        output_seq.append(hi_arr[0])
                        found_similar = True
                        break
        if not found_similar:
            if i < len(returned_line_seq):
                output_seq.append(returned_line_seq[i])
            else:
                output_seq.append("__")

output_str = ""
for obj in output_seq:
    output_str += obj + " "

print("\n\n ============= Predicted OUTPUT ================ \n")
print(output_str)




################### unsupervised learning - using k-means clustering #####################

# unsupervised.main("telugu", input_string)



