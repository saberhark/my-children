import requests
import pandas as pd
from tqdm import tqdm

def main():
    # 사용 예시
    url = "https://career.programmers.co.kr/api/job_positions"
    min_career = 4
    min_salary = 6000
    keywords = ["원격", "리모트", "재택", "제택", "remote"]

    trackable_ids = get_all_trackable_ids(url)
    job_data_list = get_all_job_position_detail(url, trackable_ids, keywords)

    # 데이터프레임 생성
    df = pd.DataFrame(job_data_list)

    # 데이터프레임을 Excel 파일로 저장
    df.to_excel("job_data.xlsx", index=False)


def get_trackable_ids(url, page, min_career=4, min_salary=6000, order="recent"):
    trackable_ids = []

    # 쿼리 파라미터 설정
    params = {
        "min_career": min_career,
        "min_salary": min_salary,
        "order": order,
        "page": page
    }

    response = requests.get(url, params=params)

    # 응답 확인
    if response.status_code == 200:
        # JSON 형식의 응답 데이터를 딕셔너리로 파싱
        data = response.json()

        # trackable_ids 추출
        trackable_ids = [item["id"] for item in data["jobPositions"]]
        total_pages = data["totalPages"]
    else:
        print("요청 실패:", response.status_code)

    return trackable_ids, page, total_pages


def get_all_trackable_ids(url, min_career=4, min_salary=6000, order="recent"):
    all_trackable_ids = []

    page = 1
    total_pages = 1

    while page <= total_pages:
        # 한 페이지만 가져오는 함수 호출
        trackable_ids, page, total_pages = get_trackable_ids(url, page, min_career, min_salary, order)

        if not trackable_ids:
            break

        # 추출한 trackable_ids를 all_trackable_ids 리스트에 추가
        all_trackable_ids.extend(trackable_ids)

        # 다음 페이지로 이동
        page += 1

    return all_trackable_ids


def get_job_position_detail(url, trackable_id, keywords):
    url = f"{url}/{trackable_id}"
    response = requests.get(url)
    info = {}
    # 응답 확인
    if response.status_code == 200:
        # JSON 형식의 응답 데이터를 딕셔너리로 파싱
        data = response.json()

        # 응답 데이터 문자열에 "원격"이 포함되어 있는지 확인
        response_text = str(data).lower()
        keyword_found = any(keyword in response_text for keyword in keywords)

        job_position = data["jobPosition"]

        company = job_position["company"]

        info["company"] = company["name"]
        info["title"] = job_position["title"]
        info["url"] = url
        info["keyword_found"] = keyword_found

        return info
    else:
        print("요청 실패:", response.status_code)


def get_all_job_position_detail(url, trackable_id_list, keywords):
    job_data_list = []
    for trackable_id in tqdm(trackable_id_list, desc="Processing"):
        job_data_list.append(get_job_position_detail(url, trackable_id, keywords))

    return sorted(job_data_list, key=lambda x: x["company"])


main()