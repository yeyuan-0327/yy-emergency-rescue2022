package org.jeecg.modules.demo.emergencycompile.entity;

import java.util.Date;

public class Emergency {
    private String name;
    private String emergencyType;
    private String emergencyLevel;
    private String address;
    private String content;
    private String state;
    private Date time;
    private boolean death;
    private boolean injury;
    private boolean loss;
    private int deathNum;
    private int injuryNum;
    private int lossNum;

    public Emergency() {
    }

    @Override
    public String toString() {
        return "Emergency{" +
                "name='" + name + '\'' +
                ", emergencyType='" + emergencyType + '\'' +
                ", emergencyLevel='" + emergencyLevel + '\'' +
                ", address='" + address + '\'' +
                ", content='" + content + '\'' +
                ", state='" + state + '\'' +
                ", time=" + time +
                ", death=" + death +
                ", injury=" + injury +
                ", loss=" + loss +
                ", deathNum=" + deathNum +
                ", injuryNum=" + injuryNum +
                ", lossNum=" + lossNum +
                '}';
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getEmergencyType() {
        return emergencyType;
    }

    public void setEmergencyType(String emergencyType) {
        this.emergencyType = emergencyType;
    }

    public String getEmergencyLevel() {
        return emergencyLevel;
    }

    public void setEmergencyLevel(String emergencyLevel) {
        this.emergencyLevel = emergencyLevel;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public String getState() {
        return state;
    }

    public void setState(String state) {
        this.state = state;
    }

    public Date getTime() {
        return time;
    }

    public void setTime(Date time) {
        this.time = time;
    }

    public boolean isDeath() {
        return death;
    }

    public void setDeath(boolean death) {
        this.death = death;
    }

    public boolean isInjury() {
        return injury;
    }

    public void setInjury(boolean injury) {
        this.injury = injury;
    }

    public boolean isLoss() {
        return loss;
    }

    public void setLoss(boolean loss) {
        this.loss = loss;
    }

    public int getDeathNum() {
        return deathNum;
    }

    public void setDeathNum(int deathNum) {
        this.deathNum = deathNum;
    }

    public int getInjuryNum() {
        return injuryNum;
    }

    public void setInjuryNum(int injuryNum) {
        this.injuryNum = injuryNum;
    }

    public int getLossNum() {
        return lossNum;
    }

    public void setLossNum(int lossNum) {
        this.lossNum = lossNum;
    }

    public Emergency(String name, String emergencyType, String emergencyLevel, String address, String content, String state, Date time, boolean death, boolean injury, boolean loss, int deathNum, int injuryNum, int lossNum) {
        this.name = name;
        this.emergencyType = emergencyType;
        this.emergencyLevel = emergencyLevel;
        this.address = address;
        this.content = content;
        this.state = state;
        this.time = time;
        this.death = death;
        this.injury = injury;
        this.loss = loss;
        this.deathNum = deathNum;
        this.injuryNum = injuryNum;
        this.lossNum = lossNum;
    }
}
