package org.jeecg.modules.demo.emergencycompile.entity;

public class Task {
    private Integer id;
    private String name;
    private int statue;

    public Task() {
    }

    @Override
    public String toString() {
        return "Task{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", statue=" + statue +
                '}';
    }

    public Task(String name, int statue) {
        this.name = name;
        this.statue = statue;
    }

    public Task(Integer id, String name, int statue) {
        this.id = id;
        this.name = name;
        this.statue = statue;
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
}
