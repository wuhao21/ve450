package com.caoyu.voice;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.os.Message;
import android.text.TextUtils;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;
import android.widget.Toast;

import com.iflytek.cloud.ErrorCode;
import com.iflytek.cloud.InitListener;
import com.iflytek.cloud.RecognizerResult;
import com.iflytek.cloud.SpeechConstant;
import com.iflytek.cloud.SpeechError;
import com.iflytek.cloud.SpeechRecognizer;
import com.iflytek.cloud.SpeechSynthesizer;
import com.iflytek.cloud.SpeechUtility;
import com.iflytek.cloud.SynthesizerListener;
import com.iflytek.cloud.ui.RecognizerDialog;
import com.iflytek.cloud.ui.RecognizerDialogListener;
import com.iflytek.cloud.util.ResourceUtil;

import org.json.JSONArray;
import org.json.JSONObject;
import org.json.JSONTokener;

import java.io.BufferedReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.ArrayList;
import java.util.List;

//用socket的部分,accessed at http://blog.csdn.net/w495800598/article/details/45169729 on Nov 1st.
public class Client extends Activity {//继承了activity的class可以使用，修改activity
    private String TAG = "===Client===";
    private String TAG1 = "===Send===";
    private TextView tv1 = null;
    Handler mhandler;//消息的封装者和处理者，handler负责将需要传递的信息封装成Message，
    // 通过调用handler对象的obtainMessage()来实现；
    // 将消息传递给Looper，这是通过handler对象的sendMessage()来实现的。
    // 继而由Looper将Message放入MessageQueue中。当Looper对象看到MessageQueue中含有Message，
    // 就将其广播出去。该handler对象收到该消息后，调用相应的handler对象的handleMessage()方法对其进行处理。
    Handler mhandlerSend;
    boolean isRun = true;
    EditText edtsendms;
    Button btnsend;
    private String sendstr = "";
    SharedPreferences sp;
    Button speechBtn;
    private Context ctx;
    Socket socket;
    PrintWriter out;
    BufferedReader in;
    SocThread socketThread;
    boolean finishread = true;

    DataBean dataBean = new DataBean();
    TextView tv_time,tv_temperature,tv_current,tv_displacement,tv_waveform,tv_process,tv_count;
    TextView tv_warning;
    //TextView tv_time1,tv_temperature1,tv_current1,tv_displacement1,tv_waveform1,tv_process1,tv_count1;
    private List<String> dataList= new ArrayList<>();


    private TextView tv_speek;
    private boolean isCloud = false;
    // 语音听写对象
    private SpeechRecognizer mIat;
    // 语音听写UI
    private RecognizerDialog mIatDialog;
    // 语记安装助手类
    ApkInstaller mInstaller;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        mToast = Toast.makeText(this, "", Toast.LENGTH_SHORT);
        setVoiceParameter();
        setContentView(R.layout.client);
        tv1 = (TextView) findViewById(R.id.tv1);
        btnsend = (Button) findViewById(R.id.button1);
        tv_time=(TextView) findViewById(R.id.tv_time);

        // 初始化识别无UI识别对象
        // 使用SpeechRecognizer对象，可根据回调消息自定义界面；
        mIat = SpeechRecognizer.createRecognizer(this, mInitListener);

        // 初始化听写Dialog，如果只使用有UI听写功能，无需创建SpeechRecognizer
        // 使用UI听写功能，请根据sdk文件目录下的notice.txt,放置布局文件和图片资源
        mIatDialog = new RecognizerDialog(this, mInitListener);
        mInstaller = new ApkInstaller(this);

       // tv_temperature1 = (TextView) findViewById(R.id.tv_temperature);
      //  tv_current1 = (TextView) findViewById(R.id.tv_current);
      //  tv_displacement1 = (TextView) findViewById(R.id.tv_displacement);
      //  tv_waveform1 = (TextView) findViewById(R.id.tv_waveform);
      //  tv_process1 = (TextView) findViewById(R.id.tv_process);
      //  tv_count1 = (TextView) findViewById(R.id.tv_count);

