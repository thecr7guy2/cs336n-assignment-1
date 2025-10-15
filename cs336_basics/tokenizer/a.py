
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
        pair_to_id[j] = 256 + i
        id_to_pair[256+i] = j

    return merges_rank,pair_to_id,id_to_pair

def training(training_text:str):
    text_in_bytes = list(training_text.encode("utf-8"))
    merges = get_merges(text_in_bytes,256)
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
    while(i<len(encoded_list)):
        if encoded_list[i] > 255:
            encoded_list[i:i+1] = list(id_to_pair[encoded_list[i]])
        if encoded_list [i] <= 255:
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
    training_text = '''తెలుగు తెలంగాణ, ఆంధ్ర రాష్ట్రాలలోని అధికారిక భాష. ఇది ద్రావిడ భాషా కుటుంబానికి చెందిన భాష. భారతదేశంలో ఒకటి కంటే ఎక్కువ రాష్ట్రాలలో మాటలాడే అధికారిక భాషలలో హిందీ, బెంగాలీలతో పాటు తెలుగు ఒకటి.[5][6] 
    పుదుచ్చేరిలోని యానం జిల్లాలో కూడా తెలుగు అధికారిక భాష. ఒడిశా, కర్ణాటక, తమిళనాడు, కేరళ, పంజాబ్, ఛత్తీస్‌గఢ్, మహారాష్ట్ర, అండమాన్ నికోబార్ దీవులలో గుర్తింపబడిన ద్వితీయ అధికారిక భాష. భారత ప్రభుత్వం భారతదేశ ప్రాచీన భాషలుగా గుర్తించిన ఆరుభాషలలో తెలుగు ఒకటి.[7][8]
    ఇంచుమించుగా తెలుగులో 10,000 శాసనాలు పైనే ఉన్నాయి.భారతదేశం ఎటువంటి ఊడఁడ లేకుండా రెండువేల పైనాటినుండే తెలుగు మాట్లాడ్తున్నట్టుగా తెలియజేయబడింది, 2011 జనాభా లెక్కబట్టి దాదాపు 8.2 కోట్ల మందికి పైగ ఇప్పుడు మాట్లాడేవారున్నారు.[9] భారతదేశంలో మాతృభాషగా తెలుగు నాలుగో స్థానంలో ఉండగా, ప్రపంచంలో 15వ స్థానంలో ఉంది.[10][11] 
    ఇది ద్రావిడభాషా కుటుంబంలో ఎక్కువమంది మాట్లాడే భాష. భారతదేశంలో ఇరవైరెండు షెడ్యూల్ భాషలలో ఇది ఒకటి.[12] ఇది అమెరికాలో వేగంగా పెంపొందుతున్న భాష.[13] 
    తెలుగు భాషలో సుమారు 10,000 పాత శాసనాలు ఉన్నాయి.[14] కన్నడిగుడైన శ్రీకృష్ణదేవరాయలు తెలుగు భాషని 'దేశ భాషలందు తెలుగు లెస్స' అని పొగిడారు.
    '''
    
    
    merges,merge_rank,pair_to_id,id_to_pair = training(training_text)
    c = encode("సాయి మంచి అబ్బాయి.",merge_rank,pair_to_id)
    # print(c)
    print(id_to_pair)
    d = decode(c,id_to_pair)
    print(d)
    # a = [1,2,3]
    # b = form_pairs(a)
    # print(b)
    



main()
