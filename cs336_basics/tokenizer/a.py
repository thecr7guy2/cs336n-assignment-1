
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
    popular_pair = max(pairs,key=pairs.get)
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


def get_merges(text_in_bytes,index2rep,max_merges=None):
    merges = []
    if max_merges is None:
        max_merges = float("inf")
    while(True):
        pairs = form_pairs(text_in_bytes)
        popular_pair,count = get_popular_pair(pairs)
        if count > 1 and len(merges) < max_merges:
            merges.append(popular_pair)
            new_text =  replace_popular_pair(text_in_bytes,popular_pair,index2rep)
            index2rep = index2rep + 1
            text_in_bytes = new_text
        else:
            break 
    
    return merges

def get_ranks(merges):
    merges_rank = {}
    pair_to_id = {}
    id_to_pair = {}

    for i,j in enumerate(merges):
        merges_rank[j] = i
        pair_to_id[j] = 257 + i
        id_to_pair[257+i] = j

    return merges_rank,pair_to_id,id_to_pair

def training(training_text:str):
    text_in_bytes = list(training_text.encode("utf-8"))
    merges = get_merges(text_in_bytes,257)
    a,b,c = get_ranks(merges)
    return merges,a,b,c


def encode(text:str,merges_rank,pair_to_id) -> list:
    text_in_bytes = list(text.encode("utf-8"))
    while(True):
        pairs = form_pairs(text_in_bytes)
        for i in merges_rank.keys():
            if i in pairs:
                lowest_rank = i
                index2rep = pair_to_id[lowest_rank]
                new_text = replace_popular_pair(text_in_bytes,lowest_rank,index2rep)
                text_in_bytes = new_text
                break
        else:
            return text_in_bytes
        
def decode(encoded_list:list,id_to_pair:dict) -> str :
    i = 0
    while(i<len(encoded_list)-1):
        if encoded_list[i] > 256:
            encoded_list[i:i+1] = list(id_to_pair[encoded_list[i]])
        if encoded_list [i] <= 256:
            i = i+1
    return bytes(encoded_list).decode("utf-8")


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
    training_text = "aaaaaaaabbbabcbababbab"






    
    merges,merge_rank,pair_to_id,id_to_pair = training(training_text)
    c = encode("aaabcbcndhbb",merge_rank,pair_to_id)
    print(c)
    print(id_to_pair)
    d = decode(c,id_to_pair)
    print(d)
    # a = [1,2,3]
    # b = form_pairs(a)
    # print(b)
    



main()
