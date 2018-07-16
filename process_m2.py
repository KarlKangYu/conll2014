#!/usr/bin/python3
import sys

original_sentences = []
corrected_sentences = []

original_sentences_with_unchanged = []
corrected_sentences_with_unchanged = []


def read_m2_file(file_path):
    file = open(file_path, 'r', encoding="utf-8")
    return file.readlines()

def get_ori_length(corrected_word_index):
    res = 0
    for i in corrected_word_index:
        if i != -1:
            res += 1
    return res

def get_modified_wordlist(word_list, word_index, action_list):
    corrected_word_list = word_list[:]
    corrected_word_index = word_index[:]
    for action in action_list:
        elems = action.split("|||")
        start, end = [int(i) for i in elems[0].split(" ")]
        change_to_word = elems[2]
        if start == end:
            if start == get_ori_length(corrected_word_index):
                corrected_word_index.append(-1)
                corrected_word_list.append(change_to_word)
            else:
                index = corrected_word_index.index(start)
                corrected_word_index.insert(index, -1)
                corrected_word_list.insert(index, change_to_word)
        else:
            index = corrected_word_index.index(start)
            corrected_word_list[index] = change_to_word
            for i in range(index + 1, index + (end - start)):
                corrected_word_list[i] = ""
    return corrected_word_list


def put_result(word_list, corrected_word_list):
    original_sentence = " ".join(word_list)
    corrected_sentence = " ".join([i for i in corrected_word_list if i != ""])
    if original_sentence != corrected_sentence:
        original_sentences.append(original_sentence)
        corrected_sentences.append(corrected_sentence)
    original_sentences_with_unchanged.append(original_sentence)
    corrected_sentences_with_unchanged.append(corrected_sentence)


def process_lines(lines):
    count = 0
    word_list = []
    word_index = []
    action_list = []
    pre_user = -1
    is_changed = False
    for line in lines:
        count += 1
        # try:
        line = line.strip('\n')
        if len(line) == 0:
            if pre_user != -1:
                corrected_word_list = get_modified_wordlist(word_list, word_index, action_list)
                is_changed = True
                put_result(word_list, corrected_word_list)
                action_list.clear()
                pre_user = -1
        elif line[0] == "S":
            if is_changed is False and len(word_list) != 0:
                put_result(word_list, word_list)
            is_changed = False
            word_list = line[2:].split(" ")
            word_index = [_ for _ in range(len(word_list))]
        elif line[0] == "A":
            if line[2:7] == "-1 -1":
                if pre_user != -1:
                    corrected_word_list = get_modified_wordlist(word_list, word_index, action_list)
                    put_result(word_list, corrected_word_list)
                    is_changed = True
                    action_list.clear()
                    pre_user = -1
                else:
                    pre_user = -1

            elif pre_user == -1:
                action_list.append(line[2:])
                pre_user = int(line.split('|')[-1])
            elif int(line.split('|')[-1]) == pre_user:
                action_list.append(line[2:])
            else:
                corrected_word_list = get_modified_wordlist(word_list, word_index, action_list)
                put_result(word_list, corrected_word_list)
                is_changed = True
                action_list.clear()
                action_list.append(line[2:])
                pre_user = int(line.split('|')[-1])
        # except Exception:
        #     print(count)
        #     break


def write_result_to_file(output_path):
    file1 = open(output_path + "/correction_only.out", "w")
    for i in range(len(original_sentences)):
        line = original_sentences[i] + "\t" + corrected_sentences[i] + "\n"
        file1.write(line)
    file1.close()
    file2 = open(output_path + "/correction_with_unchanged_sentences.out", "w")
    for i in range(len(original_sentences_with_unchanged)):
        line = original_sentences_with_unchanged[i] + "\t" + corrected_sentences_with_unchanged[i] + "\n"
        file2.write(line)
    file2.close()


if __name__ == '__main__':
    m2_file_path = sys.argv[1]
    output_path = sys.argv[2]
    # m2_file_path = "/Users/xinmei/Downloads/m2/conll14st-preprocessed.m2"
    # output_path = "/Users/xinmei/Downloads/m2"

    lines = read_m2_file(m2_file_path)

    process_lines(lines)

    write_result_to_file(output_path)
