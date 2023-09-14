  __  __            _     _              _____                    _       _   _             
 |  \/  | __ _  ___| |__ (_)_ __   ___  |_   _| __ __ _ _ __  ___| | __ _| |_(_) ___  _ __  
 | |\/| |/ _` |/ __| '_ \| | '_ \ / _ \   | || '__/ _` | '_ \/ __| |/ _` | __| |/ _ \| '_ \ 
 | |  | | (_| | (__| | | | | | | |  __/   | || | | (_| | | | \__ \ | (_| | |_| | (_) | | | |
 |_|  |_|\__,_|\___|_| |_|_|_| |_|\___|   |_||_|  \__,_|_| |_|___/_|\__,_|\__|_|\___/|_| |_|


Methods Implemented:
    Data Collection (Parallel corpus)
    Tokenization
    Creating Inverted Index
    Calculating most probable sentence
    POS Tagging (Parts of Speech)
    Identifying NER (Named Entity Recognition)
    Output Generater Model (uses POS tagging and NER recognition)

Running:
    Command:
        $> python indexer.py "input-telugu-sequence"
    Flow:
        - Creating tokens out of parallel corpus
        - Creating inverted index for tokens and document-ids
        - Calculating most probable hindi sentence
        - Calculating pos tags for input telugu sentence
        - Identifying ner (rule 1, rule 2) for input telugu sentence
        - Generating output using model based on ner and pos tagging
