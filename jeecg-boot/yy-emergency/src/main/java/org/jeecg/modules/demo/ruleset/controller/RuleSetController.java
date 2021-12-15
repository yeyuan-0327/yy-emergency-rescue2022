package org.jeecg.modules.demo.ruleset.controller;

import lombok.SneakyThrows;
import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.api.vo.Result;
import org.jeecg.modules.demo.ruleset.entity.InsuranceInfo;
import org.jeecg.modules.demo.ruleset.service.IRuleService;
import org.jeecg.modules.demo.ruleset.service.IRuleSetService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.*;

@RequestMapping("/ruleSet")
@RestController
@Slf4j

public class RuleSetController {
    //规则服务
    @Autowired
    private IRuleSetService iRuleSetService;

    @GetMapping(value = "/hello")
    public Result<String> hello() {
        Result<String> result = new Result<String>();
        result.setResult("Hello World!RuleSetTest!");
        result.setSuccess(true);
        return result;
    }
    //drools服务
    @Autowired
    private IRuleService ruleService;

    @GetMapping("/insuranceInfoCheck")
    public Result<?> insuranceInfoCheck(){
        Map map = new HashMap();

        //模拟数据，实际应为页面传递过来
        InsuranceInfo insuranceInfo = new InsuranceInfo();
        insuranceInfo.setParam1("PICC");
        insuranceInfo.setParam4("上海");
        insuranceInfo.setParam5("11");

        try {
            List<String> list = ruleService.insuranceInfoCheck(insuranceInfo);
            if(list != null && list.size() > 0){
                map.put("checkResult",false);
                map.put("msg","准入失败");
                map.put("detail",list);
            }else{
                map.put("checkResult",true);
                map.put("msg","准入成功");
            }
            return Result.OK(map);
        } catch (Exception e) {
            e.printStackTrace();
            map.put("checkResult",false);
            map.put("msg","未知错误");
            return Result.OK(map);
        }
    }

    @GetMapping("/jarInfoCheck")
    public Result<?> jarInfoCheck(){
        List<String> list = null;
        try {
            list = ruleService.jarInfoCheck();
            return Result.OK(list);
        } catch (Exception e) {
            e.printStackTrace();
            return Result.error("fail");
        }

    }
    @RequestMapping(value = "/ruleCite/compileJarLink", method = RequestMethod.POST)
    public Result<?> compileJarLink(@RequestBody List<String> postList) throws Exception{
        List<String> res = ruleService.compileJarLink(postList);
        return Result.OK(res);
    }

    @RequestMapping(value = "/ruleCite/ruleUploadExcel", method = RequestMethod.POST)
    public Result<?> ruleUploadExcel(@RequestBody MultipartFile[] multipartFiles) throws Exception{
        String savePath = ruleService.ruleUploadExcel(multipartFiles);
        System.out.println("excel文件上传api");
        return Result.OK(savePath);
    }

    @RequestMapping(value = "/ruleCite/ruleUploadDB", method = RequestMethod.POST)
    public Result<?> ruleUploadDB(@RequestBody LinkedHashMap<String,Object> postList) throws Exception {
        int last_id = iRuleSetService.ruleUploadDB(postList);
        return Result.OK(last_id);
    }

    @GetMapping("/ruleList/getRuleList")
    public Result<?> getRuleList() {
        List<Map<String, Object>> res = iRuleSetService.getRuleList();
        return Result.OK(res);
    }

    @RequestMapping(value = "/ruleList/deleteRule", method = RequestMethod.POST)
    public Result<?> deleteRule(@RequestBody List<String> postList){
        boolean res = iRuleSetService.deleteRule(postList);
        return Result.OK(res);
    }
}
