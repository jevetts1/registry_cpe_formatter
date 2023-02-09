import spacy

model = spacy.load("en_core_web_md")

def is_entity(string):
    entities = list(model(string).ents)

    if len(entities) > 0:
        return str(entities[0].label_)
    
    return False