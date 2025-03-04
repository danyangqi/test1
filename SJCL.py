import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams['font.sans-serif'] = ['SimHei']  
plt.rcParams['axes.unicode_minus'] = False  

#典型数据字段示例（每个车辆包含100+维度）
# {
#     "Vehicle_ID": 102,                # 车辆唯一标识
#     "Frame_ID": 12580,                # 时间戳(0.1秒单位)
#     "Local_X": 35.214,                # 横向坐标(米)
#     "Local_Y": 1205.76,               # 纵向坐标(米)
#     "v_Vel": 12.5,                    # 速度(m/s)
#     "v_Accel": 0.32,                  # 加速度(m/s²)
#     "Lane_ID": 2,                     # 车道编号
#     "Preceding_Veh": 101,             # 前车ID
#     "Space_Headway": 8.2,             # 车头间距(米)
#     "Time_Headway": 1.5               # 车头时距(秒)
#     
# }

data1=pd.read_csv(r"C:\Users\14611\Documents\WeChat Files\lk62433999\FileStorage\File\2025-02\US-101-LosAngeles-CA\us-101-vehicle-trajectory-data\vehicle-trajectory-data\0750am-0805am\trajectories-0750am-0805am.csv")
# 新增筛选语句
data_vehicle_2 = data1[data1['Vehicle_ID'] == 2]

print(f"找到 {len(data_vehicle_2)} 条记录")
print(data_vehicle_2[['Vehicle_ID', 'Frame_ID', 'Local_X', 'Local_Y']].head())

# 修改保存路径（示例：保存到桌面）
save_path = r"C:\Users\14611\Desktop\vehicle_2_data.csv"
data_vehicle_2.to_csv(save_path, index=False)
data1=pd.read_csv(r"C:\Users\14611\Desktop\vehicle_2_data.csv")
# 替换原有的静态可视化代码
# 修改可视化部分为双图布局
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), dpi=150)

# 轨迹图初始化
line, = ax1.plot([], [], 'b-', linewidth=1.5)
dot = ax1.scatter([], [], c='r', s=30)
ax1.set(xlim=(data_vehicle_2['Local_X'].min()-5, data_vehicle_2['Local_X'].max()+5),
       ylim=(data_vehicle_2['Local_Y'].min()-5, data_vehicle_2['Local_Y'].max()+5),
       xlabel='Local_X (米)', ylabel='Local_Y (米)', 
       title='车辆轨迹动态可视化')
ax1.grid(True, linestyle='--', alpha=0.5)

# 新增速度图初始化
speed_line, = ax2.plot([], [], 'g-', linewidth=1)
speed_dot = ax2.scatter([], [], c='orange', s=30)
ax2.set(xlim=(0, len(data_vehicle_2)),
       ylim=(data_vehicle_2['v_Vel'].min()-2, data_vehicle_2['v_Vel'].max()+2),
       xlabel='时间帧', ylabel='速度 (m/s)', 
       title='速度变化曲线')
ax2.grid(True, linestyle='--', alpha=0.5)

def init():
    line.set_data([], [])
    dot.set_offsets(np.empty((0, 2)))
    speed_line.set_data([], [])
    speed_dot.set_offsets(np.empty((0, 2)))
    return line, dot, speed_line, speed_dot

def animate(i):
    # 更新轨迹图
    x = data_vehicle_2['Local_X'].iloc[:i+1]
    y = data_vehicle_2['Local_Y'].iloc[:i+1]
    line.set_data(x, y)
    dot.set_offsets(np.column_stack((x.iloc[-1], y.iloc[-1])))
    
    # 新增速度图更新
    t = np.arange(i+1)
    v = data_vehicle_2['v_Vel'].iloc[:i+1]
    speed_line.set_data(t, v)
    speed_dot.set_offsets(np.column_stack((i, v.iloc[-1])))
    
    return line, dot, speed_line, speed_dot

# 修改动画参数
ani = animation.FuncAnimation(
    fig, animate, 
    init_func=init,
    frames=len(data_vehicle_2),
    interval=50,
    blit=True
)

plt.tight_layout()
plt.show()