        tv_temperature = (TextView) findViewById(R.id.tv_temperature);
        tv_current = (TextView) findViewById(R.id.tv_current);
        tv_displacement = (TextView) findViewById(R.id.tv_displacement);
        tv_waveform = (TextView) findViewById(R.id.tv_waveform);
        tv_process = (TextView) findViewById(R.id.tv_process);
        tv_count = (TextView) findViewById(R.id.tv_count);
        tv_warning = (TextView) findViewById(R.id.tv_warning);
        ctx = Client.this;
        edtsendms = (EditText) findViewById(R.id.editText1);
        mhandler = new Handler() {
            @Override
            public void handleMessage(Message msg) {
                try {
                    MyLog.i(TAG, "mhandler接收到msg=" + msg.what);
                    if (msg.obj != null) {
                        String s = msg.obj.toString();
                        if (s.trim().length() > 0) {
                            MyLog.i(TAG, "mhandler接收到obj=" + s);
                            MyLog.i(TAG, "开始更新UI");
							if (dataList.size() >2){
                                dataList.remove(0);
                            }
                            dataList.add(s);
                            StringBuffer sb = new StringBuffer();
                            for (String item : dataList){
                                sb.append("\n"+item);
                            }
                            tv1.setText("" + sb.toString());
                            parseData(s);
                            MyLog.i(TAG, "更新UI完毕");
                        } else {
                            Log.i(TAG, "没有数据返回不更新");
                        }
                    }
                } catch (Exception ee) {
                    MyLog.i(TAG, "加载过程出现异常");
                    ee.printStackTrace();
                }
            }
        };
        mhandlerSend = new Handler() {
            @Override
            public void handleMessage(Message msg) {
				try {
					MyLog.i(TAG, "mhandlerSend接收到msg.what=" + msg.what);
					String s = msg.obj.toString();
					if (msg.what == 1) {
						tv1.append("\n ME: " + s + "      发送成功");
					} else {
						tv1.append("\n ME: " + s + "     发送失败");
					}
				} catch (Exception ee) {
					MyLog.i(TAG, "加载过程出现异常");
					ee.printStackTrace();
				}
            }
        };
        startSocket();//发送数据到服务器
		btnsend.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				// 发送数据
				MyLog.i(TAG, "准备发送数据");
				sendstr = edtsendms.getText().toString().trim();
				socketThread.Send(sendstr);

			}
		});


        speechBtn = (Button) findViewById(R.id.speechBtn);

        speechBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                speak();
            }
        });

        tv_speek = (TextView) findViewById(R.id.tv_speek);

    }

    private void parseData(String data) {//数据解析
        if (!Tools.isNullString(data)) {
            try {
                JSONObject jsonObject = new JSONObject(data);
                dataBean.setTime(jsonObject.getString("time"));
                dataBean.setTemperature(jsonObject.getString("temperature"));
                dataBean.setDisplacement(jsonObject.getString("displacement"));
                dataBean.setCurrent(jsonObject.getString("current"));
                dataBean.setWave(jsonObject.getString("wave"));
                dataBean.setTemp_high(jsonObject.getString("temp_high"));
                dataBean.setCurrent_high(jsonObject.getString("current_high"));
                dataBean.setBlock(jsonObject.getString("block"));
                dataBean.setProcess(jsonObject.getString("process"));
                dataBean.setCount(jsonObject.getString("count"));
                refrushData();
            } catch (Exception e) {
                e.printStackTrace();
                Toast.makeText(this, "数据有问题", Toast.LENGTH_SHORT).show();//简易消息提示窗口
            }
        } else {
            Toast.makeText(this, "数据有问题", Toast.LENGTH_SHORT).show();
        }
    }

    private void refrushData() {
//        StringBuffer sb = new StringBuffer();
//        sb.append("温度：" + dataBean.getTemperature() + "℃");
//        sb.append("\n位移：" + dataBean.getDisplacement() + "mm");
//        sb.append("\n电流：" + dataBean.getCurrent() + "mA");
//        sb.append("\n波形：" + dataBean.getWave());
        //tv_time1.setText("Time: ");
        tv_time.setText("Time: "+ dataBean.getTime());///时间
        //tv_temperature.setText("Temperature: ");
        tv_temperature.setText("温度: "+ dataBean.getTemperature() + "℃");//温度
        //tv_displacement1.setText("Displacement: ");
        tv_displacement.setText("位移: "+ dataBean.getDisplacement() + "mm");//位移
        //tv_current1.setText("Current: ");
        tv_current.setText("电流: "+dataBean.getCurrent() + "mA");//电流
        //tv_waveform1.setText("Waveform: ");
        tv_waveform.setText("波形: "+dataBean.getWave());//波形
        //tv_process1.setText("Process: ");
        tv_process.setText("进程: "+dataBean.getProcess());//进程
        //tv_count1.setText("Count: ");
        tv_count.setText("数量: "+dataBean.getCount());//进程


//        dataBean.setCurrent_high("1");
////        dataBean.setTemp_high("1");
//这里是条件判断语句，如果解析到的数据满足一定条件，语音播报。
        //可以当读取出json字符串满足其他条件，可以任意在这里加
        if(true) {

            if (!Tools.isNullString(dataBean.getBlock()) && dataBean.getBlock().equals("1")) {
                String word = "请注意：电机堵转！";
                tv_warning.setText(word);
                mTts.startSpeaking(word, mSynListener);
                finishread=false;
                new Handler().postDelayed(new Runnable() {
                    public void run() {
                        //execute the task
                        tv_warning.setText("");
                        finishread=true;
                    }
                }, 3000);
            } else if (!Tools.isNullString(dataBean.getTemp_high()) && dataBean.getTemp_high().equals("1")) {
                String word = "请注意：温度太高";
                tv_warning.setText(word);
                mTts.startSpeaking(word, mSynListener);
                finishread=false;
                new Handler().postDelayed(new Runnable() {
                    public void run() {
                        //execute the task
                        tv_warning.setText("");
                        finishread=true;
                    }
            }, 3000);
            } else if (!Tools.isNullString(dataBean.getCurrent_high()) && dataBean.getCurrent_high().equals("1")) {
                String word = "请注意：电流太大";
                tv_warning.setText(word);
                mTts.startSpeaking(word, mSynListener);
                finishread=false;
                new Handler().postDelayed(new Runnable() {
                    public void run() {
                        //execute the task
                        tv_warning.setText("");
                        finishread=true;
                    }
                }, 3000);
            }
        }

       // if (dataBean.getBlock().equals("1")) {
        //       String word = "Rotor is blocked!";
         //     mTts.startSpeaking(word, mSynListener);
        //     } else if (dataBean.getTemp_high().equals("1")) {
        //        String word = "Temperature is too high!";
        //        mTts.startSpeaking(word, mSynListener);
        //     } else if (dataBean.getCurrent_high().equals("1")) {
        //    String word = "Current is too high!";
        //    mTts.startSpeaking(word, mSynListener);
        //     }

        //if (!Tools.isNullString(dataBean.getTemp_high()) && dataBean.getTemp_high().equals("1") && !Tools.isNullString(dataBean.getCurrent_high()) && dataBean.getCurrent_high().equals("1")&&!Tools.isNullString(dataBean.getBlock()) && dataBean.getBlock().equals("1")) {
        //    String word = "Temperature too high, Current too high, Rotor blocked!";
        //    mTts.startSpeaking(word, mSynListener);
       // } else if (!Tools.isNullString(dataBean.getTemp_high()) && dataBean.getTemp_high().equals("1")) {
        //    String word = "Temperature is too high!";
        //    mTts.startSpeaking(word, mSynListener);
       // } else if (!Tools.isNullString(dataBean.getCurrent_high()) && dataBean.getCurrent_high().equals("1")) {
        //    String word = "Current is too high!";
        //    mTts.startSpeaking(word, mSynListener);
        //} else if (!Tools.isNullString(dataBean.getBlock()) && dataBean.getBlock().equals("1")) {
        //    String word = "Rotor blocked.";
        //    mTts.startSpeaking(word, mSynListener);
        //}else if (!Tools.isNullString(dataBean.getTemp_high()) && dataBean.getTemp_high().equals("1")&&!Tools.isNullString(dataBean.getCurrent_high()) && dataBean.getCurrent_high().equals("1")) {
       //    String word = "Both temperature and current are too high!";
        //    mTts.startSpeaking(word, mSynListener);
       // }else if (!Tools.isNullString(dataBean.getTemp_high()) && dataBean.getTemp_high().equals("1")&&!Tools.isNullString(dataBean.getBlock()) && dataBean.getBlock().equals("1")) {
       //     String word = "Temperature is too high and Rotor blocked.";
       //     mTts.startSpeaking(word, mSynListener);
        //}else if (!Tools.isNullString(dataBean.getCurrent_high()) && dataBean.getCurrent_high().equals("1")&&!Tools.isNullString(dataBean.getBlock()) && dataBean.getBlock().equals("1")) {
       //     String word = "Current is too high and Rotor blocked";
        //    mTts.startSpeaking(word, mSynListener);
       // }
//        tv1.setText(sb.toString());

        sendstr = "received";//这里每次成功接收一次消息，都向服务器返回一个received.
        socketThread.Send(sendstr);
    }

    public void startSocket() {
        socketThread = new SocThread(mhandler, mhandlerSend, ctx);
        socketThread.start();
    }


    private void stopSocket() {
        socketThread.isRun = false;
        socketThread.close();
        socketThread = null;
    }

    @Override
    protected void onStart() {
        super.onStart();
    }

    @Override
    protected void onRestart() {
        super.onRestart();
        startSocket();
    }

    @Override
    protected void onResume() {
        super.onResume();
    }

    @Override
    protected void onPause() {
        super.onPause();
    }

    @Override
    protected void onStop() {
        super.onStop();
        stopSocket();
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        mTts.stopSpeaking();
        // 退出时释放连接
        mTts.destroy();

        mhandler = null;
    }


    private Toast mToast;

    private void showTip(final String str) {
        mToast.setText(str);
        mToast.show();
    }

    //语音播报
    SpeechSynthesizer mTts;

    private void setVoiceParameter() {
        //1.创建SpeechSynthesizer对象, 第二个参数：本地合成时传InitListener
        mTts = SpeechSynthesizer.createSynthesizer(this, null);
        //2.合成参数设置，详见《科大讯飞MSC API手册(Android)》SpeechSynthesizer 类
        mTts.setParameter(SpeechConstant.VOICE_NAME, Tools.getPreferencesValue(this,Constants.VOICE,Constants.voices[0]));//设置发音人
        mTts.setParameter(SpeechConstant.SPEED, "50");//设置语速
        mTts.setParameter(SpeechConstant.VOLUME, "80");//设置音量，范围0~100
        mTts.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_LOCAL); //设置云端
