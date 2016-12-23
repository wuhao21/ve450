package com.caoyu.voice;

import android.os.Bundle;
import android.os.Environment;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import com.iflytek.cloud.SpeechConstant;
import com.iflytek.cloud.SpeechError;
import com.iflytek.cloud.SpeechSynthesizer;
import com.iflytek.cloud.SynthesizerListener;
import com.iflytek.cloud.util.ResourceUtil;

public class WriteActivity extends AppCompatActivity implements View.OnClickListener {
    SpeechSynthesizer mTts;
    private EditText contentEt;
    private Button writeBtn, cancelBtn, pauseBtn, resumeBtn;
    private Toast mToast;
    private boolean isCloud = false;
    //合成监听器
    private SynthesizerListener mSynListener = new SynthesizerListener() {
        @Override
        public void onSpeakBegin() {
            showTip("开始播放");
        }

        @Override
        public void onSpeakPaused() {
            showTip("暂停播放");
        }

        @Override
        public void onSpeakResumed() {
            showTip("继续播放");
        }

        @Override
        public void onBufferProgress(int percent, int beginPos, int endPos,
                                     String info) {
//            // 合成进度
//            mPercentForBuffering = percent;
//            showTip(String.format(getString(R.string.tts_toast_format),
//                    mPercentForBuffering, mPercentForPlaying));
        }

        @Override
        public void onSpeakProgress(int percent, int beginPos, int endPos) {
//            // 播放进度
//            mPercentForPlaying = percent;
//            showTip(String.format(getString(R.string.tts_toast_format),
//                    mPercentForBuffering, mPercentForPlaying));
        }

        @Override
        public void onCompleted(SpeechError error) {
            if (error == null) {
                showTip("播放完成");
            } else if (error != null) {
                showTip(error.getPlainDescription(true));
            }
        }

        @Override
        public void onEvent(int eventType, int arg1, int arg2, Bundle obj) {
            // 以下代码用于获取与云端的会话id，当业务出错时将会话id提供给技术支持人员，可用于查询会话日志，定位出错原因
            // 若使用本地能力，会话id为null
            //	if (SpeechEvent.EVENT_SESSION_ID == eventType) {
            //		String sid = obj.getString(SpeechEvent.KEY_EVENT_SESSION_ID);
            //		Log.d(TAG, "session id =" + sid);
            //	}
        }
    };

    private void showTip(final String str) {
        mToast.setText(str);
        mToast.show();
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mToast = Toast.makeText(this,"",Toast.LENGTH_SHORT);
        setContentView(R.layout.activity_write);
        writeBtn = (Button) findViewById(R.id.writeBtn);
        contentEt = (EditText) findViewById(R.id.contentEt);
        findViewById(R.id.writeBtn).setOnClickListener(this);
        findViewById(R.id.cancelBtn).setOnClickListener(this);
        findViewById(R.id.pauseBtn).setOnClickListener(this);
        findViewById(R.id.resumeBtn).setOnClickListener(this);
        setParameter();
    }

    private void setParameter() {
        //1.创建SpeechSynthesizer对象, 第二个参数：本地合成时传InitListener
        mTts = SpeechSynthesizer.createSynthesizer(this, null);
        //2.合成参数设置，详见《科大讯飞MSC API手册(Android)》SpeechSynthesizer 类
        mTts.setParameter(SpeechConstant.VOICE_NAME, Tools.getPreferencesValue(this,Constants.VOICE,Tools.getPreferencesValue(this,Constants.VOICE,Constants.voices[0])));//设置发音人
        mTts.setParameter(SpeechConstant.SPEED, "50");//设置语速
        mTts.setParameter(SpeechConstant.VOLUME, "80");//设置音量，范围0~100
//        mTts.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_CLOUD); //设置云端
        //设置合成
//        if(isCloud)
//        {
//            //设置使用云端引擎
//            mTts.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_CLOUD);
//        }else {
//            //设置使用本地引擎
//            mTts.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_LOCAL);
//            //设置发音人资源路径
//            mTts.setParameter(ResourceUtil.TTS_RES_PATH,getResourcePath());
//        }

        mTts.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_LOCAL);

    }



//    //获取发音人资源路径
//    private String getResourcePath(){
//        StringBuffer tempBuffer = new StringBuffer();
//        //合成通用资源
//        tempBuffer.append(ResourceUtil.generateResourcePath(this, ResourceUtil.RESOURCE_TYPE.assets, "tts/common.jet"));
//        tempBuffer.append(";");
//        //发音人资源
//        tempBuffer.append(ResourceUtil.generateResourcePath(this, ResourceUtil.RESOURCE_TYPE.assets, "tts/"+Tools.getPreferencesValue(this,Constants.VOICE,Constants.voices[0])+".jet"));
//        return tempBuffer.toString();
//    }

    @Override
    public void onClick(View view) {
        switch (view.getId()) {
            case R.id.writeBtn:
                mTts.startSpeaking(contentEt.getText().toString(), mSynListener);
                break;
            case R.id.cancelBtn:
                mTts.stopSpeaking();
                break;
            case R.id.pauseBtn:
                mTts.pauseSpeaking();
                break;
            case R.id.resumeBtn:
                mTts.resumeSpeaking();
                break;

        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mTts.stopSpeaking();
        // 退出时释放连接
        mTts.destroy();
    }
}
