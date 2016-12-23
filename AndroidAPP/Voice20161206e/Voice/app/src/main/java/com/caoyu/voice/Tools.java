package com.caoyu.voice;
//这个文件夹里面陈列了一些会常常用到的小工具。

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.os.Bundle;
import android.telephony.TelephonyManager;
import android.view.View;
import android.widget.Toast;

import java.math.BigDecimal;
import java.text.DecimalFormat;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.HashSet;
import java.util.List;

public class Tools {
    /**
     * 是否弹出输入法
     * WindowManager.LayoutParams.SOFT_INPUT_STATE_HIDDEN
     *
     * @param activity
     */
    public static void setSoftInputMode(Activity activity, int mode) {
        activity.getWindow().setSoftInputMode(mode);
    }

    //把view转化为图片
    public static Bitmap getBitmapFromView(View view) {
        view.destroyDrawingCache();
        view.measure(View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED), View.MeasureSpec.makeMeasureSpec(0, View.MeasureSpec.UNSPECIFIED));
        view.layout(0, 0, view.getMeasuredWidth(), view.getMeasuredHeight());
        view.setDrawingCacheEnabled(true);
        Bitmap bitmap = view.getDrawingCache(true);
        return bitmap;
    }


    //检查应用是否含有某个权限
    public static boolean isGetPermission(Context context, String permission) {
        PackageManager pm = context.getPackageManager();
        boolean isGet = (PackageManager.PERMISSION_GRANTED == pm.checkPermission(permission, context.getPackageName()));
        return isGet;
    }

    public static void startActivity(Activity nowActivity, Class<?> desClass) {
        Intent intent = new Intent(nowActivity, desClass);
        nowActivity.startActivity(intent);
    }

    //根据距离来判断单位和保留的小数
    public static String getFormatLength(double lenMeter, boolean isKmType) {

        if (lenMeter > 1000) {
            float dis = (float) lenMeter / 1000;
            DecimalFormat fnum = new DecimalFormat("##0.0");
            String dstr = fnum.format(dis);
            if (isKmType) {
                return "" + dstr + "KM";
            } else {
                return "" + dstr + "公里";
            }
        }

        int dis = (int) lenMeter / 10 * 10;
        if (isKmType) {
            return "" + dis + "M";
        } else {
            return "" + dis + "米";
        }
    }

