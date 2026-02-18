package org.renpy.android;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.webkit.WebView;

import com.google.android.material.dialog.MaterialAlertDialogBuilder;

public class MainActivity extends Activity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        SharedPreferences preferences = getSharedPreferences("UserPrefs", MODE_PRIVATE);
        boolean isPrivacyAgreed = preferences.getBoolean("privacy_agreed", false);

        if (!isPrivacyAgreed) {
            showPrivacyPolicyDialog();
        } else {
            startGame();
        }
    }

    private void showPrivacyPolicyDialog() {
        WebView webView = new WebView(this);
        webView.loadUrl("file:///android_asset/privacy_policy.html");
        // 这里就是html的调用，你可以自己改main文件下面的html名字然后更改这里的文件引用来引入不同的文件
        new MaterialAlertDialogBuilder(this)   // 改用 MaterialAlertDialogBuilder
                .setTitle("隐私协议")
                .setView(webView)
                .setCancelable(false)
                .setPositiveButton("同意", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        SharedPreferences preferences = getSharedPreferences("UserPrefs", MODE_PRIVATE);
                        preferences.edit().putBoolean("privacy_agreed", true).apply();
                        startGame();
                    }
                })
                .setNegativeButton("拒绝", new DialogInterface.OnClickListener() {
                    @Override
                    public void onClick(DialogInterface dialog, int which) {
                        finishAffinity(); // 退出整个应用
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