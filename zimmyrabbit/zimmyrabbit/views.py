from django.shortcuts import render,redirect
from django.http import HttpResponse
import subprocess
import requests
import base64

def index(request) :
    return render(request, 'jenkins/main.html')


def check_model(request) :
    content = request.POST.get('content')
    scontent = sorted(set(content.split()))
    print(scontent)

    context = {"data": scontent}

    '''
    command = ''
    output = subprocess.check_output(command, shell=True, text=True)

    # 결과 파싱하여 계정, 날짜, 커밋로그 저장
    commits = []
    lines = output.split('------------------------------------------------------------------------')

    accounts = []
    dates = []
    commit_logs = []

    for i in range(1, len(lines)-1):
        line = lines[i].split(" | ")
        account = line[1].strip()
        date = line[2].strip()
        commit_log = line[-1].strip()
        accounts.append(account)
        dates.append(date)
        commit_logs.append(commit_log)

    print("Accounts:", accounts)
    print("Dates:", dates)
    print("Commit Logs:", commit_logs)
    '''
    
    '''
    url = ''
    username = ''
    password = '' #token
    
    # 인증 정보를 Base64로 인코딩하여 헤더에 추가
    auth_header = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}'}
    
    headers['Content-Type'] = 'application/json'
    
    #response = requests.get(url, headers=headers)
    response = requests.post(url, headers=headers)
    
    #200번대는 성공으로 판단
    if response.status_code // 100 == 2:
        url = ''
        response = requests.post(url, headers=headers)

        try:
            response.raise_for_status()
            data = response.json()
            print(data['id'])

            url = ''
            response = requests.post(url, headers=headers)
            print(response.json())
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP 오류 발생: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"요청 오류 발생: {req_err}")
        except requests.exceptions.JSONDecodeError as json_err:
            print(f"JSON 디코드 오류 발생: {json_err}")
    else:
        print(f"API 호출 실패 - 상태 코드: {response.status_code}")
    '''
    return redirect('zimmyrabbit:index')