//    //根据距离来判断单位和保留的小数
//    public static String getFormatLength(double lenMeter) {
//        if (lenMeter > 10000) // 10 km
//        {
//            int dis = (int) lenMeter / 1000;
//            return "" + dis;
//        }
//
//        if (lenMeter > 1000) {
//            float dis = (float) lenMeter / 1000;
//            DecimalFormat fnum = new DecimalFormat("##0.0");
//            String dstr = fnum.format(dis);
//            return "" + dstr;
//        }
//
//        if (lenMeter > 100) {
//            int dis = (int) lenMeter / 50 * 50;
//            return "" + dis;
//        }
//
//        int dis = (int) lenMeter / 10 * 10;
////        if (dis == 0) {
////            dis = 10;
////        }
//
//        return "" + dis;
//    }

    /**
     * 保留几位小数
     */
    public static float keepFloatCount(float value, int count) {
        BigDecimal b = new BigDecimal(value);
        float f1 = (float) b.setScale(count, BigDecimal.ROUND_HALF_UP)
                .doubleValue();
        return f1;
    }


    /**
     * 保证一个整数至少有几位
     */
    public static String keepIntCount(int value, int count) {
        String retrunValue = String.format("%0" + count + "d", value);
        return retrunValue;
    }

    /**
     * 保证一个float至少有几位
     */
    public static String keepFloatCountTwo(float value) {
        DecimalFormat df = new DecimalFormat("#####0.00");
        String str = df.format(value);
        return str;
    }

    /**
     * @param activity 当前context
     * @param cls      目标activity
     */
    public static void startUpAct(Activity activity, Class<?> cls, boolean isFinish,
                                  Bundle bundle) {
        Intent intent = new Intent();
        if (bundle != null) {
            intent.putExtras(bundle);
        }
        intent.setClass(activity, cls);
        activity.startActivity(intent);
        if (isFinish) {
            activity.finish();
        }
    }


    /**
     * 将ip的整数形式转换成ip形式
     *
     * @param ipInt
     * @return
     */
    public static String int2ip(int ipInt) {
        StringBuilder sb = new StringBuilder();
        sb.append(ipInt & 0xFF).append(".");
        sb.append((ipInt >> 8) & 0xFF).append(".");
        sb.append((ipInt >> 16) & 0xFF).append(".");
        sb.append((ipInt >> 24) & 0xFF);
        return sb.toString();
    }

    /**
     * 将php端返回的时间戳转换成Date类型
     *
     * @param time php端时间戳
     * @return java本地的Date对象
     * @author zhaozhijun
     */
    public static Date convertTimeStampFromPHP(long time) {
        Date date = new Date();
        if (new String(time + "").length() == 10) {
            //php端的时间戳没有毫秒，手动加3个0进去
            date.setTime(Long.decode(time + "000"));
        }
        return date;
    }


    /**
     * 保留最后几位
     */
    public static String keepLastString(String value, int count) {
        if (value == null && value.equals("")) {
            return value;
        }
        if (value.length() <= count) {
            return value;
        }
        String keepStr = value.substring(value.length() - count, value.length());
        return keepStr;
    }

    /**
     * 将php返回的以秒作单位的int型时间戳，转成ms单位的对应日期格式的字符串
     *
     * @param phpTime      服务器返回时间戳(秒)
     * @param formatString eg:MM月dd日
     * @return string
     * @author chenyouren
     */
    public static String phpTimeFormatToString(int phpTime, String formatString) {
        long time = 1000;
        time *= phpTime;
        SimpleDateFormat format = new SimpleDateFormat(formatString);
        return format.format(new Date(time));
    }


    /**
     * 判断string是否为null，或者“”
     */
    public static boolean isNullString(String value) {
        if (value != null && !value.equals("")) {
            return false;
        } else {
            return true;
        }
    }


    public static List<String> getAtoZletter() {
        String[] letterArr = new String[]{"A", "B", "C", "D", "E", "F", "G", "H", "J", "K", "L", "M", "N", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"};
        List<String> data = new ArrayList<String>();
        Collections.addAll(data, letterArr);
        return data;
    }

    public static void removeDuplicate(List list) {
        HashSet h = new HashSet(list);
        list.clear();
        list.addAll(h);
    }

    public static boolean isCanUseSim(Context context) {
        try {
            TelephonyManager mgr = (TelephonyManager) context.getSystemService(Context.TELEPHONY_SERVICE);

            return TelephonyManager.SIM_STATE_READY == mgr
                    .getSimState();
        } catch (Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    public static String hideNum(String num, int beforeShow, int afterShow) {
        String hideNum = num;
        if (Tools.isNullString(num) || num.length() <= (beforeShow + afterShow)) {
            return hideNum;
        }
        int hideCount = num.length() - beforeShow - afterShow;
        String middleStr = "";
        if (hideCount > 0) {
            for (int i = 0; i < hideCount; i++) {
                middleStr += "*";
            }
        }
        hideNum = num.substring(0, beforeShow) + middleStr + num.substring(num.length() - afterShow, num.length());
        return hideNum;
    }

    public static boolean containWords(String word, String keyword) {
        if (!isNullString(word) && !isNullString(keyword)) {
            if (word.contains(keyword)){
                return true;
            }
        }
        return false;
    }

    public static void savePreferencesValue(Context context, String name, String value) {
        SharedPreferences preferences = context.getSharedPreferences(Constants.SP_NAME, Context.MODE_WORLD_READABLE);
        SharedPreferences.Editor editor = preferences.edit();
        editor.putString(name, value);
        editor.commit();
    }

    public static String getPreferencesValue(Context context, String name, String defaultValue) {
        SharedPreferences preferences = context.getSharedPreferences(Constants.SP_NAME, Context.MODE_WORLD_READABLE);
        return preferences.getString(name, defaultValue);
    }

    public static void savePreferencesCount(Context context, int count){
        SharedPreferences preferences = context.getSharedPreferences(Constants.SP_NAME, Context.MODE_WORLD_READABLE);
        SharedPreferences.Editor editor = preferences.edit();
        editor.putInt("count", count);
        editor.commit();
    }

    public static int getPreferencesCount(Context context){
        SharedPreferences preferences = context.getSharedPreferences(Constants.SP_NAME, Context.MODE_WORLD_READABLE);
        return preferences.getInt("count", 0);
    }

    public static void toastShow(Context context, String showText){
        Toast.makeText(context,showText, Toast.LENGTH_SHORT).show();
    }

}
