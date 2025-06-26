from microbit import *

# 状态变量
face = -2
last_displayed = -3
display_lock = False

# 初始化
k210_models.initialization()
music.set_built_in_speaker_enabled(True)
music.set_volume(59)
display.clear()

def update_display(face_id):
    global last_displayed, display_lock
    display_lock = True

    # 仅当状态变化时刷新显示
    if face_id != last_displayed:
        if face_id == 0:
            display.show(Image("00900:09090:09090:09090:00900"))  # 圆圈
        elif face_id == 1:
            display.show(Image("00900:00900:00900:00900:00900"))  # 竖线
        elif face_id == 2:
            display.show(Image("09990:00090:09990:09000:09990"))  # 数字2
        elif face_id == -1:
            display.clear()
        else:
            display.show(Image("90009:09090:00900:09090:90009"))  # X图标

        last_displayed = face_id

    sleep(300)  # 显示保持300ms
    display_lock = False

# 主循环
while True:
    if not display_lock:
        new_face = k210_models.face_reg()
        if new_face != face:
            face = new_face
            update_display(face)

            # 音效触发
            if face == 0:
                music.play(music.POWER_UP)
            elif face == 1:
                music.play(music.JUMP_UP)
            elif face == 2:
                music.play(music.JUMP_DOWN)
