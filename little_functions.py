def information_extractor(name):
    text = open("static/text_data/" + name,"r").read()
    return text.split("\n/*/\n")
