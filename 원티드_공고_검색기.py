import time
import shlex
import requests
import pandas as pd
import os

base_url = "https://www.wanted.co.kr"

#엑셀 자동 맞춤 ALT - H - O - I
def fetch_ids():
    global base_url
    next_url = "/api/chaos/navigation/v1/results?job_group_id=518&years=-1&locations=all&country=kr&job_sort=job.recommend_order"
    ids = []
    cnt = 0

    while True:
        url = f"{base_url}{next_url}"
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Request failed with status code: {response.status_code}")
            break

        data = response.json()
        job_data = data.get('data', [])
        ids.extend([job['id'] for job in job_data])

        links = data.get('links', {})
        next_url = links.get('next')
        if not next_url:
            break

        cnt += 1
        if cnt % 10 == 0:
            print(f"\r{cnt}번 반복됨 ...", end="")
    print()

    return ids


def fetch_detail(id, keywords, current_index, total_jobs):
    global base_url
    current_time_millis = int(time.time() * 1000)
    detail_url = f"{base_url}/api/chaos/jobs/v1/{id}/details?{current_time_millis}="
    result_data = []

    response = requests.get(detail_url)

    if response.status_code != 200:
        print(f"\nRequest failed with status code: {response.status_code}")
        return None

    data = response.json()
    job_detail = data.get('job', {}).get('detail', {})
    company_name = data.get('job', {}).get('company', {}).get('name', '')
    position = job_detail.get('position', '')

    # job.detail 아래에 있는 모든 텍스트를 검색하고, 해당 텍스트에 키워드가 포함되어 있는지 확인합니다.
    detail_text = " ".join(str(v) for v in job_detail.values()).lower()
    included_keywords = [keyword for keyword in keywords if keyword.lower() in detail_text]

    if included_keywords:
        job_url = f"https://www.wanted.co.kr/wd/{id}"
        result_data.append({
            'url': job_url,
            'company_name': company_name,
            'position': position,
            'included_keywords': included_keywords
        })

    # 진행 상황 표시
    progress = (current_index + 1) / total_jobs * 100
    print(f"\rProcessing {current_index + 1}/{total_jobs} (Progress: {progress:.2f}%)", end="")

    return result_data


def main():
    # 사용자로부터 입력을 받습니다.
    input_keywords = input("Enter keywords: ")

    # shlex.split를 사용하여 쉼표와 공백으로 분리하고, 큰따옴표 또는 작은따옴표로 묶인 키워드를 정확하게 처리합니다.
    keywords = [keyword.strip() for keyword in shlex.split(input_keywords.replace(',', ' '))]

    # 리스트
    job_ids = fetch_ids()

    # 검색
    results = []
    total_jobs = len(job_ids)
    for index, job_id in enumerate(job_ids):
        result = fetch_detail(job_id, keywords, index, total_jobs)
        if result:
            results.extend(result)

    # 결과를 pandas 데이터프레임으로 변환합니다.
    df_results = pd.DataFrame(results)

    # 회사 이름으로 결과를 정렬합니다.
    df_results_sorted = df_results.sort_values(by='company_name', ascending=True)

    # 결과를 엑셀 파일로 저장합니다.
    filename_base = 'search_results'
    filename_ext = '.xlsx'
    output_filename = filename_base + filename_ext
    counter = 1

    # 파일 이름이 중복되는 경우 새로운 이름을 생성합니다.
    while os.path.isfile(output_filename):
        output_filename = f"{filename_base} ({counter}){filename_ext}"
        counter += 1

    df_results_sorted.to_excel(output_filename, index=False)
    print(f"\nResults have been saved to {output_filename}")


# main 함수 호출
main()





