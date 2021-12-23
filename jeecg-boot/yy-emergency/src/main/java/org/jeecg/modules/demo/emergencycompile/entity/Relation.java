package org.jeecg.modules.demo.emergencycompile.entity;

public class Relation {
    private Integer id;
    private Integer emergency_id;
    private Integer task_id;

    @Override
    public String toString() {
        return "Relation{" +
                "id=" + id +
                ", emergency_id=" + emergency_id +
                ", task_id=" + task_id +
                '}';
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Integer getEmergency_id() {
        return emergency_id;
    }

    public void setEmergency_id(Integer emergency_id) {
        this.emergency_id = emergency_id;
    }

    public Integer getTask_id() {
        return task_id;
    }

    public void setTask_id(Integer task_id) {
        this.task_id = task_id;
    }

    public Relation() {
    }

    public Relation(Integer emergency_id, Integer task_id) {
        this.emergency_id = emergency_id;
        this.task_id = task_id;
    }

    public Relation(Integer id, Integer emergency_id, Integer task_id) {
        this.id = id;
        this.emergency_id = emergency_id;
        this.task_id = task_id;
    }
}
