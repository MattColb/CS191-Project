import json
import hashlib
import base64

def jwt_creation(payload):
    header = """{
      "alg": "SHA256",
      "typ": "JWT"
    }"""
    b64_header = base64.b64encode(header.encode()).decode()
    secret_string = "" 
    json_payload = json.dumps(payload).encode()
    b64_json_payload = base64.b64encode(json_payload).decode()
    full_to_encode = b64_header + "." + b64_json_payload + "." + secret_string
    validation = hashlib.sha256(full_to_encode.encode()).hexdigest()
    full_jwt = b64_header + "." + b64_json_payload + "." + validation
    return full_jwt

def jwt_verification_retrieval(event, jwt):
    
    b64_json_payload = jwt.split(".")[1]
    json_payload = base64.b64decode(b64_json_payload)
    valid = jwt.split(".")[2]
    secret_string = ""
    front_piece = jwt.split(".")[0:2].join(".")
    full_to_encode = front_piece + "." + secret_string
    validation = hashlib.sha256(full_to_encode).hexdigest()
    if validation == valid:
        return True, json.loads(json_payload)
    return False, None
