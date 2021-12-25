package org.jeecg.modules.demo.emergencycompile.service.impl;

import com.alibaba.fastjson.JSON;
import net.sf.json.JSONObject;
import org.jeecg.modules.demo.emergencycompile.entity.Emergency;
import org.jeecg.modules.demo.emergencycompile.entity.Relation;
import org.jeecg.modules.demo.emergencycompile.entity.Task;
import org.jeecg.modules.demo.emergencycompile.mapper.CompileMapper;
import org.jeecg.modules.demo.emergencycompile.service.IEmergencyCompileService;
import org.jeecg.modules.demo.utils.KieSessionUtils;
import org.jeecg.modules.demo.utils.MultipartFileUtils;
import org.jeecg.modules.demo.utils.RegularEmergency;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.util.*;


@Service
public class EmergencyServiceImpl implements IEmergencyCompileService {

    private final static String ROOT_PATH = "/Users/yuanye/Documents/yy-paper2022/jeecg-boot/yy-emergency/src/main/java/org/jeecg/modules/demo/emergencycompile/file/";

    @Override
    public Object uploadPdf(MultipartFile[] multipartFiles) throws Exception{
        MultipartFile file = multipartFiles[0];
        String filePath = MultipartFileUtils.saveFile(ROOT_PATH,file);
        // pdf文件
        return RegularEmergency.CompileEmergencyPushEntity(filePath);
    }

    @Override
    public Object ruleFireLevelTask(LinkedHashMap<String, Object> postList) {
        String json= JSON.toJSONString(postList);
        JSONObject objJson = JSONObject.fromObject(json);
        Emergency em = (Emergency) JSONObject.toBean(objJson,Emergency.class);
        // 系统推荐
        em.setTaskAllocation("系统推荐");
        //level & task
        KieSessionUtils.ruleFireFindLevelTask(em);
        return em;
    }
    @Autowired
    CompileMapper compileMapper;

    @Override
    public int confirmEmergencyTaskPublish(LinkedHashMap<String, Object> postList) {
        String json= JSON.toJSONString(postList);
        JSONObject objJson = JSONObject.fromObject(json);
        Emergency e = (Emergency) JSONObject.toBean(objJson,Emergency.class);
        e.setState("提交");
        compileMapper.writeEmergency(e);
        // 创建子任务
        List<String> taskList = e.getTaskList();
        for (String i : taskList){
            taskAndRelationWrite(i,e.getId());
        }
        return e.getId();
    }

    @Override
    public List<Map<String, Object>> getEmergencyList() {
        List<Map<String, Object>> emergencyList = compileMapper.getEmergencyList();
        List<Map<String, Object>> res = new ArrayList<>();
        for (Map<String, Object> m : emergencyList){
            List<String> task_list = compileMapper.getTaskList((Integer) m.get("id"));
            m.put("task_list",task_list);
            res.add(m);
        }
        return res;
    }

    @Override
    public List<Map<String, Object>> getEmergenciesByType(List<String> postList) {
        String type = postList.get(0);
        return compileMapper.getEmergenciesByType(type);
    }

    @Override
    public Object getEmergencyById(List<String> postList) {
        String id = postList.get(0);
        Emergency em  = compileMapper.getEmergencyById(id);
        return em;
    }

    @Override
    public int writeTask(LinkedHashMap<String,Object> postList) {
        String name = (String) postList.get("name");
        Integer eId = Integer.parseInt((String) postList.get("emergency_id"));
        return taskAndRelationWrite(name,eId);
    }

    @Override
    public List<Map<String, Object>> getTaskByEmergencyId(List<String> postList) {
        int eId = Integer.parseInt(postList.get(0));
        List<Map<String, Object>> taskIdList = compileMapper.getTasksList(eId);
        return taskIdList;
    }

    @Override
    public boolean taskDeleteById(List<String> postList) {
        int len = 0;
        for(String id : postList) len += compileMapper.taskDeleteById(id);
        return len == postList.size();
    }

    private int taskAndRelationWrite(String name,Integer emergencyId){
        Task t = new Task(name);
        compileMapper.writeTask(t);
        Relation r = new Relation(emergencyId,t.getId());
        compileMapper.writeEmergencyTaskRelation(r);
        return t.getId();
    }
}
