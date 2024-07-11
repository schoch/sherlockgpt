import json

def clean_chat(chat):
    if (len(chat)<=0):
        return []
    
    result = []
    for message in chat[1:]:
        text = message["content"]
        sender = "character" if message["role"] == "system" else "user"
        result.append({"text": text, "sender": sender})

    return result
