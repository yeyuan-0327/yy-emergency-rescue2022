package org.jeecg.modules.demo.ruleset.entity;

import java.util.Date;

public class Rule {
    private Integer id;
    private String name;
    private String type;
    private String path;
    private String meta;
    private String task_type;
    private Date invalid_date;
    private Date update;
    private int delete_flag ;

    public Rule() {
    }

    @Override
    public String toString() {
        return "Rule{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", type='" + type + '\'' +
                ", path='" + path + '\'' +
                ", meta='" + meta + '\'' +
                ", task_type='" + task_type + '\'' +
                ", invalid_date=" + invalid_date +
                ", update=" + update +
                ", delete_flag=" + delete_flag +
                '}';
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

    public String getTask_type() {
        return task_type;
    }

    public void setTask_type(String task_type) {
        this.task_type = task_type;
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

    public int getDelete_flag() {
        return delete_flag;
    }

    public void setDelete_flag(int delete_flag) {
        this.delete_flag = delete_flag;
    }

    public Rule(Integer id, String name, String type, String path, String meta, String task_type, Date invalid_date, Date update, int delete_flag) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.path = path;
        this.meta = meta;
        this.task_type = task_type;
        this.invalid_date = invalid_date;
        this.update = update;
        this.delete_flag = delete_flag;
    }
}