//设置合成音频保存位置（可自定义保存位置），保存在“./sdcard/iflytek.pcm”
//保存在SD卡需要在AndroidManifest.xml添加写SD卡权限
//如果不需要保存合成音频，注释该行代码
//        mTts.setParameter(SpeechConstant.TTS_AUDIO_PATH, "./sdcard/iflytek.pcm");
////3.开始合成
//        mTts.startSpeaking("科大讯飞，让世界聆听我们的声音", mSynListener);
    }

//    private void setVoiceParameter() {
//        //1.创建SpeechSynthesizer对象, 第二个参数：本地合成时传InitListener
//        mTts = SpeechSynthesizer.createSynthesizer(this, null);
//        //2.合成参数设置，详见《科大讯飞MSC API手册(Android)》SpeechSynthesizer 类
//        mTts.setParameter(SpeechConstant.VOICE_NAME, Tools.getPreferencesValue(this,Constants.VOICE,Constants.voices[0]));//设置发音人
//        mTts.setParameter(SpeechConstant.SPEED, "50");//设置语速
//        mTts.setParameter(SpeechConstant.VOLUME, "80");//设置音量，范围0~100
////        mTts.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_CLOUD); //设置云端
//        //设置合成
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
//    }



//    //获取发音人资源路径
//    private String getResourcePath(){
//        StringBuffer tempBuffer = new StringBuffer();
//        //合成通用资源
//        tempBuffer.append(ResourceUtil.generateResourcePath(this, ResourceUtil.RESOURCE_TYPE.assets, "tts/common.jet"));
//        tempBuffer.append(";");
//        //发音人资源
//        tempBuffer.append(ResourceUtil.generateResourcePath(this, ResourceUtil.RESOURCE_TYPE.assets, "tts/"+Constants.voices[0]+".jet"));
//        return tempBuffer.toString();
//    }

    //合成监听器
    private SynthesizerListener mSynListener = new SynthesizerListener() {
        @Override
        public void onSpeakBegin() {
            showTip("开始播报");
        }

        @Override
        public void onSpeakPaused() {
            showTip("停止播报");
        }

        @Override
        public void onSpeakResumed() {
            showTip("继续播报");
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
                showTip("结束播报");
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










//    //語音識別
//    //TODO 开始说话：
//    private void speech() {
//        RecognizerDialog dialog = new RecognizerDialog(this,null);
//        dialog.setParameter(SpeechConstant.LANGUAGE, "zh_cn");
//        dialog.setParameter(SpeechConstant.ACCENT, "mandarin");//默认输出语言是普通话
//
//        dialog.setListener(new RecognizerDialogListener() {
//            @Override
//            public void onResult(RecognizerResult recognizerResult, boolean b) {
//                Log.e("lin","b--->" + b);
//                if (!b){
//                    printResult(recognizerResult);
//                }
//            }
//            @Override
//            public void onError(SpeechError speechError) {
//            }
//        });
//        dialog.show();
//        Toast.makeText(this, "Speak aloud please.", Toast.LENGTH_SHORT).show();
//    }

    //回调结果：
    private void printResult(RecognizerResult results) {
        String text = parseIatResult(results.getResultString());
        tv_speek.setText(text);
        String word = "";
        // 自动填写地址
        if (!Tools.isNullString(text)){
            //支持子串识别
            if (Tools.containWords(text,"电流") || Tools.containWords(text,"current")){
                word = dataBean.getCurrent();
            }
            if (Tools.containWords(text,"波形") || Tools.containWords(text,"waveform")){
                word = dataBean.getWave();
            }

            if (Tools.containWords(text,"温度") || Tools.containWords(text,"temperature")){
                word = dataBean.getTemperature();
            }

            if (Tools.containWords(text,"位移") || Tools.containWords(text,"displacement")){
                word = dataBean.getDisplacement();
            }
            if (Tools.containWords(text,"进程") || Tools.containWords(text,"process")||Tools.containWords(text,"过程")){
                word = dataBean.getProcess();
            }
            if (Tools.containWords(text,"数量") || Tools.containWords(text,"count")){
                word = dataBean.getCount();
            }

//            if (text.equals("电流") || text.equals("current")){
//                    word = dataBean.getCurrent();
//            }
//            if (text.equals("波形") || text.equals("waveform")){
//                word = dataBean.getWave();
//            }
//
//            if (text.equals("温度") || text.equals("temperature")){
//                word = dataBean.getTemperature();
//            }
//
//            if (text.equals("位移") || text.equals("displacement")){
//                word = dataBean.getDisplacement();
//            }
//            if (text.equals("过程") || text.equals("process")){
//                word = dataBean.getProcess();
//            }
             Log.e("lin","word-->" + word);//打log
            if (Tools.isNullString(word)){
                mTts.startSpeaking("请重新输入", mSynListener);
            }else{
                mTts.startSpeaking(word, mSynListener);
            }

        }else{
            showTip("沒有內容");
        }
    }
    /**
     * Json结果解析类
     */
    //accessed at http://blog.csdn.net/java04/article/details/51545322
    public static String parseIatResult(String json) {
        StringBuffer ret = new StringBuffer();
        try {
            JSONTokener tokener = new JSONTokener(json);/* 此时还未读取任何json文本，直接读取就是一个JSONObject对象。
                                                     如果此时的读取位置在"temperature" : 了，那么nextValue就是"30"（String）
                    */
            JSONObject joResult = new JSONObject(tokener);
         /* 接下来的就是JSON对象的操作了 */
            JSONArray words = joResult.getJSONArray("ws");
            for (int i = 0; i < words.length(); i++) {
                // 转写结果词，默认使用第一个结果
                JSONArray items = words.getJSONObject(i).getJSONArray("cw");
                JSONObject obj = items.getJSONObject(0);
                ret.append(obj.getString("w"));
            }
        } catch (Exception e) {//异常处理代码
            e.printStackTrace();
        }
        return ret.toString();
    }


    private void speak(){
        /**
         * 选择本地听写 判断是否安装语记,未安装则跳转到提示安装页面
         */
        if (!SpeechUtility.getUtility().checkServiceInstalled()) {
            mInstaller.install();
            return;
        } else {
            String result = FucUtil.checkLocalResource();
            if (!TextUtils.isEmpty(result)) {
                Tools.toastShow(this,result);
                return;
            }
        }
        setParam();
        // 显示听写对话框
        mIatDialog.setListener(new RecognizerDialogListener() {
            @Override
            public void onResult(RecognizerResult recognizerResult, boolean b) {
                printResult(recognizerResult);
            }
            @Override
            public void onError(SpeechError speechError) {
            }
        });
        mIatDialog.show();
    }


    /**
     * 参数设置
     *
     * @return
     */
    public void setParam() {
        // 清空参数
        mIat.setParameter(SpeechConstant.PARAMS, null);

        // 设置听写引擎
        mIat.setParameter(SpeechConstant.ENGINE_TYPE, SpeechConstant.TYPE_LOCAL);
        // 设置返回结果格式
        mIat.setParameter(SpeechConstant.RESULT_TYPE, "json");


        mIat.setParameter(SpeechConstant.LANGUAGE, "zh_cn");
        mIat.setParameter(SpeechConstant.ACCENT, "mandarin");
//        String lag = mSharedPreferences.getString("iat_language_preference",
//                "mandarin");
//        if (lag.equals("en_us")) {
//            // 设置语言
//            mIat.setParameter(SpeechConstant.LANGUAGE, "en_us");
//        } else {
//            // 设置语言
//            mIat.setParameter(SpeechConstant.LANGUAGE, "zh_cn");
//            // 设置语言区域
//            mIat.setParameter(SpeechConstant.ACCENT, lag);
//        }

        // 设置语音前端点:静音超时时间，即用户多长时间不说话则当做超时处理
        mIat.setParameter(SpeechConstant.VAD_BOS, "4000");

        // 设置语音后端点:后端点静音检测时间，即用户停止说话多长时间内即认为不再输入， 自动停止录音
        mIat.setParameter(SpeechConstant.VAD_EOS, "1000");

        // 设置标点符号,设置为"0"返回结果无标点,设置为"1"返回结果有标点
        mIat.setParameter(SpeechConstant.ASR_PTT, "1");

        // 设置音频保存路径，保存音频格式支持pcm、wav，设置路径为sd卡请注意WRITE_EXTERNAL_STORAGE权限
        // 注：AUDIO_FORMAT参数语记需要更新版本才能生效
        mIat.setParameter(SpeechConstant.AUDIO_FORMAT,"wav");
        mIat.setParameter(SpeechConstant.ASR_AUDIO_PATH, Environment.getExternalStorageDirectory()+"/msc/iat.wav");
    }

    /**
     * 初始化监听器。
     */
    private InitListener mInitListener = new InitListener() {

        @Override
        public void onInit(int code) {
            if (code != ErrorCode.SUCCESS) {
                Tools.toastShow(Client.this,"初始化失败，错误码：" + code);
            }
        }
    };

}
