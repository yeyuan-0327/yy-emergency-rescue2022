package org.jeecg.modules.demo.ruleset.entity;

import java.util.Date;

public class Rule {
    private Integer id;
    private String name;
    private String type;
    private String path;
    private String meta;
    private String emergency_type;
    private Date invalid_date;
    private Date update;
    private String delete_flag;

    public Rule() {
    }

    public Rule(Integer id, String name, String type, String path, String meta, String emergency_type, Date invalid_date, Date update, String delete_flag) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.path = path;
        this.meta = meta;
        this.emergency_type = emergency_type;
        this.invalid_date = invalid_date;
        this.update = update;
        this.delete_flag = delete_flag;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getPath() {
        return path;
    }

    public void setPath(String path) {
        this.path = path;
    }

    public String getMeta() {
        return meta;
    }

    public void setMeta(String meta) {
        this.meta = meta;
    }

    public String getEmergency_type() {
        return emergency_type;
    }

    public void setEmergency_type(String emergency_type) {
        this.emergency_type = emergency_type;
    }

    public Date getInvalid_date() {
        return invalid_date;
    }

    public void setInvalid_date(Date invalid_date) {
        this.invalid_date = invalid_date;
    }

    public Date getUpdate() {
        return update;
    }

    public void setUpdate(Date update) {
        this.update = update;
    }

    public String getDelete_flag() {
        return delete_flag;
    }

    public void setDelete_flag(String delete_flag) {
        this.delete_flag = delete_flag;
    }

    @Override
    public String toString() {
        return "Rule{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", type='" + type + '\'' +
                ", path='" + path + '\'' +
                ", meta='" + meta + '\'' +
                ", emergency_type='" + emergency_type + '\'' +
                ", invalid_date=" + invalid_date +
                ", update=" + update +
                ", delete_flag='" + delete_flag + '\'' +
                '}';
    }
}
