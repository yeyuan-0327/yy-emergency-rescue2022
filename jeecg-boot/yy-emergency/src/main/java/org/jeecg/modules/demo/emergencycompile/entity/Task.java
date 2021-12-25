package org.jeecg.modules.demo.emergencycompile.entity;

public class Task {
    private Integer id;
    private String name;
    private int statue;
    private int delete_flag;

    public Task() {
    }

    @Override
    public String toString() {
        return "Task{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", statue=" + statue +
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

    public int getStatue() {
        return statue;
    }

    public void setStatue(int statue) {
        this.statue = statue;
    }

    public int getDelete_flag() {
        return delete_flag;
    }

    public void setDelete_flag(int delete_flag) {
        this.delete_flag = delete_flag;
    }

    public Task(Integer id, String name, int statue, int delete_flag) {
        this.id = id;
        this.name = name;
        this.statue = statue;
        this.delete_flag = delete_flag;
    }

    public Task(String name) {
        this.name = name;
    }

}
