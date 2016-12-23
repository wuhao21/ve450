package com.caoyu.voice;

//这是一个简单的应用程序素材

public class DataBean {
    /**
     * temperature : 30.03
     * displacement : 123.33
     * current : 321
     * wave : triangle
     * temp_high : 0
     * current_high : 0
     * block: 0
     * process: drilling hole
     */
    private String time;
    private String temperature;
    private String displacement;
    private String current;
    private String wave;
    private String temp_high;
    private String current_high;
    private String block;
    private String process;
    private String count;

    public String getTime(){return time;}

    public void setTime(String time) {this.time = time;}

    public String getTemperature() {
        return temperature;
    }

    public void setTemperature(String temperature) {
        this.temperature = temperature;
    }

    public String getDisplacement() {
        return displacement;
    }

    public void setDisplacement(String displacement) {
        this.displacement = displacement;
    }

    public String getCurrent() {
        return current;
    }

    public void setCurrent(String current) {
        this.current = current;
    }

    public String getWave() {
        return wave;
    }

    public void setWave(String wave) {
        this.wave = wave;
    }

    public String getTemp_high() {
        return temp_high;
    }

    public void setTemp_high(String temp_high) {
        this.temp_high = temp_high;
    }

    public String getCurrent_high() {
        return current_high;
    }

    public void setCurrent_high(String current_high) {
        this.current_high = current_high;
    }

    public String getBlock() {return block;}

    public void setBlock(String block) {this.block = block;}

    public String getProcess(){return process;}

    public void setProcess(String process) {this.process = process;}

    public String getCount(){return count;}

    public void setCount(String count) {this.count = count;}

}
