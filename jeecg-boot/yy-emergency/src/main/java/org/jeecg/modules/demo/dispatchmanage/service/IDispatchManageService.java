package org.jeecg.modules.demo.dispatchmanage.service;

import java.util.List;
import java.util.Map;

public interface IDispatchManageService {
    List<Map<String, Object>> getEmergencies();

    List<Map<String, Object>> getTaskAddsByEmergencyId(List<String> postList);

    int updateTaskAddress(List<String> postList);
}
