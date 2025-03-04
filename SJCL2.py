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

# 新增动画参数设置
section_limits = [60, 300]  # 对应200-800英尺转换为米（约61-244米）
y_limit = [-52, 76]         # -170~250英尺转换为米
vehicle_colors = {1: 'red', 2: 'yellow', 3: 'green'}  # 车型颜色映射

# 初始化画布（新增代码）
fig, ax = plt.subplots(figsize=(12, 6))
ax.set_title('NGSIM 车辆轨迹动画')
ax.set_xlim(section_limits[0]-15, section_limits[1]+15)
ax.set_ylim(y_limit[0], y_limit[1])
ax.set_xlabel('纵向坐标 (米)')
ax.set_ylabel('横向坐标 (米)')
ax.invert_yaxis()  # 保持与MATLAB相同的坐标系方向

# 绘制道路边界（新增代码）
ax.axhline(0, color='blue', linestyle='--', linewidth=0.8)
ax.axhline(3.7, color='blue', linestyle='--', linewidth=0.8)  # 假设车道宽度3.7米

def animate(frame):
    """动画更新函数"""
    while ax.patches:
        ax.patches[-1].remove()
    while ax.texts:
        ax.texts[-1].remove()
    
    frame_data = data1[(data1['Frame_ID'] == frame) & 
                      (data1['Local_Y'].between(*section_limits))]
    
    for _, row in frame_data.iterrows():
        color = vehicle_colors.get(row.get('Class', 2), 'yellow')
        rect = plt.Rectangle(
            (row['Local_Y']-row['v_Length'], row['Local_X']-row['v_Width']/2),
            row['v_Length'], row['v_Width'],
            facecolor=color, edgecolor='black')
        ax.add_patch(rect)
        ax.text(row['Local_Y']-row['v_Length']*0.6, row['Local_X'], 
               str(row['Vehicle_ID']), fontsize=6, color='blue')
    
    ax.figure.canvas.draw()  # 新增重绘控制
    return []

# 修改动画生成参数
ani = animation.FuncAnimation(
    fig, animate,
    frames=np.sort(data1['Frame_ID'].unique()),  # 使用实际存在的帧号
    interval=100,  # 加快刷新速度
    repeat=False,
    cache_frame_data=False)
    
plt.show()