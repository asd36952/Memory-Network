import util
import os

if __name__=="__main__":

    #util.all_word_to_one("/home/asd36952/exobrain/data/wikipedia/morp_lemma_only/","/home/asd36952/exobrain/data/wikipedia/all_morp_lemma_only.txt")
    util.all_word_to_one("/home/asd36952/exobrain/data/wikipedia/morp_lemma_type/","/home/asd36952/exobrain/data/wikipedia/all_morp_lemma_type.txt")
    util.all_word_to_one("/home/asd36952/exobrain/data/query/morp_lemma_only/","/home/asd36952/exobrain/data/query/all_morp_lemma_only.txt")
    util.all_word_to_one("/home/asd36952/exobrain/data/query/morp_lemma_type/","/home/asd36952/exobrain/data/query/all_morp_lemma_type.txt")
    exit()
    count=0
    unicode_error_list=[]
    other_error_list=[]
    for file_name in os.listdir("../data/wikipedia/preprocessed/"):
        print(file_name)
        try:
            util.extract_morp(file_name,"../data/wikipedia/preprocessed/","../data/wikipedia/morp_lemma_only/","../data/wikipedia/morp_lemma_type/")
        except UnicodeDecodeError:
            unicode_error_list.append(file_name)
        except:
            other_error_list.append(file_name)
        count+=1
        print(count)
    print(len(unicode_error_list))
    print(len(other_error_list))
    exit()

    count=0
    unicode_error_list=[]
    other_error_list=[]
    for file_name in os.listdir("../data/query/preprocessed/"):
        print(file_name)
        try:
            util.extract_morp(file_name,"../data/query/preprocessed/","../data/query/morp_lemma_only/","../data/query/morp_lemma_type/")
        except UnicodeDecodeError:
            unicode_error_list.append(file_name)
        except:
            other_error_list.append(file_name)
        count+=1
        print(count)
    print(unicode_error_list)
    print(other_error_list)
    exit()
    count=0
    unicode_error_list=[]
    other_error_list=[]
    for file_name in os.listdir("../data/wikipedia/preprocessed/"):
        print(file_name)
        try:
            util.extract_morp(file_name)
        except UnicodeDecodeError:
            unicode_error_list.append(file_name)
        #except:
        #    other_error_list.append(file_name)
        count+=1
        print(count)
    print(len(unicode_error_list))
    print(len(other_error_list))
    exit()
    
    
    for elem in util.load_stories():
        print(elem)
        input()
    exit()
    


    content=util.read_file("0003694_결박된 프로메테우스(본문).txt")
    title,text=util.process_content(content)
    print("title:",title)
    print("text:",text)
    exit()
    util.load_query()
    exit()
