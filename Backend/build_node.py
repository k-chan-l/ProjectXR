'''
목표
opencv를 활용해서 저장된 도면 이미지를 읽고, 도면에 표시
도면 기반으로 엔진 내부의 좌표 계산 후 json으로 저장

필요한 정보
건물 도면 + 기준점 2좌표 + 층별 높이 좌표

로직
0. 좌표지정 -> 최초 1회만 실행
0-1. 첫번째 이미지를 띄움 opencv
0-2. 첫번째 이미지에서 기준점 잡기, 하드코딩된 좌표를 수동으로 클릭하여 좌표 출력
0-3. 이미지에서 출력된 x,y, w,h를 기준점으로 지정하여 거리 계수 저장
1. 각 층별 반복 1~n층 opencv
1-1. 폴더 내부의 이미지 읽기, 현재 층 dictionary에 지정
1-2. 도면 이미지 띄우기
1-3. 버튼 클릭시 해당 위치에 이미지에 노드 이름 표시(원과 글씨) 및 좌표 추정 하여 스택에 저장
1-3-1. u버튼 입력시 되돌리기
1-4. q버튼을 입력하여 현재 노드가 지정된 이미지를 저장 + 스택에 있는 정보를 dictionary에 저장하고, 다음 이미지로드
2. 각층 이미지를 띄움 각 층마다 반복 matplotlib.plt 사용
2-1. 입력된 dictionary를 바탕으로 각층별 노드와 연결된 노드를 입력 공백으로 구분
3. 입력된 연결노드를 바탕으로 거리를 계산해서 dictionary에 입력
4. dictionary를 json으로 변환해서 저장

json data
graph = {
    floor(int) :{ 층
        node(int) : 층별 노드 번호
        {
        'coordinate' : {'x' : x, 'y' : y, 'z' : z},
        'node_name' : name,
        'links' : [
            {
            'node' : node_name,
            'cost' : distance,
            'type': vertical or horizontal
            }
        ],
        'description' : text
        'type' : path or destination
        }
    }
}
'''
import cv2
import json
import math
import numpy as np
from pathlib import Path

floorplan_dir = './Data/FloorPlan/'
graph_dir = './Data/Graph/'
floorplan_name = 'floor_'
floorplan_type = '.png'
# 직접 확인 후 지정
point = [{'x':2185, 'y':-2975}, {'x':-35, 'y':-2975}] # 엔진 내부 기준 좌표
p_point = [{'x':442, 'y':70}, {'x':277, 'y':70}] # 그림 기준 좌표
z_level = {1:0, 2:450, 3:1050}
scale = (point[0]['x'] - point[1]['x']) / (p_point[0]['x'] - p_point[1]['x'])

types = ('path', 'destination', 'escalator')
link_types = ('horizontal', 'vertical')

def calc_UEpoint(x, y):
    dx = x - p_point[0]['x']
    dy = y - p_point[0]['y']
    ue_x = point[0]['x'] + dx*scale
    ue_y = point[0]['y'] + dy*scale
    return (ue_x, ue_y)

def mouse_clickEvent(e, x, y, flags, params):
    if e == cv2.EVENT_LBUTTONDOWN:
        global count; count += 1
        st = params['st']
        st.append((x, y, count)) # 카운트를 글자로해서 x,y지점에 그림을 그림
        ue_x, ue_y = calc_UEpoint(x, y)
        floor_node = params['dict']
        floor_node[count] = {
            'coordinate' : {'x':ue_x, 'y':ue_y, 'z':params['z']},
            'node_name':count,
            'img_coordinate': (x,y)
            }

def draw_node(st, img):
    for i in st:
        cv2.circle(img, (i[0], i[1]), 5, (0, 0, 255), -1)
        cv2.putText(img, str(i[2]), (i[0]+8, i[1]-8),
            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)

def calc_dist(st_node, ed_node):
    x_dist_pow = (st_node['coordinate']['x'] - ed_node['coordinate']['x'])**2
    y_dist_pow = (st_node['coordinate']['y'] - ed_node['coordinate']['y'])**2
    z_dist_pow = (st_node['coordinate']['z'] - ed_node['coordinate']['z'])**2
    return (x_dist_pow + y_dist_pow + z_dist_pow)**0.5

