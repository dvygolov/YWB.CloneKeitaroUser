import requests,json,secrets,string,copy

k_api_key="<YOUR KEITARO'S API KEY>"
k_url="https://<KEITARO'S DOMAIN>"
k_timezone="Europe/Moscow"

def copyright():
    print()
    print("                     Clone Keitaro Users v1.0")
    print("   _            __     __  _ _             __          __  _     ")
    print("  | |           \ \   / / | | |            \ \        / / | |    ")
    print("  | |__  _   _   \ \_/ /__| | | _____      _\ \  /\  / /__| |__  ")
    print("  | '_ \| | | |   \   / _ \ | |/ _ \ \ /\ / /\ \/  \/ / _ \ '_ \ ")
    print("  | |_) | |_| |    | |  __/ | | (_) \ V  V /  \  /\  /  __/ |_) |")
    print("  |_.__/ \__, |    |_|\___|_|_|\___/ \_/\_/    \/  \/ \___|_.__/ ")
    print("          __/ |                                                  ")
    print("         |___/             https://yellowweb.top                 ")
    print()
    print("If you like this script, PLEASE DONATE!")
    print("WebMoney: Z182653170916")
    print("Bitcoin: bc1qqv99jasckntqnk0pkjnrjtpwu0yurm0qd0gnqv")
    print("Ethereum: 0xBC118D3FDE78eE393A154C29A4545c575506ad6B")
    print()

def get_users(session):
    r=session.get(k_url+"users")
    return json.loads(r.text)

def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for i in range(10))
    return password

def create_user(session,user):
    r=session.post(k_url+"users",data=json.dumps(user))
    return json.loads(r.text)['id']

def create_campaign_group(session,uname):
    r=session.post(k_url+"groups",data={"name":uname,"type":"campaigns"})
    return json.loads(r.text)['id']

def update_access(session,user_id,access_data):
    r=session.put(f"{k_url}users/{user_id}/access",data=json.dumps(access_data))
    return json.loads(r.text)['id']

if __name__ == "__main__":
    copyright()
    k_url+="/admin_api/v1/"
    session=requests.session()
    session.headers.update({"Api-Key":k_api_key})
    users=get_users(session)
    list(map(lambda u: print(f"{u[0]}. {u[1]['login']}"),zip(range(1,len(users)),users)))
    uindex=int(input("Select a user to clone:"))-1
    u2clone=users[uindex]
    unames=input("Add new user name or user names delimited by comma:").split(',')
    for uname in unames:
        newuser=copy.copy(u2clone)
        password=generate_password()
        newuser['login']=uname
        newuser['new_password']=password
        newuser['new_password_confirmation']=password
        newuser['preferences']={}
        newuser['preferences']['timezone']=k_timezone
        newuser['preferences']['language']='ru'
        nuaccess=newuser['access_data']
        newuser.pop('access_data')
        newuser.pop('keyCount')
        newuser.pop('id')
        print(uname,password)
        nuid=create_user(session,newuser)
        grid=create_campaign_group(session,uname)
        nuaccess['campaigns_selected_groups']=[grid]
        nuaccess['campaigns_selected_entities']=[]
        nuaccess['landings_selected_entities']=[]
        nuaccess['domains_selected_entities']=[]
        access_data={"access_data":nuaccess}
        update_access(session,nuid,access_data)


