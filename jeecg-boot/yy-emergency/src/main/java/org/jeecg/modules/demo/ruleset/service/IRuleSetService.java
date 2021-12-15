package org.jeecg.modules.demo.ruleset.service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public interface IRuleSetService {
    int ruleUploadDB(LinkedHashMap<String,Object> postList) throws Exception;

    List<Map<String, Object>> getRuleList();

    boolean deleteRule(List<String> postList);
}
