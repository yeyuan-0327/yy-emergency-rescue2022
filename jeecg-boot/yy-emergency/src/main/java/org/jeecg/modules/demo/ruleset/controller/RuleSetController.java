package org.jeecg.modules.demo.ruleset.controller;

import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.api.vo.Result;
import org.jeecg.modules.demo.ruleset.entity.InsuranceInfo;
import org.jeecg.modules.demo.ruleset.service.IRuleService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

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

    @RequestMapping(value = "/uploadExcel", method = RequestMethod.POST)
    public Result<?> ruleUploadExcel(@RequestBody MultipartFile[] multipartFiles){
        System.out.println(multipartFiles.length);
        System.out.println(Arrays.toString(multipartFiles));
        System.out.println("excel文件上传api");
        return null;
    }
}
