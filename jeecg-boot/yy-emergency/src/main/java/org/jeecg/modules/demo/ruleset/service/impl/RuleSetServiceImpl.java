package org.jeecg.modules.demo.ruleset.service.impl;

import com.alibaba.fastjson.JSON;
import net.sf.json.JSONObject;
import org.jeecg.modules.demo.ruleset.entity.Rule;
import org.jeecg.modules.demo.ruleset.mapper.RuleSetMapper;
import org.jeecg.modules.demo.ruleset.service.IRuleSetService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;


@Service
public class RuleSetServiceImpl implements IRuleSetService {
    @Autowired
    private RuleSetMapper ruleSetMapper;

    @Override
    public int ruleUploadDB(LinkedHashMap<String,Object> postList)  throws Exception {
        // 初始化rule对象
        String v_d = (String) postList.get("invalid_date");
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd hh:mm:ss");
        Date invalid_date = sdf.parse(v_d.replaceAll("[ZT]"," "));
        String json= JSON.toJSONString(postList);
        JSONObject objJson = JSONObject.fromObject(json);
        Rule rule = (Rule) JSONObject.toBean(objJson,Rule.class);
        rule.setInvalid_date(invalid_date);
        rule.setUpdate(new Date());
        // 插入数据库
        ruleSetMapper.ruleUploadDB(rule);
        return rule.getId();
    }

    @Override
    public List<Map<String, Object>> getRuleList() {
        return ruleSetMapper.getRuleList();
    }

    @Override
    public boolean deleteRule(List<String> postList) {
        int len = 0;
        for(String id : postList) len += ruleSetMapper.deleteRule(id);
        return len == postList.size();
    }
}
