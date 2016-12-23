package com.caoyu.voice;

import android.content.Context;
import android.content.Intent;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.text.TextUtils;
import android.view.View;
import android.widget.Button;

import com.iflytek.cloud.SpeechConstant;
import com.iflytek.cloud.SpeechUtility;

import java.io.BufferedWriter;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
//这个是主要程序，是这个程序打开，第一个弹出来的生命周期.
public class MainActivity extends AppCompatActivity {
    private Button writeBtn, speechBtn,sendBtn,settingBtn;//这个界面中有三个按钮
    // 语记安装助手类
    ApkInstaller mInstaller;
    private Context mContext;


    @Override//验证以下方法名字是不是父类中所有的，如果没有回报错
    protected void onCreate(Bundle savedInstanceState) {//状态保存，用于再次打开是重新恢复到原来的状态
        super.onCreate(savedInstanceState);//调用父类里面oncreate的方法
//        SpeechUtility.createUtility(this, SpeechConstant.APPID + "=58009700");
//        SpeechUtility.createUtility(this, SpeechConstant.APPID + "=5456f07a");//自定义你的配置环境信息
        mContext = this;
        mInstaller = new ApkInstaller(this);
        setContentView(R.layout.activity_main);//引入R文件
        writeBtn = (Button) findViewById(R.id.writeBtn);//设置按钮，android 的用户界面一般使用xml文件做的
        // ，对应的xml文件在layout包下如果xml里放了个按钮什么的
        // 在activity中要获取该按钮就用findViewById
        speechBtn = (Button) findViewById(R.id.speechBtn);
        sendBtn = (Button) findViewById(R.id.sendBtn);

        settingBtn = (Button) findViewById(R.id.settingBtn);

        writeBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {//获取事件响应，点击响应事件
                /**
                 * 选择本地听写 判断是否安装语记,未安装则跳转到提示安装页面
                 */
                if (!SpeechUtility.getUtility().checkServiceInstalled()) {
                    mInstaller.install();
                    return;
                } else {
                    String result = FucUtil.checkLocalResource();
                    if (!TextUtils.isEmpty(result)) {
                        Tools.toastShow(mContext,result);
                        return;
                    }
                }
                Tools.startActivity(MainActivity.this, WriteActivity.class);
            }
        });

        speechBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {//同上
                /**
                 * 选择本地听写 判断是否安装语记,未安装则跳转到提示安装页面
                 */
                if (!SpeechUtility.getUtility().checkServiceInstalled()) {
                    mInstaller.install();
                    return;
                } else {
                    String result = FucUtil.checkLocalResource();
                    if (!TextUtils.isEmpty(result)) {
                        Tools.toastShow(mContext,result);
                        return;
                    }
                }
                Tools.startActivity(MainActivity.this, SpeechActivity.class);
            }
        });
        sendBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                /**
                 * 选择本地听写 判断是否安装语记,未安装则跳转到提示安装页面
                 */
                if (!SpeechUtility.getUtility().checkServiceInstalled()) {
                    mInstaller.install();
                    return;
                } else {
                    String result = FucUtil.checkLocalResource();
                    if (!TextUtils.isEmpty(result)) {
                        Tools.toastShow(mContext,result);
                        return;
                    }
                }
                Tools.startActivity(MainActivity.this, Client.class);
            }
        });
        settingBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                // 跳转到设置界面
                Intent intent = new Intent();
                intent.setClass(MainActivity.this, Setting.class);
                MainActivity.this.startActivity(intent);// 打开新界面
            }
        });

//        int count = Tools.getPreferencesCount(this);
//        if (count > 5) {
//            Tools.toastShow(this, "请购买正版");
////				outRel.setVisibility(View.GONE);
//            findViewById(R.id.outLin).setVisibility(View.GONE);
//            return;
//        } else {
//            count++;
//            Tools.savePreferencesCount(this, count);
//        }

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
    }

    private void send(){                 //定义发送函数
        new Thread(new Runnable() {
            @Override
            public void run() {
                try {                     //使用线程
                    System.out.println("Client：Connecting");
                    //IP地址和端口号（对应服务端），我这的IP是本地路由器的IP地址
                    Socket socket = new Socket("23.83.239.12", 29839);
                    //发送给服务端的消息
                    String message = "Message from Android phone";
                    try {
                        System.out.println("Client Sending: '" + message + "'");

                        //第二个参数为True则为自动flush
                        PrintWriter out = new PrintWriter(
                                new BufferedWriter(new OutputStreamWriter(
                                        socket.getOutputStream())), true);
                        out.println(message);
                        //                      out.flush();
                    } catch (Exception e) {
                        e.printStackTrace();
                    } finally {
                        //关闭Socket
                        socket.close();
                        System.out.println("Client:Socket closed");
                    }
                } catch (UnknownHostException e1) {
                    e1.printStackTrace();//打印错误信息
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }).start();

    }

}
