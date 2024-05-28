import time
import shlex
import requests
import pandas as pd
import os

base_url = "https://www.wanted.co.kr"

# alt h o i
def fetch_ids(years):
    global base_url
    # 전체 경력
    if years is None:
        years = 'years=-1'
    else:
        years = f'years=0&years={years}'

    next_url = f"/api/chaos/navigation/v1/results?job_group_id=518&{years}&locations=all&country=kr&job_sort=job.recommend_order"
    ids = []
    cnt = 0
    max_retries = 3  # 최대 재시도 횟수

    while True:
        retry_count = 0  # 현재 재시도 횟수
        while retry_count <= max_retries:
            url = f"{base_url}{next_url}"
            response = requests.get(url)
            if response.status_code == 200:
                break  # 요청이 성공하면 재시도 반복문을 빠져나감
            else:
                print(f"Request failed with status code: {response.status_code}, retrying... ({retry_count+1}/{max_retries})")
                retry_count += 1
                time.sleep(1)  # 재시도 사이에 간단한 대기 시간 추가

        if retry_count > max_retries:
            print("Failed to fetch data after maximum retries.")
            break  # 최대 재시도 횟수를 초과하면 루프를 빠져나감

        # 요청 성공 시 데이터 처리
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



def fetch_detail(id, keyword_groups, current_index, total_jobs):
    global base_url
    current_time_millis = int(time.time() * 1000)
    detail_url = f"{base_url}/api/chaos/jobs/v1/{id}/details?{current_time_millis}="
    result_data = []

    max_retries = 3  # 최대 재시도 횟수
    attempt = 0  # 현재 시도 횟수

    while attempt <= max_retries:
        response = requests.get(detail_url)
        if response.status_code == 200:
            # 요청 성공
            data = response.json()
            break
        else:
            # 요청 실패, 재시도
            print(f"Attempt {attempt+1} failed with status code {response.status_code}. Retrying...")
            attempt += 1
            time.sleep(1)  # 잠시 대기 후 재시도

    if attempt > max_retries:
        # 최대 재시도 횟수 초과
        print(f"Failed to fetch details after {max_retries} retries.")
        return None

    job_detail = data.get('job', {}).get('detail', {})
    company_name = data.get('job', {}).get('company', {}).get('name', '')
    position = job_detail.get('position', '')

    detail_text = " ".join(str(v) for v in job_detail.values()).lower()
    included_keywords = set()
    for keywords in keyword_groups:
        for keyword in keywords:
            if keyword.lower() in detail_text:
                included_keywords.add(keyword)

    if included_keywords:
        job_url = f"https://www.wanted.co.kr/wd/{id}"
        result_data.append({
            'url': job_url,
            'company_name': company_name,
            'position': position,
            'included_keywords': ', '.join(included_keywords)
        })

    progress = (current_index + 1) / total_jobs * 100
    print(f"\rProcessing {current_index + 1}/{total_jobs} (Progress: {progress:.2f}%)", end="")

    return result_data



def read_applied_companies(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        applied_companies = {line.strip() for line in file if line.strip()}
    return applied_companies


def save_to_excel(df, filename_base):
    filename_ext = '.xlsx'
    output_folder = "result"

    output_filename = f"{output_folder}/{filename_base}{filename_ext}"
    counter = 1

    # result 폴더가 없으면 생성
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 파일 이름이 중복되는 경우 새로운 이름을 생성합니다.
    while os.path.isfile(output_filename):
        output_filename = f"{output_folder}/{filename_base} ({counter}){filename_ext}"
        counter += 1

    df.to_excel(output_filename, index=False)
    print(f"\nResults have been saved to {output_filename}")



def main():
    applied_companies = read_applied_companies("./company")

    keyword_groups = []
    group_count = 1

    input_years = input(f"경력 : ")

    while True:
        input_keywords = input(f"Enter keywords {group_count}: ")
        if not input_keywords.strip():
            break

        keywords = [keyword.strip() for keyword in shlex.split(input_keywords.replace(',', ' '))]
        keyword_groups.append(keywords)
        group_count += 1

    job_ids = fetch_ids(input_years)

    results = []
    total_jobs = len(job_ids)
    for index, job_id in enumerate(job_ids):
        result = fetch_detail(job_id, keyword_groups, index, total_jobs)
        if result:
            results.extend(result)

    df_results = pd.DataFrame(results)

    if results:
        df_results = pd.DataFrame(results)

        # 회사 이름으로 결과를 정렬합니다.
        df_results_sorted = df_results.sort_values(by='company_name', ascending=True)

        # 지원하지 않은 회사는 'search_results.xlsx'로, 지원한 회사는 'applied_companies_results.xlsx'로 저장
        df_not_applied = df_results_sorted[~df_results_sorted['company_name'].isin(applied_companies)]
        df_applied = df_results_sorted[df_results_sorted['company_name'].isin(applied_companies)]

        if not df_not_applied.empty:
            save_to_excel(df_not_applied, 'search_results')
        if not df_applied.empty:
            save_to_excel(df_applied, 'applied_companies_results')
    else:
        print("No results to save.")


main()
#Enter keywords 1: 제택, 리모트, 원격, 재택
#Enter keywords 2: 파이썬, 파이선, python, java, 자바, kotlin, 코틀린, spring, 스프링, 쟝고, 장고, django, flask, fastapi