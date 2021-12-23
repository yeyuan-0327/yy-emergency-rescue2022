package org.jeecg.modules.demo.emergencycompile.entity;

public class Task {
    private Integer id;
    private String name;

    public Task() {
    }

    public Task(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Task{" +
                "id=" + id +
                ", name='" + name + '\'' +
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

    public Task(Integer id, String name) {
        this.id = id;
        this.name = name;
    }
}
