package org.jeecg.modules.demo.dispatchmanage.mapper;

import org.apache.ibatis.annotations.Param;

import java.util.List;
import java.util.Map;

public interface DispatchMapper {
    List<Map<String, Object>> getEmergencies();

    List<Map<String, Object>> getTasks(String eId);

    String existsLocation(String tId);

    void insertDefaultLocationTask(@Param("tId")String tId,
                                   @Param("address")String address);

    String getEmergencyAddress(String eId);

    List<Map<String, Object>> getTaskLocationById(String eId);

    int updateTaskAddress(@Param("tId")Integer tId,
                             @Param("address")String address,
                             @Param("lngLat")String lngLat,
                             @Param("explain")String explain);
}
