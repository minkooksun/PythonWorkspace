import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


# 문제 설정
fabric_width = 2000
pieces = [
    (1000, 2000), (1000, 2000), (1000, 2000),
    (660, 2000), (660, 2000), (660, 2000),
    (500, 1000), (500, 1000), (500, 1000), (500, 2000), (300, 500)
    , (300, 500), (200, 900)
]
num_pieces = len(pieces)

# 공간이 비어 있는지 확인하는 함수
def is_space_free(placements, x, y, width, height, fabric_width):
 
    if x + width > fabric_width:
        return False
    
    
    for px, py, pwidth, pheight in placements:
        if not (x + width <= px or x >= px + pwidth or y + height <= py or y >= py + pheight):
            
            return False 
    return True

def append_if_not_exists(arr, item):
    if item not in arr:
        arr.append(item)

# 간극 채워넣기
def fill_gaps(placements, pieces, fabric_width):
    new_placements = placements[:]
    pieces = sorted(pieces, key=lambda piece: piece[0] * piece[1], reverse=True)
    y_positions = [0]  # 초기 y 위치
    max_height = 0
    for width, height in pieces:
        placed = False
 
        y_positions.sort()  # y_positions를 정렬

        for y in y_positions :
            if placed:
                break
            for x in range(fabric_width): 

                if is_space_free(new_placements, x, y, width, height, fabric_width):
                     
                    new_placements.append((x, y, width, height))
                    append_if_not_exists(y_positions,y + height)
                    if max_height < (y + height):
                        max_height = y + height  
                    placed = True
                    break
 
        if not placed:
            # 배치할 수 없으면 새로운 위치에 배치
            current_max_y = max(y + height for _, y, _, height in new_placements)
            new_placements.append((0, current_max_y, width, height))
            append_if_not_exists(y_positions,current_max_y + height) 

        # 기존 배치된 조각 사이의 빈 공간을 확인하고 조각을 넣을 수 있는지 확인
        for i in range(len(new_placements)):
            for j in range(i + 1, len(new_placements)):
                px1, py1, pw1, ph1 = new_placements[i]
                px2, py2, pw2, ph2 = new_placements[j]

                # 가로 방향으로 빈 공간 확인
                if px1 + pw1 <= px2:
                    if is_space_free(new_placements, px1 + pw1, py1, width, height, fabric_width):
                        new_placements.append((px1 + pw1, py1, width, height))
                        placed = True
                        break

                # 세로 방향으로 빈 공간 확인
                if py1 + ph1 <= py2:
                    if is_space_free(new_placements, px1, py1 + ph1, width, height, fabric_width):
                        new_placements.append((px1, py1 + ph1, width, height))
                        placed = True
                        break

            if placed:
                break

    return new_placements

# 배치 시각화
def visualize_placements(placements, fabric_width):
    fig, ax = plt.subplots()
    current_max_y = 0

    for (x, y, width, height) in placements:
        ax.add_patch(Rectangle((x, y), width, height, edgecolor='black', facecolor='gray', fill=True))
        current_max_y = max(current_max_y, y + height)

    ax.set_xlim(0, fabric_width)
    ax.set_ylim(0, current_max_y)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

# 초기 배치
placements = []
print("Placements before filling gaps:", placements)
# 간극 채워넣기
placements = fill_gaps(placements, pieces, fabric_width)
print("Placements after filling gaps:", placements)

# 배치 시각화
visualize_placements(placements, fabric_width)