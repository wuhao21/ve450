package com.caoyu.voice;

import android.app.Activity;
import android.content.SharedPreferences;
import android.content.SharedPreferences.Editor;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.List;

public class Setting extends Activity {
	private Button btnsave;
	private EditText edtip;
	private EditText edtport;
	SharedPreferences sp;//轻量级数据存储，用于保存常用配置
	private String TAG="=Setting=";

	Spinner spinner;
	private List<String> data_list;
	private ArrayAdapter<String> arr_adapter;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.setting);
		btnsave = (Button) findViewById(R.id.button1);
		edtip = (EditText) findViewById(R.id.editText1);
		edtport = (EditText) findViewById(R.id.editText2);
		sp = this.getSharedPreferences("SP", MODE_PRIVATE);
		edtip.setText(sp.getString("ipstr", SocThread.ip));
		edtport.setText(sp.getString("port", ""+SocThread.port));

		btnsave.setOnClickListener(new OnClickListener() {
			@Override
			public void onClick(View v) {
				Log.i(TAG,"开始修改");
				String ip = edtip.getText().toString();//
				String port = edtport.getText().toString();//
				Editor editor = sp.edit();
				editor.putString("ipstr", ip);
				editor.putString("port", port);
				editor.commit();//保存新数据

				String value = (String)spinner.getSelectedItem();
				Tools.savePreferencesValue(Setting.this,Constants.VOICE,value);

				Toast.makeText(Setting.this,"保存成功",Toast.LENGTH_SHORT).show();
				Setting.this.finish();
				Log.i(TAG, "保存成功"+sp.getString("ipstr", "")+";"+sp.getString("port", ""));

			}
		});




		spinner = (Spinner) findViewById(R.id.spinner);

		//数据
		data_list = new ArrayList<String>();
		for (String voice : Constants.voices){
			data_list.add(voice);
		}

		//适配器
		arr_adapter= new ArrayAdapter<String>(this, android.R.layout.simple_spinner_item, data_list);
		//设置样式
		arr_adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
		//加载适配器
		spinner.setAdapter(arr_adapter);

		String defaultVoice = Tools.getPreferencesValue(this,Constants.VOICE,Constants.voices[0]);
		for (int i = 0;i<Constants.voices.length;i++){
			if (Constants.voices[i].equals(defaultVoice)){
				spinner.setSelection(i);
			}
		}
	}
}
