from PIL import Image
import os

# 이미지를 자르고 저장할 디렉토리 경로
output_dir = 'assets/images/'

# 이미지를 로드합니다. (이미지 파일 경로를 정확하게 입력해주세요.)
image_path = "assets/images/brik.png"  # 프로젝트 폴더 안에 있는 경로로 변경  # 실제 이미지 경로로 변경해주세요.
img = Image.open(image_path)

# 자를 이미지의 크기 (각 블록의 크기)
block_width = 72
block_height = 22

# 이미지의 크기 확인 (이미지의 가로, 세로 크기)
img_width, img_height = img.size

# 블록을 자를 수 있도록 출력 디렉토리 만들기
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 블록을 자르고 저장하는 루프
block_counter = 1
blocks_per_column = 5  # 세로로 5개 블록
blocks_per_row = 2     # 가로로 2개 블록

# 블록 자르기: 이미지가 가로 2개, 세로 5개 블록이므로 각 블록의 위치를 계산
for row in range(blocks_per_column):  # 세로로 5개의 블록
    for col in range(blocks_per_row):  # 가로로 2개의 블록
        # 자를 영역 계산
        left = col * block_width
        upper = row * block_height
        right = left + block_width
        lower = upper + block_height
        
        # 이미지에서 해당 부분을 자름
        block = img.crop((left, upper, right, lower))
        
        # 파일 이름을 지정하여 저장
        block.save(os.path.join(output_dir, f"block_{block_counter}.png"))
        
        # 블록 카운터 증가
        block_counter += 1

print("블록 저장 완료!")