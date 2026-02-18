define build.android_permissions = [
    "android.permission.READ_EXTERNAL_STORAGE", # 读取存储权限
    "android.permission.WRITE_EXTERNAL_STORAGE",
    "android.permission.READ_MEDIA_IMAGES", # 读取媒体权限
    "android.permission.READ_MEDIA_VIDEO"
]
init python:
    
    # 导入jnius
    class AlbumManager(object):
        try:
            import os
            import shutil
            from jnius import autoclass     
            def __init__(self):
                self.PythonSDLActivity = autoclass('org.renpy.android.PythonSDLActivity')
                # 获取PythonSDLActivity类
                self.activity = self.PythonSDLActivity.mActivity
                # 获取活动
                self.last_saved_filename = ""
            def open_gallery(self):
                # 调用java中的openSystemAlbum
                self.activity.openSystemAlbum()
            def fetch_and_copy_image(self):
                # 调用java中的getPickedPath 
                source_path = self.activity.getPickedPath()
                renpy.notify(f"Picked image path: {source_path}")
                # 这个notify是调试用的，可以删除
                if not source_path:
                    return None
                target_dir = os.path.join(config.gamedir, "images/Q_C_pick")
                # 定义图片路径，这里必须和下面图片变量定义一样
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                original_filename = os.path.basename(source_path)
                dest_filename = "picked_" + original_filename
                # 在获取的图片名前加上picked_
                target_path = os.path.join(target_dir, dest_filename)
                try:
                    shutil.copy(source_path, target_path)
                    self.last_saved_filename = dest_filename
                    renpy.notify(f"Image copied to: {target_path}")
                    # 这个notify是调试用的，可以删除
                    return dest_filename
                except Exception as e:
                    renpy.notify("Copy Error: " + str(e))
                    # 这个notify是调试用的，可以删除
                    return None
            def get_image_name(self):
                return self.last_saved_filename
        except Exception as e:
            renpy.notify("非移动平台" + str(e))
# 使用方法：
# 首先先实例化Album
# 然后调用open_gallery()打开相册
# 之后调用fetch_and_copy_image()获取所选图片并复制到游戏目录，返回图片文件名
# 获取图片要像picked_img = "images/Q_C_pick/" + img_name，前面的"images/Q_C_pick/"是必须的，不然会找不到图片
# 然后这里定义了一个变量用于临时储存获取的图片
# 在使用前，你需要使用request_permission获取权限，不然会失败
# 这里给出一个使用并且用show语句展示
label album_test:
    "准备调用相册..."
    python:
        # 授权权限，你可以把这一部分移动到别的地方，但是需要在调用相册前申请权限
        for pess in build.android_permissions:
            renpy.request_permission(pess)
        #
        album = AlbumManager()
        album.open_gallery()
    "选照片"
    python:
        img_name = album.fetch_and_copy_image()
    if img_name:
        $ picked_img = "images/Q_C_pick/" + img_name
        "成功：[img_name]"
        show expression picked_img at truecenter
        "[img_name]"
    jump album_test