def draw_arrow(img, p1, p2, size=10):
    x1, y1 = p1
    x2, y2 = p2

    dx = x2 - x1
    dy = y2 - y1
    dist = math.hypot(dx, dy)

    if dist == 0:
        return

    ux, uy = dx / dist, dy / dist

    # 화살표 끝
    tip = (x2, y2)

    # 뒤쪽 기준점
    base_x = x2 - ux * size
    base_y = y2 - uy * size

    # 좌우 퍼짐
    perp_x = -uy
    perp_y = ux

    left = (int(base_x + perp_x * size/2), int(base_y + perp_y * size/2))
    right = (int(base_x - perp_x * size/2), int(base_y - perp_y * size/2))

    # 선
    cv2.line(img, p1, p2, (255,255,255), 1)

    # 화살촉
    cv2.fillPoly(img, [np.array([tip, left, right])], (255,255,255))

folder = Path(floorplan_dir)
floor_num = len(list(folder.glob("*" + floorplan_type)))
count = 0
floors = {}
maps = {}
# 노드 맵핑
for floor in range(1, floor_num+1):
    floor_node = {}
    st = [] # 작업 스택
    path = floorplan_dir + floorplan_name + str(floor) + floorplan_type
    img = cv2.imread(filename=path)
    rotated_origin = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE) # 이미지 회전 -> 언리얼, 이미지 방향 통일
    while True:
        rotated = rotated_origin.copy()
        draw_node(st,rotated)
        cv2.imshow('floorplan', rotated)
        params = {'st':st, 'z':z_level[floor], 'dict':floor_node}
        cv2.setMouseCallback('floorplan', mouse_clickEvent, params)
        key = cv2.waitKey(1)
        if key == ord('q'):
            maps[floor] = rotated
            break
        elif key == ord('u'):
            st.pop()
            del floor_node[count]
            count -=1
    floors[floor] = floor_node
# print(floors)
# edge 설정
all_nodes = {}
for i in floors.values():
    all_nodes.update(i)
print(all_nodes)
for cur_floor in range(1, floor_num+1):
    path = graph_dir + floorplan_name + str(cur_floor) + floorplan_type
    cv2.imwrite(path, maps[cur_floor])


graph = {}
for cur_floor in range(1, floor_num+1):
    floor = {}
    floorplan = maps[cur_floor]
    for nodes in floors[cur_floor].values():
        cv2.imshow('floorplan', floorplan)
        cv2.waitKey(1)
        print(f'현재 노드 : {nodes['node_name']} --------')
        disc = input('현재 노드의 설명을 입력하세요 : ')
        node_type = int(input('현재 노드의 타입을 입력하세요(path:0, destination:1, escalator:2): '))
        next_nodes = list(map(int,input('이동할 수 있는 노드를 입력하세요(공백으로 구분) : ').split()))
        next_nodes_type = list(map(int,input('각 연결의 타입을 입력하세요(공백으로 구분, horizontal:0, vertical:1) : ').split()))
        # 연결 정리 및 그림 그리기
        links = []
        for i in range(len(next_nodes)):
            link = {}
            link['node'] = next_nodes[i]
            link['type'] = link_types[next_nodes_type[i]]
            link['cost'] = calc_dist(nodes, all_nodes[next_nodes[i]])
            links.append(link)
            if node_type == 2:
                cv2.circle(floorplan, nodes['img_coordinate'], 5, (255, 0, 0), -1)
            if next_nodes_type[i] == 0:
                draw_arrow(floorplan, nodes['img_coordinate'], floors[cur_floor][next_nodes[i]]['img_coordinate'], 5)

        floor[nodes['node_name']] = {
            'coordinate' : nodes['coordinate'],
            'node_name': nodes['node_name'],
            'links' : links,
            'description' : disc,
            'type' : types[node_type]
        }
    graph[cur_floor] = floor
    
    path = graph_dir + floorplan_name + str(cur_floor) + floorplan_type
    cv2.imwrite(path, floorplan)
with open(graph_dir+'graph.json', 'w', encoding='utf-8') as f:
    json.dump(graph, f, ensure_ascii=False, indent=4)
cv2.destroyAllWindows()