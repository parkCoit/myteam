import cv2
import pytesseract


def video_capture():
    # 동영상 파일 경로
    video_path = "../data/video/13-1_KR-6333959106_11.webm"

    # 이미지 저장 경로
    image_path = "../data/img/capture2/"

    # 동영상 캡처 객체 생성
    cap = cv2.VideoCapture(video_path)

    # 프레임 수 확인
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(frame_count)

    # 프레임 레이트 확인
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(fps)

    # 저장될 이미지 번호 초기화
    image_count = 0

    # 프레임 순회
    while cap.isOpened():
        # 프레임 캡처
        ret, frame = cap.read()

        # 캡처 실패시 종료
        if not ret:
            break

        # 일정 프레임 간격으로 이미지 저장
        if image_count % 5 == 0:
            image_name = f"{image_path}frame_{image_count}.jpg"
            cv2.imwrite(image_name, frame)

        image_count += 1

    # 객체 해제
    cap.release()



if __name__ == '__main__':
    video_capture()



