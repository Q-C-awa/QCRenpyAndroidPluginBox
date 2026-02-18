package org.renpy.android;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
import android.webkit.WebView;
import androidx.appcompat.app.AlertDialog;

public class MainActivity extends Activity implements DialogInterface.OnClickListener {

    private static final String GAME_NAME = "冬日树下的回忆";
    private static final String PRIVACY_URL = "https://docs.qq.com/doc/DQUhnUnhUWmVCdkJo?errorpage_redirect_count=1&nlc=1";
    private static final String PRIVACY_CONTEXT = 
        "\n欢迎您使用【" + GAME_NAME + "】！我们非常重视保护您的个人信息和隐私。" +
        "您可以通过《【" + GAME_NAME + "】<a href=\"" + PRIVACY_URL + "\">《隐私政策》</a>" +
        "了解我们收集、使用、存储用户个人信息的情况";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        if (hasUserAcceptedPrivacy()) {
            startGame();
            return;
        }
        showPrivacyDialog();
    }

    private void showPrivacyDialog() {
        WebView webView = new WebView(this);
        webView.loadData(PRIVACY_CONTEXT, "text/html", "UTF-8");

        new AlertDialog.Builder(this)
            .setCancelable(false)
            .setView(webView)
            .setTitle("提示")
            .setNegativeButton("拒绝", this)
            .setPositiveButton("同意", this)
            .create()
            .show();
    }

    @Override
    public void onClick(DialogInterface dialog, int which) {
        switch (which) {
            case AlertDialog.BUTTON_POSITIVE:
                setPrivacyAccepted(true);
                startGame();
                break;
            case AlertDialog.BUTTON_NEGATIVE:
                finish(); // 用户拒绝，退出应用
                break;
        }
    }

    private void startGame() {
        startActivity(new Intent(this, PythonSDLActivity.class));
        finish();
    }

    private boolean hasUserAcceptedPrivacy() {
        // 从 SharedPreferences 或其他存储读取用户是否同意隐私政策
        return getPreferences(MODE_PRIVATE).getBoolean("PRIVACY_ACCEPTED", false);
    }

    private void setPrivacyAccepted(boolean accepted) {
        // 存储用户同意状态
        getPreferences(MODE_PRIVATE).edit()
            .putBoolean("PRIVACY_ACCEPTED", accepted)
            .apply();
    }
}
