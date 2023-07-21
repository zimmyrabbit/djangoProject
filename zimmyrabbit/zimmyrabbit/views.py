from django.shortcuts import render,redirect
from django.http import HttpResponse
import subprocess

def index(request) :
    return render(request, 'jenkins/main.html')


def check_model(request) :
    content = request.POST.get('content')
    scontent = sorted(set(content.split()))
    print(scontent)

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


    return redirect('zimmyrabbit:index')