import regex as re 

def form_pairs(text_in_bytes):
    pairs={}
    for i in range(0,len(text_in_bytes)-1):
        pair = (text_in_bytes[i],text_in_bytes[i+1])
        if pair in pairs:
            pairs[pair] = pairs[pair] + 1
        else:
            pairs[pair] = 1 
    return pairs

def get_popular_pair(pairs):
    popular_pair = max(pairs, key=lambda p: (pairs[p], p)) #chatgpt this - gives the best lexicographic pair.
    return popular_pair,pairs[popular_pair]

def replace_popular_pair(text_in_bytes,popular_pair,index2rep):
    new_text = []
    i = 0
    while (i < len(text_in_bytes)):
        if (i < len(text_in_bytes) -1):
            if text_in_bytes[i] == popular_pair [0] and text_in_bytes[i+1] == popular_pair [1] :
                new_text.append(index2rep)
                i = i + 2
            else:
                new_text.append(text_in_bytes[i])
                i = i + 1
        else:
            new_text.append(text_in_bytes[i])
            i = i + 1
    return new_text

def get_ranks(merges):
    merges_rank = {}
    pair_to_id = {}
    id_to_pair = {}

    for i,j in enumerate(merges):
        merges_rank[j] = i
        pair_to_id[j] = 256 + i
        id_to_pair[256+i] = j

    return merges_rank,pair_to_id,id_to_pair


def form_vocab(merges):
    vocab = {}
    for i in range(0,256):
        vocab[i] = bytes([i])
    for i,(a,b) in enumerate(merges):
        vocab[256+i] = vocab[a] + vocab[b]
    return vocab

def frequency_dict(pretok_list):
    freq_dict = {}
    for i in pretok_list:
        if i in freq_dict.keys():
            freq_dict[i] = freq_dict[i] + 1 
        else:
            freq_dict[i]= 1
    return freq_dict

def byte_seq_freq(freq_dict):
    lst = [] 
    for i in freq_dict.keys():
        lst.append((list(i.encode("utf-8")),freq_dict[i]))
    return lst

def get_weighted_pairs(byte_freq_dict):
    weighted_pairs = {}
    for i in byte_freq_dict:
        pairs = form_pairs(i[0])
        for j in pairs.keys():
            if j in weighted_pairs:
                weighted_pairs[j] = weighted_pairs[j] + pairs[j] * i[1]
            else:
                weighted_pairs[j] = pairs[j] * i[1]
    return weighted_pairs


def pre_token_merge(pair,byte_freq_lst,index2rep):
    after_merge_list = []
    for i in  range  (0,len(byte_freq_lst)):
        b = replace_popular_pair(byte_freq_lst[i][0],pair,index2rep)
        after_merge_list.append((b,byte_freq_lst[i][1]))
    return after_merge_list


def pretok_train(training_text,max_merges=None,index2rep=256):
    pretok_list= training_text.split(" ")
    freq_dict = frequency_dict(pretok_list)
    byte_freq_lst= byte_seq_freq(freq_dict)
    print(byte_freq_lst)
    merges = []
    if max_merges is None:
        max_merges = float("inf")
    while(True):
        wp_dict = get_weighted_pairs(byte_freq_lst)
        if not wp_dict:
            break
        popular_pair,count = get_popular_pair(wp_dict)
        if count > 1 and len(merges) < max_merges:
            merges.append(popular_pair)
            new_text = pre_token_merge(popular_pair,byte_freq_lst,index2rep)
            index2rep = index2rep + 1
            byte_freq_lst = new_text
        else:
            break

    merges_rank,pair_to_id,id_to_pair = get_ranks(merges)
    vocab=form_vocab(merges)
    return merges,byte_freq_lst,merges_rank,pair_to_id,id_to_pair,vocab


def decode(encoded_list:list,vocab:dict) -> str :
    tokens= []
    for i in range (0,len(encoded_list)):
        if i in vocab.keys():
            tokens.append(vocab[encoded_list[i]])
        else:
            continue
    tokens = b"".join(tokens)
    return tokens.decode("utf-8")

def pre_tok_encode(text:str,merges_rank,pair_to_id) -> list:
    encoded_list = []
    pretok_list= text.split(" ")
    for i in pretok_list:
        text_in_bytes = i.encode("utf-8")
        while(True):
            pairs = form_pairs(text_in_bytes)
            for j in merges_rank.keys():
                if j in pairs:
                    index2rep = pair_to_id[j]
                    new_text = replace_popular_pair(text_in_bytes,j,index2rep)
                    text_in_bytes = new_text
                    break
            else:
                break
        encoded_list.extend(text_in_bytes)

    return encoded_list
# Same as get popular pair but here we have to add the logic of picking the 

    # while(i<len(text_in_bytes)):
    #     if i< len(text_in_bytes)-1:
    #         pair = text_in_bytes[i],text_in_bytes[i+1]
    #         if pair in merges_rank:
    #             encoded_list.append(pair_to_id[pair])
    #             i = i + 2
    #         else:
    #             encoded_list.append(text_in_bytes[i])
    #             i = i + 1 
    #     else:
    #         encoded_list.append(text_in_bytes[i])
    #         i = i + 1


def main():
    training_text = '''low low low low low lower lower widest widest widest newest newest newest newest newest newest'''
    gpt2pat =  r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""

    merges,byte_freq_lst,merges_rank,pair_to_id,id_to_pair,vocab = pretok_train(training_text,index2rep=256)
    # a = pretok_train(training_text,max_merges=None,index2rep=256)

    print(merges)
    print(byte_freq_lst)
    print(vocab)

    text = "I am wearing a new watch which is low on my hand"

    encoded_text = pre_tok_encode(text,merges_rank,pair_to_id)

    print(encoded_text)

    decoded_text = decode(encoded_text,vocab)

    print(decoded_text)

    
main()
