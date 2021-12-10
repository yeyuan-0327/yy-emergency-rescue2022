package org.jeecg.modules.demo.ruleset.controller;

import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.api.vo.Result;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("/ruleSet")
@RestController
@Slf4j

public class RuleSetController {
    @GetMapping(value = "/hello")
    public Result<String> hello() {
        Result<String> result = new Result<String>();
        result.setResult("Hello World!RuleSetTest!");
        result.setSuccess(true);
        return result;
    }
}
