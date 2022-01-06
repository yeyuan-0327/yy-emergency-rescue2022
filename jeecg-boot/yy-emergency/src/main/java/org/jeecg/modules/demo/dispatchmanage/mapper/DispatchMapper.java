package org.jeecg.modules.demo.dispatchmanage.mapper;

import java.util.List;
import java.util.Map;

public interface DispatchMapper {
    List<Map<String, Object>> getEmergencies();

    List<Map<String, Object>> getTasks(String eId);

    String existsLocation(String tId);

    void insertDefaultLocationTask(String eId, String tId, String address);
}
