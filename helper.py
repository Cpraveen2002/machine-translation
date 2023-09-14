import codecs
import os
import sys

tags = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25']
clusters = ['NN', 'NST', 'NNP', 'PRP', 'DEM', 'VM', 'VAUX', 'JJ', 'RB', 'PSP', 'RP', 'CC', 'WQ', 'QF', 'QC', 'QO', 'CL', 'INTF', 'INJ', 'NEG', 'UT', 'SYM', 'COMP', 'RDP', 'ECH', 'UNK']

def max_connect(x, y, viterbi_matrix, emission, transmission_matrix):
	max = -99999
	path = -1
	
	for k in range(len(tags)):
		val = viterbi_matrix[k][x-1] * transmission_matrix[k][y]
		if val * emission > max:
			max = val
			path = k
	return max, path

def main(language, input_string):

	exclude = ["<s>", "</s>", "START", "END"]

	filepath = ["./data/hindi_training_unsupervised.txt", "./data/telugu_training_unsupervised.txt"]
	if language == "telugu":
		file_path = filepath[1]
	else:
		file_path = filepath[0]
	
	# languages = ["hindi", "telugu", "kannada", "tamil"]
	f = codecs.open(file_path, 'r', encoding='utf-8')
	file_contents = f.readlines()

	wordtypes = []
	tagscount = []

	for x in range(len(tags)):
		tagscount.append(0)

	for x in range(len(file_contents)):
		line = file_contents.pop(0).strip().split(' ')
		for i, word in enumerate(line):
			if i == 0:
				if word not in wordtypes and word not in exclude:
					wordtypes.append(word)
			else:
				if word in tags and word not in exclude:
					tagscount[tags.index(word)] += 1
	f.close()
		
	emission_matrix = []
	transmission_matrix = []
			
	for x in range(len(tags)):
		emission_matrix.append([])
		for y in range(len(wordtypes)):
			emission_matrix[x].append(0)

	for x in range(len(tags)):
		transmission_matrix.append([])
		for y in range(len(tags)):
			transmission_matrix[x].append(0)


	f = codecs.open(file_path, 'r', encoding='utf-8')
	file_contents = f.readlines()

	row_id = -1
	for x in range(len(file_contents)):
		line = file_contents.pop(0).strip().split(' ')

		if line[0] not in exclude and len(line) >= 2:
			col_id = wordtypes.index(line[0])
			prev_row_id = row_id
			row_id = tags.index(line[1])
			emission_matrix[row_id][col_id] += 1
			if prev_row_id != -1:
				transmission_matrix[prev_row_id][row_id] += 1
		else:
			row_id = -1
					
	for x in range(len(tags)):
		for y in range(len(wordtypes)):
			if tagscount[x] != 0:
				emission_matrix[x][y] = float(emission_matrix[x][y]) / tagscount[x]

	for x in range(len(tags)):
		for y in range(len(tags)):
			if tagscount[x] != 0:
				transmission_matrix[x][y] = float(transmission_matrix[x][y]) / tagscount[x]

	# testpath = test_file_path
	# file_test = codecs.open(testpath, 'r', encoding='utf-8')

	# test_input = file_test.readlines()
	test_input = [input_string]
	test_words = []
	pos_tags = []

	# file_output = codecs.open("./output/"+ language+"_tags_unsupervised.txt", 'w', 'utf-8')
	# file_output.close()

	return_string = ""

	for j in range(len(test_input)):
		
		test_words = []
		pos_tags = []

		line = test_input.pop(0).strip().split(' ')
		
		for word in line:
			test_words.append(word)
			pos_tags.append(-1)

		viterbi_matrix = []
		viterbi_path = []
		
		for x in range(len(tags)):
			viterbi_matrix.append([])
			viterbi_path.append([])
			for y in range(len(test_words)):
				viterbi_matrix[x].append(0)
				viterbi_path[x].append(0)

		for x in range(len(test_words)):
			for y in range(len(tags)):
				if test_words[x] in wordtypes:
					word_index = wordtypes.index(test_words[x])
					tag_index = tags.index(tags[y])
					emission = emission_matrix[tag_index][word_index]
				else:
					emission = 0.001

				if x > 0:
					max, viterbi_path[y][x] = max_connect(x, y, viterbi_matrix, emission, transmission_matrix)
				else:
					max = 1
				viterbi_matrix[y][x] = emission * max

		maxval = -999999
		maxs = -1
		for x in range(len(tags)):
			if viterbi_matrix[x][len(test_words)-1] > maxval:
				maxval = viterbi_matrix[x][len(test_words)-1]
				maxs = x
			
		for x in range(len(test_words)-1, -1, -1):
			pos_tags[x] = maxs
			maxs = viterbi_path[maxs][x]

		# print pos_tags
			
		# file_output = codecs.open("./output/"+ language +"_tags_unsupervised.txt", 'a', 'utf-8')
		# for i, x in enumerate(pos_tags):
		# 	file_output.write(test_words[i] + "_" + tags[x] + " ")
		# file_output.write(" ._.\n")

		for i, x in enumerate(pos_tags):
			# return_string += test_words[i] + "_" + clusters[x] + " \n"
			return_string += test_words[i] + "_" + tags[x] + " \n"

	f.close()
	# file_output.close()

	# print("Kindly check ./output/" + language + "_tags_unsupervised.txt file for POS tags.")
	return return_string

