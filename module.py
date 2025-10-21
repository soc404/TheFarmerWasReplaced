
# returns true if n is even
def is_even(n):
    return n % 2 == 0

# Returns true if the player is on a tree-planting square
def can_tree(x=get_pos_x(),y=get_pos_y()):
    return is_even(x)==is_even(y)
        
# Plant either a tree or a carrot based on the current position
def plantx():
    num_items(Items.Hay)
    num_items(Items.Wood)
    num_items(Items.Carrot)
    if can_tree():
            plant(Entities.Tree)
    else:
        if is_even(get_pos_x()):
            if get_ground_type()==Grounds.Grassland:
                till()
            plant(Entities.Carrot)
        else:
            if get_ground_type()==Grounds.Soil:
                till()
            

# Move to a specific (x,y) coordinate
def moveto(x, y):
    L = get_world_size()
    current_x, current_y = get_pos_x(), get_pos_y()
    x %= L
    y %= L
    
    # 计算环上最短移动
    def calc_move(current, target, pos_dir, neg_dir):
        d = abs(current - target)
        if d <= L - d:  # 直接距离更短
            steps = d
            if target > current:
                direction = pos_dir
            else:
                direction = neg_dir
        else:  # 绕环距离更短
            steps = L - d
            if target > current:
                direction = neg_dir
            else:
                direction = pos_dir
        return steps, direction
    
    steps_x, dir_x = calc_move(current_x, x, East, West)
    steps_y, dir_y = calc_move(current_y, y, North, South)
    
    # 交替移动，优先移动距离较远的方向
    while steps_y > 0 or steps_x > 0:
        if steps_y > steps_x:
            move(dir_y)
            steps_y -= 1
        else:
            move(dir_x)
            steps_x -= 1

# Move to the next square in a zig-zag pattern
def move_zig_zag():
    world_size=get_world_size()
    if is_even(get_pos_x()):
        if get_pos_y() == world_size-1:
            move(East)
        else:
            move(North)
    else:
        if get_pos_y() == 0:
            move(East)
        else:
            move(South)

# Move to the next square in a custom zig-zag pattern
def move_zig_zag_custom(x1=0,y1=0,x2=get_world_size()-1,y2=get_world_size()-1):
    if get_pos_y()<y1 or get_pos_y()>y2 or get_pos_x()<x1 or get_pos_x()>x2:
        moveto(x1,y1)
        return
    if is_even(get_pos_x()):
        if get_pos_y() == y2:
            if get_pos_x() != x2:
                move(East)
            else:
                moveto(x1,y2)
        else:
            move(North)
    else:
        if get_pos_y() == y1:
            if get_pos_x() != x2:
                move(East)
            else:
                moveto(x1,y1)
        else:
            move(South)
            

# Main loop to plant trees and carrots
def run():
    while True:
        if can_harvest():
            harvest()
            plantx()
        elif get_entity_type()==None or get_entity_type()==Entities.Dead_Pumpkin:
            plantx()
        move_zig_zag()

# Plant a pumpkin if not already planted
def plant_Pumpkin():
    if get_entity_type()==Entities.Pumpkin:
        return
    if get_ground_type()==Grounds.Grassland:
        till()
    plant(Entities.Pumpkin)

# Main loop to plant pumpkins in a zig-zag pattern
def run_Pumpkin(square_num=get_world_size()**2):
    count=0
    while True:
        if can_harvest() and get_entity_type()!=Entities.Pumpkin:
            harvest()
            count=0
        elif can_harvest() and get_entity_type()==Entities.Pumpkin:
            if count==square_num-1:
                    harvest()
                    count=0
            else:
                count+=1
        else:
            count=0
        plant_Pumpkin()
        move_zig_zag()

def run_Pumpkin_multiple():
    set_world_size(13)
    clear()
    #areas=[[0,0,5,5],[0,6,5,11],[6,0,11,5],[6,6,11,11]]
    areas=[[0,0,5,5],[0,7,5,12],[7,0,12,5],[7,7,12,12]]
    def pumpkin(i=num_drones()-2):
            moveto(areas[i][0],areas[i][1])
            square_num=(areas[i][2]-areas[i][0]+1)*(areas[i][3]-areas[i][1]+1)
            count=0
            while True:
                if can_harvest() and get_entity_type()!=Entities.Pumpkin:
                    harvest()
                    count=0
                elif can_harvest() and get_entity_type()==Entities.Pumpkin:
                    if count==square_num-1:
                        harvest()
                        count=0
                    else:
                        count+=1
                else:
                    count=0
                plant_Pumpkin()
                move_zig_zag_custom(areas[i][0],areas[i][1],areas[i][2],areas[i][3])
    for _ in range(max_drones()):
        if not spawn_drone(pumpkin):
            for y in range(13):
                moveto(6,y)
                if can_tree():
                    plant(Entities.Tree)
                else:
                    plant(Entities.Bush)
            for x in range(13):
                moveto(x,6)
                if can_tree():
                    plant(Entities.Tree)
                else:
                    plant(Entities.Bush)
            moveto(6,6)
            print("每 人 一 块 南 瓜 田 ~ ~ ~ ")
            pumpkin(3)

def run_Weird():
    clear()
    moveto(1,1)
    while True:
        if can_harvest():
            use_item(Items.Weird_Substance)
            harvest()
            moveto(1,2)
            harvest()
            moveto(2,1)
            harvest()
            moveto(1,0)
            harvest()
            moveto(0,1)
            harvest()
            moveto(1,1)

# Main loop to using weird substance and seek treasure 
def run_seek_Treasure():
    clear()
    substance_need = get_world_size() * 2**(num_unlocked(Unlocks.Mazes) - 1)
    directions = [North, East, South, West]
    while True:
        plant(Entities.Bush)
        use_item(Items.Weird_Substance, substance_need)
        index = 0
        while get_entity_type()!=Entities.Treasure:
            index = (index - 1) % 4
            while can_move(directions[index])==False:
                index = (index + 1) % 4
            move(directions[index])
        harvest()


def run_companion_mode():
    moveto(random()*get_world_size()//1,random()*get_world_size()//1)
    plant_type=Entities.Carrot
    while True:
        if get_ground_type()==Grounds.Grassland:
            till()
        if get_water()<0.75:
            use_item(Items.Water,(1-get_water())//0.25)
        if get_entity_type()!=None:
            while not can_harvest():
                use_item(Items.Fertilizer)
            harvest()

        while plant(plant_type)==False:
            if get_entity_type()!=None:
                moveto(random()*get_world_size()//1,random()*get_world_size()//1)
                break
        next_plant_type, (x, y) = get_companion()
        while next_plant_type==Entities.Tree and not(can_tree(x,y)):
            harvest()
            plant(plant_type)
            next_plant_type, (x, y) = get_companion()
        plant_type=next_plant_type
        moveto(x, y)

def multiple_companion_mode():
    clear()
    def multiple():
        for _ in range(max_drones()):
            moveto(random()*get_world_size()//1,random()*get_world_size()//1)
            spawn_drone(run_companion_mode)
        run_companion_mode()
    multiple()