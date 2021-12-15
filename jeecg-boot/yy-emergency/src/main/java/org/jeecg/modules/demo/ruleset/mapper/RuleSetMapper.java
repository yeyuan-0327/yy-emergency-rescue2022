package org.jeecg.modules.demo.ruleset.mapper;

import org.apache.ibatis.annotations.Param;
import org.jeecg.modules.demo.ruleset.entity.Rule;

import java.util.List;
import java.util.Map;

public interface RuleSetMapper {
    void ruleUploadDB(Rule rule);

    List<Map<String, Object>> getRuleList();

    int deleteRule(@Param("id")String id);
}
