package org.jeecg.modules.demo.dispatchmanage.service.impl;

import org.jeecg.modules.demo.dispatchmanage.mapper.DispatchMapper;
import org.jeecg.modules.demo.dispatchmanage.service.IDispatchManageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;

@Service
public class DispatchManageImpl implements IDispatchManageService {
    @Autowired
    DispatchMapper dispatchMapper;

    @Override
    public List<Map<String, Object>> getEmergencies() {
        return dispatchMapper.getEmergencies();
    }

    @Override
    public List<Map<String, Object>> getTaskAddsByEmergencyId(List<String> postList) {
        String eId = postList.get(0);
        List<Map<String, Object>> taskList = dispatchMapper.getTasks(eId);
        for (Map<String, Object> t : taskList){
            String tId = String.valueOf(t.get("id"));
            String queryResult = dispatchMapper.existsLocation(tId);
            // 如果task不存在位置表中,那么插入险情默认的地址
            if (queryResult == null){
                String address = "";
                dispatchMapper.insertDefaultLocationTask(eId,tId,address);
            }
        }
//        System.out.println(taskList);
        return null;
    }
}
