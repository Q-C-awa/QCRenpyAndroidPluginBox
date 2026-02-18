package org.renpy.android;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.webkit.WebView;
import androidx.appcompat.app.AlertDialog;

// MainActivity 类继承自 Activity 类，用于管理应用的主界面
public class MainActivity extends Activity {

    @Override
    // onCreate 方法在 Activity 创建时被调用，用于初始化界面和数据进行设置
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 获取名为 "UserPrefs" 的 SharedPreferences 对象，用于存储和获取用户偏好设置
        SharedPreferences preferences = getSharedPreferences("UserPrefs", MODE_PRIVATE);
        // 从 SharedPreferences 中获取 "privacy_agreed" 键对应的布尔值，默认为 false
        boolean isPrivacyAgreed = preferences.getBoolean("privacy_agreed", false);

        // 如果用户未同意隐私协议，则显示隐私协议对话框
        if (!isPrivacyAgreed) {
            showPrivacyPolicyDialog();
        } else {
            // 如果用户已同意隐私协议，则启动游戏
            startGame();
        }
    }

    // showPrivacyPolicyDialog 方法用于显示隐私协议对话框
    private void showPrivacyPolicyDialog() {
        // 创建 WebView 对象并加载本地 HTML 文件中的隐私协议内容
        WebView webView = new WebView(this);
        webView.loadUrl("file:///android_asset/privacy_policy.html");

        // 使用 AlertDialog.Builder 创建对话框，并设置标题、视图和按钮
        new AlertDialog.Builder(this)
                .setTitle("隐私协议")
                .setView(webView)
                .setCancelable(false) // 设置对话框不可取消
                .setPositiveButton("同意", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // 用户点击同意按钮后，将 "privacy_agreed" 键设置为 true
                        SharedPreferences preferences = getSharedPreferences("UserPrefs", MODE_PRIVATE);
                        preferences.edit().putBoolean("privacy_agreed", true).apply();
                        // 启动游戏
                        startGame();
                    }
                })
                .setNegativeButton("拒绝", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        // 用户点击拒绝按钮后，退出应用
                        finishAffinity();
                    }
                })
                .show();
    }

    private void startGame() {
        // 启动游戏逻辑，比如跳转到 PythonSDLActivity
        startActivity(new android.content.Intent(this, PythonSDLActivity.class));
        finish(); // 关闭当前 Activity
    }
}
