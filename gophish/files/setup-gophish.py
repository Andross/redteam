#!/usr/bin/env python3
import requests, re, urllib, html, secrets, string
import traceback, os, json
# def get_first_csrf_token():
#     headers = {}
#     r = requests.get('https://localhost:3333/', verify=False)
proxies = {
              "http"  : "http://192.168.42.120:8080",
              "https" : "http://192.168.42.120:8080"
            }

def import_email_templates(url, cookies, api_key):
    import os
    # assign directory
    directory = 'email_templates'
    
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            name = f.split("/")
            file = open(f, mode='r')
            print(f)
            html = file.read()
            #.replace("\n",r'\\n').replace("           ","\t").replace('\t','\\t').replace('   ','\t')
            enc_html = html.replace('"',"\\\"").encode('utf-8')
            dec_html = enc_html.decode('utf-8')
            subject = name
            import_email_template(url, cookies, api_key, dec_html, name, subject, "kyle@moveworks.co")

def import_email_template(url, cookies, api_key, template_html, name, subject, sender):
    try:
        data = json.loads('{{"attachments":[],"name":"{name}","subject":"{subject}","envelope_sender":"{sender}","html":"{template_html}","text":""}}'.format(name=name[1], subject=subject[1].replace(".html",""), sender=sender, template_html=template_html), strict=False)
        headers = {"Content-Type":"application/json", "Authorization" : "Bearer {api_key}".format(api_key=api_key)}
        r = requests.post(url, cookies=cookies, json=data, headers=headers, verify=False)
        if r.status_code == 201:
            print("Successfully imported template {name}".format(name=name))

    except Exception:
        print(traceback.format_exc())

def get_api_key(url, cookies):

    r = requests.get(url, cookies=cookies, verify=False)
    # print(r.content)
    result = re.search(': "(.*)",', str(r.content))
    api_key = result.group(1)
    print(api_key)

    return api_key

def get_session_cookies(url, cookies, csrf_token, password):
    try:
        convert_csrf_token = html.unescape(csrf_token)
        encoded_csrf_token = urllib.parse.quote_plus(convert_csrf_token)
        body = 'username=admin&password={password}&csrf_token={csrf_token}'.format(password=password, csrf_token=encoded_csrf_token)
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        r = requests.post(url, headers=headers, cookies=cookies, data=body,  allow_redirects=False, verify=False)

        cookies = update_cookies(cookies, r.cookies)
        print(cookies)
        r = requests.get('https://localhost:3333/', cookies=cookies, headers=headers, verify=False)
        # print(r.content)
        # csrf_token, cookies = get_csrf_token(r, cookies)
        # print("Cookies %s" %cookies)
    except Exception as e:
        print(e)

def change_password(url, cookies, csrf_token, new_password):
    try:
        convert_csrf_token = html.unescape(csrf_token)
        encoded_csrf_token = urllib.parse.quote_plus(convert_csrf_token)
        print(cookies)
        body = 'password={new_password}&confirm_password={new_password}&csrf_token={csrf_token}'.format(new_password=new_password, csrf_token=encoded_csrf_token)
        headers = {"Content-Type":"application/x-www-form-urlencoded"}
        r = requests.post(url, headers=headers, cookies=cookies, data=body, verify=False)
        # print(r.content)
        # for c in r.cookies:
        #     cookies[c.name] = c.value
        
        # print("Cookies %s" %cookies)
    except Exception as e:
        print(e)

def update_cookies(cookies_dict, req_cookies):
    try:
        for c in req_cookies:
            cookies_dict[c.name] = c.value
        
        return cookies_dict
    except Exception:
        print(traceback.format_exc())

def get_csrf_token(r, cookies):
    result = re.search('name="csrf_token" value="(.*)" />', str(r.content))
    cookies = update_cookies(cookies, r.cookies)
            # print(cookies)
    print(cookies)

    csrf_token = result.group(1)
    return csrf_token, cookies



def main ():

    import requests, re
    try:
        pattern = re.compile("^[0-9a-z]{16}\"$")
        with open("/go/gophish.log", "r+") as log_file:
            for lines in log_file:
                words = lines.split(" ")
                for word in words:
                    # print(word)
                    if pattern.match(word):
                        password = word.replace("\"","").rstrip()
                        url = 'https://localhost:3333/login?next=%2F'
                        r = requests.get(url,verify=False)
                        cookies = {}
                        csrf_token, cookies = get_csrf_token(r, cookies)
                        get_session_cookies(url, cookies, csrf_token, password)
                        url = 'https://localhost:3333/reset_password?next=%2F'
                        alphabet = string.ascii_letters + string.digits + '!@#$%^&*()'
                        new_password = ''.join(secrets.choice(alphabet) for i in range(32))
                        url_enc_new_pw = urllib.parse.quote_plus(new_password)
                        change_password(url, cookies, csrf_token, url_enc_new_pw)
                        with open('password.txt', 'a+') as the_file:
                            the_file.write(new_password + "\n")

                        url = 'https://localhost:3333/settings'
                        api_key = get_api_key(url, cookies)
                        url = 'https://localhost:3333/api/templates/'
                        import_email_templates(url, cookies, api_key)
                        
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()