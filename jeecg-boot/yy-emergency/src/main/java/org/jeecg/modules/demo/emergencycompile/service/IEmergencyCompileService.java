package org.jeecg.modules.demo.emergencycompile.service;

import org.springframework.web.multipart.MultipartFile;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public interface IEmergencyCompileService {
    Object uploadPdf(MultipartFile[] multipartFiles) throws Exception;

    Object ruleFireLevelTask(LinkedHashMap<String, Object> postList);

    int confirmEmergencyTaskPublish(LinkedHashMap<String, Object> postList);

    List<Map<String, Object>> getEmergencyList();

}
