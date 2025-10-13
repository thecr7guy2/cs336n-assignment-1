
[0,1,2,3,4,5]
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


def get_merges(text_in_bytes,index2rep):
    merges = []
    while(True):
        pairs = form_pairs(text_in_bytes)
        popular_pair,count = get_popular_pair(pairs)
        if count > 1:
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
    encoded_list = []
    text_in_bytes = list(text.encode("utf-8"))
    i =0 
    while(i<len(text_in_bytes)):
        if i< len(text_in_bytes)-1:
            pair = text_in_bytes[i],text_in_bytes[i+1]
            if pair in merges_rank:
                encoded_list.append(pair_to_id[pair])
                i = i + 2
            else:
                encoded_list.append(text_in_bytes[i])
                i = i + 1 
        else:
            encoded_list.append(text_in_bytes[i])
            i = i + 1


def main():
    training_text = '''
           You will require prior written permission for the reimbursement of ambulance transport in these 2 situations:
           transport over a distance of more than 200 km
           transport by any mode of transport other than an ambulance
           Consent is not required in the case of unforeseen care that cannot reasonably be postponed.
           A request for transport should include a report from the treating doctor, including the medical diagnosis/diagnoses, a description of the current problem and substantiation of the request. Please send requests for permission to:
        '''
    
    merges,a,b,c = training(training_text)
    



main()