package org.jeecg.modules.demo.ruleset.service;

import java.util.LinkedHashMap;

public interface IRuleSetService {
    int ruleUploadDB(LinkedHashMap<String,Object> postList) throws Exception;
}
