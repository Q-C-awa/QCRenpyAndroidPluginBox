# 这个文件放在你项目里面
init python:
    def AndroidNotify(title_text="Ren’py", box_text="这是一条来自Ren’py的通知", channel_id="renpy_channel"):
        try:
            import jnius
            if not renpy.android:
                return False
            try:
                PythonSDLActivity = jnius.autoclass("org.renpy.android.PythonSDLActivity")
                activity = PythonSDLActivity.mActivity
                if activity is None:
                    renpy.notify("无活动")
                    return False
                activity.AndroidNotifyBox(title_text, box_text)
                return True
            except Exception as error:
                print(None, f"发送通知失败:\n {str(error)}")
                return False
        except Exception as error:
            renpy.notify(f"{str(error)}\n无法初始化，运行平台非Android")
