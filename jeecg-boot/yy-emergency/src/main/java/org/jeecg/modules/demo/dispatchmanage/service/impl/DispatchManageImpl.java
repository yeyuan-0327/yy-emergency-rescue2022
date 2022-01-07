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
        String emergencyAddress = dispatchMapper.getEmergencyAddress(eId);
        for (Map<String, Object> t : taskList){
            String tId = String.valueOf(t.get("id"));
            String queryResult = dispatchMapper.existsLocation(tId);
            // 如果task不存在位置表中,那么插入险情默认的地址
            if (queryResult == null){
                dispatchMapper.insertDefaultLocationTask(tId,emergencyAddress);
            }
        }
        List<Map<String, Object>> result = dispatchMapper.getTaskLocationById(eId);
        return result;
    }

    @Override
    public int updateTaskAddress(List<String> postList) {
        Integer tId = Integer.valueOf(postList.get(0));
        String taskAddress = postList.get(1);
        String lngLat = postList.get(2);
        String explain = postList.get(3);
        int res = dispatchMapper.updateTaskAddress(tId,taskAddress,lngLat,explain);
        return res;
    }
}
