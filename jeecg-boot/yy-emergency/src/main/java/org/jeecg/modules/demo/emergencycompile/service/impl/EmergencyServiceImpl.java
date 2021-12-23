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
            Task t = new Task(i);
            compileMapper.writeTask(t);
            Relation r = new Relation(e.getId(),t.getId());
            compileMapper.writeEmergencyTaskRelation(r);
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
            System.out.println(m);
            res.add(m);
        }
        return res;
    }
}
