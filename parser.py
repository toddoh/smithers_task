import spacy
from spacy.lang.en import STOP_WORDS

nlp = spacy.load("en_core_web_sm")
doc = nlp(u"sign up f")
#print(list(doc.noun_chunks))

for noun_phrase in list(doc.noun_chunks):
    noun_phrase.merge(noun_phrase.root.tag_, noun_phrase.root.lemma_, noun_phrase.root.ent_type_)

rootChildren = []
root_token = None
finalRootToken = []
rootSupportToken = []

for token in doc:
    if token.dep_ == "ROOT":
        root_token = str(token.text)
        finalRootToken.append(str(token.text))
        for child in token.children:
            rootChildren.append(str(child))
    
    print(token.text, token.dep_, token.head.text, token.is_stop, token.head.pos_,
            [child for child in token.children])

for token in doc:
    if token.head.text == root_token:
        if token.dep_ == "nsubj" or token.dep_ == "dsubj" or token.dep_ == "nobj" or token.dep_ == "dobj" or token.dep_ == "pobj":
            rootSupportToken.append(token.text)
            for fulltoken in doc:
                if fulltoken.dep_ == "appos" and fulltoken.head.text == token.text:
                    if fulltoken.is_stop is False or fulltoken.dep_ == "aux" or fulltoken.dep_ == "auxpass":
                        rootSupportToken.append(fulltoken.text)

        if token.dep_ == "prt" :
            finalRootToken.append(token.text)

        if token.dep_ == "prep" or token.dep_ == "prepc" or token.dep_ == "nobj" or token.dep_ == "dobj" or token.dep_ == "pobj":
            rootSupportToken.append(token.text)
            for fulltoken in doc:
                if fulltoken.dep_ == "appos" and fulltoken.head.text == t.text:
                    if fulltoken.is_stop is False or fulltoken.dep_ == "aux" or fulltoken.dep_ == "auxpass":
                        rootSupportToken.append(fulltoken.text)
            
    if any(token.text in c for c in rootChildren):
        for t in token.children:
            for fulltoken in doc:
                #if fulltoken.dep_ == "appos" and fulltoken.head.text == t.text:
                if fulltoken.text == t.text:
                    if fulltoken.is_stop is False:
                        rootSupportToken.append(fulltoken.text)


    
print('Dependency: root: {0}, supporting: {1}'.format(root_token, rootSupportToken))