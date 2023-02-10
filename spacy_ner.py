import spacy

model = spacy.load("en_core_web_md") #medium model, the small model's suffix is sm and the large is lg

def is_entity(string): #returns the entity type of a single word if the model thinks it is an entity, otherwise returns false
    entities = list(model(string).ents)

    if len(entities) > 0:
        return str(entities[0].label_)
    
    return False