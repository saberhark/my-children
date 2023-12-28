import cv2

def extract_frames(video_path, output_dir, num_frames=30, skip_seconds=0, scale=0.5):
    cap = cv2.VideoCapture(video_path)

    # FPS 및 총 프레임 수 확인
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # 건너뛸 프레임 수 계산
    frames_to_skip = int(fps * skip_seconds)
    remaining_frames = total_frames - frames_to_skip

    # 남은 프레임에서 추출할 프레임 간격 계산
    skip_frames = remaining_frames // num_frames
    skip_frames = 1

    for i in range(total_frames):
        # 건너뛸 프레임을 고려하여 설정
        frame_index = frames_to_skip + i * skip_frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
        ret, frame = cap.read()

        if ret:
            # 프레임 크기 조정
            frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
            frame_path = output_dir + "/hornmush_" + f"{i:03d}.jpg"
            cv2.imwrite(str(frame_path), frame)
        else:
            break

    cap.release()

# 프레임 추출 실행
video_path = r"C:\Users\Hwang\Videos\Captures\MapleStory Worlds-Mapleland 2023-12-23 22-32-58.mp4"
output_dir = "./frame/"
extract_frames(video_path, output_dir, scale=1)  # 프레임 크기를 50%로 조정
