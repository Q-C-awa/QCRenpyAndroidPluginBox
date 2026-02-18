package org.renpy.android;

import android.app.Activity;
import android.content.DialogInterface;
import android.content.Intent;
import android.os.Bundle;
// MD3主题
import android.text.Html;
import android.text.method.LinkMovementMethod;
import android.util.TypedValue;
import android.widget.TextView;
import androidx.appcompat.app.AppCompatActivity; 
import com.google.android.material.dialog.MaterialAlertDialogBuilder;

public class MainActivity extends AppCompatActivity implements DialogInterface.OnClickListener {

    // 删除 GAME_NAME 常量
    private static final String PRIVACY_URL = "这里填你的隐私合规文档等链接";

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
        // 使用 getApplicationInfo().labelRes 获取应用名称资源
        String gameName = getString(getApplicationInfo().labelRes);
        
        // 使用 HTML 格式定义内容，<a> 标签会被处理为可点击链接
        String privacyContext = "欢迎您使用【" + gameName + "】！我们非常重视保护您的个人信息和隐私。<br><br>" +
                "您可以通过阅读 <a href=\"" + PRIVACY_URL + "\">《隐私政策》</a> " +
                "了解我们收集、使用、存储用户个人信息的情况。";
        // 这里的文本不喜欢可以看着改
        TextView textView = new TextView(this);
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.N) {
            textView.setText(Html.fromHtml(privacyContext, Html.FROM_HTML_MODE_LEGACY));
        } else {
            textView.setText(Html.fromHtml(privacyContext));
        }
        textView.setMovementMethod(LinkMovementMethod.getInstance());
        int padding = (int) TypedValue.applyDimension(TypedValue.COMPLEX_UNIT_DIP, 24, getResources().getDisplayMetrics());
        textView.setPadding(padding, padding/2, padding, 0);
        textView.setTextSize(16);
        new MaterialAlertDialogBuilder(this)
            .setCancelable(false)
            .setTitle("个人信息保护提示")
            .setView(textView) // 放入 TextView
            .setNegativeButton("退出", this)
            .setPositiveButton("同意并继续", this)
            .show();
    }

    @Override
    public void onClick(DialogInterface dialog, int which) {
        switch (which) {
            case DialogInterface.BUTTON_POSITIVE:
                setPrivacyAccepted(true);
                startGame();
                break;
            case DialogInterface.BUTTON_NEGATIVE:
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
