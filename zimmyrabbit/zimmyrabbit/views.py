from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
import subprocess
import requests
import base64
import json
import time
import os

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from datetime import datetime

from .serializers import BuildHistSerializer
from .models import BuildHist


def index(request) :
    return render(request, 'jenkins/main.html')


def check_model(request) :
    jsonObject = json.loads(request.body)

    content = jsonObject.get('content')
    scontent = sorted(set(content.split()))

    all_contexts = []

    for i in range(0,len(scontent)): 
        app = scontent[i][-2:]
        comp = scontent[i].split("_")[0]
        package = scontent[i].split("_")[1]
        contentUrl = ''
        if app == "xp" :
            contentUrl = f'xpapps/{comp}/{package}'
        else :
            contentUrl = f'components/{comp}/{package}'

        command = os.environ.get("SVN_ADDRESS") + contentUrl + '\"'
        print(command)
        output = subprocess.check_output(command, shell=True, text=True)

        # 결과 파싱하여 계정, 날짜, 커밋로그 저장
        commits = []
        lines = output.split('------------------------------------------------------------------------')

        accounts = []
        dates = []
        commit_logs = []

        for j in range(1, len(lines)-1):
            line = lines[j].split(" | ")
            account = line[1].strip()
            date = line[2].strip()
            commit_log = line[-1].strip()
            accounts.append(account)
            dates.append(date)
            commit_logs.append(commit_log)

        print("Accounts:", accounts)
        print("Dates:", dates)
        print("Commit Logs:", commit_logs)
        
        context = {'account': accounts, 'dates': dates, 'commitLogs' : commit_logs}
        all_contexts.append({'context' : context, 'package' : package})

    return JsonResponse(all_contexts, safe=False)

def request_build(request):
    jsonObject = json.loads(request.body) 

    id = jsonObject.get('id')
    token = jsonObject.get('token')
    build_job = 'lis_' + jsonObject.get('buildJob')
    jenkins_url = f'{os.environ.get("JENKINS_ADDRESS")}{build_job}/build'
    print(f"build url : {jenkins_url}")
    print(f"id : {id}")
    print(f"token : {token}")

    # 인증 정보를 Base64로 인코딩하여 헤더에 추가
    auth_header = base64.b64encode(f"{id}:{token}".encode('utf-8')).decode('utf-8')
    headers = {'Authorization': f'Basic {auth_header}'}
    headers['Content-Type'] = 'application/json'

    response = requests.post(jenkins_url, headers=headers)
    if response.status_code == 201:
        last_build_url = f'{os.environ.get("JENKINS_ADDRESS")}{build_job}/lastBuild/api/json'
        response = requests.get(last_build_url, headers=headers)

        response.raise_for_status()
        data = response.json()

        print(f"빌드 시작. 빌드 번호: {data['id']}")
        build_status = wait_for_build_completion(build_job, data['id'], headers)
        print(f"빌드 완료. 빌드 상태: {build_status}")

        return JsonResponse({'message': '빌드 성공', 'build_number': data['id']})
        
    else:
        print("빌드 실패")

        return JsonResponse({'error': '빌드 실패'})
        

def wait_for_build_completion(build_job, build_number, headers) :
    # 빌드가 완료될 때까지 주기적으로 빌드 상태를 확인하는 함수
    while True:
        build_status = get_build_status(build_job, build_number, headers)
        if build_status is not None:
            return build_status
        time.sleep(5)  # 5초마다 빌드 상태를 확인
    
def get_build_status(build_job, build_number, headers):
    # 빌드 상태 확인을 위한 Jenkins 빌드 정보 API 호출
    api_url = f'{os.environ.get("JENKINS_ADDRESS")}{build_job}/{build_number}/api/json'
    response = requests.get(api_url, headers=headers)
    print(f"get_build_status response.status_code : {response.status_code}")
    if response.status_code == 200:
        build_info = json.loads(response.content.decode())
        return build_info['result']
    return None


#drf class
class BuildHistList(APIView):
    def get(self, request):
        buildHists = BuildHist.objects.all()

        serializer = BuildHistSerializer(buildHists, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = BuildHistSerializer(
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    
class BuildHistDetail(APIView):
    def get_object(self, pk):
        try:
            return BuildHist.objects.get(pk=pk)
        except BuildHist.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        buildHist = self.get_object(pk)
        serializer = BuildHistSerializer(buildHist)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        buildHist = self.get_object(pk)
        serializer = BuildHistSerializer(buildHist, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        buildHist = self.get_object(pk)
        buildHist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)