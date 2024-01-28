from emailSender.settings import EMAIL_HOST_USER, BASE_DIR
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
import os
from django.http import JsonResponse
from cryptography.fernet import Fernet
from urllib.parse import quote, unquote



def encrypt_text(request,text,key=""):
    key = Fernet.generate_key() if key == "" else key
    cipher_suite = Fernet(key)
    # Encrypt the text
    encrypted_text = cipher_suite.encrypt(text.encode('utf-8'))
    return JsonResponse({"cipher":encrypted_text,"key":key})

'''

def decrypt_text(encrypted_text,key):
    # Decrypt the text
    print("Encrypted Text in Decryption Function",encrypt_text)
    print("KEY",key)
    cipher_suite = Fernet(key)
    decrypted_text = cipher_suite.decrypt(encrypted_text).decode('utf-8')
    print("Decrypted one ",decrypt_text)
    return decrypted_text

'''

def Invite_Faculty(request,id,name,email):
    path = "invitation.html"
    response = send_mail("Welcome to Sri Vasavi Engineering College",strip_tags(render_to_string(path,{'id':id,'name':name,'email':email})),EMAIL_HOST_USER,[email],fail_silently=False)
    return JsonResponse({"status":response})

def Password_Reset_Initiator(request,id,email):
    path = os.path.join(BASE_DIR, "templates\\reset.html")
    cipher,key = encrypt_text(id)
    cipher = quote(cipher)
    response = send_mail("Password Reset - Sri Vasavi Engineering College",strip_tags(render_to_string(path,{'id':id, 'cipher':cipher})),EMAIL_HOST_USER,[email],fail_silently=False)
    return JsonResponse({"status":response,"key":cipher})

'''

def Password_Resetter(request,cipher):
    print(cipher)
    cipher = unquote(cipher)
    print(cipher)
    text = decrypt_text(cipher, request.session["KEY"].encode('utf-8'))
    if request.method == "POST":
        # Step 1: Define the API endpoint of the JSON server
        json_server_url = 'http://localhost:3001/FACULTY'

        # Step 2: Make a GET request to fetch the current data
        response = requests.get(json_server_url)
        
        if response.status_code == 200:
            # Step 3: Load the current data
            data = response.json()

            for faculty in data:
                if faculty["ID"] == text:
                    faculty["PASSWORD"] = request.POST["pswd"]

            # Step 5: Make a PUT request to update the data on the JSON server
            print(data)
            update_response = requests.put(json_server_url, data=json.dumps(data), headers={'Content-Type':'application/json'})
            print(update_response)

            if update_response.status_code == 200:
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Failed to update data on the JSON server'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Failed to fetch current data from the JSON server'})
    return render(request,"form.html", {"text":text})

'''
