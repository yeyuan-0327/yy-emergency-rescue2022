package org.jeecg.modules.demo.dispatchmanage.controller;

import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.api.vo.Result;
import org.jeecg.modules.demo.dispatchmanage.service.IDispatchManageService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.*;

@RequestMapping("/dispatchManage")
@RestController
@Slf4j
public class DispatchManageController {
    @Autowired
    IDispatchManageService iDispatchManageService;

    @GetMapping("/locationSelect/getEmergencies")
    public Result<?> getEmergencies() {
        List<Map<String, Object>> res = iDispatchManageService.getEmergencies();
        return Result.OK(res);
    }

    @RequestMapping(value = "/locationSelect/getTaskAddsByEmergencyId", method = RequestMethod.POST)
    public Result<?> getTaskAddsByEmergencyId(@RequestBody List<String> postList) {
        List<Map<String, Object>> res = iDispatchManageService.getTaskAddsByEmergencyId(postList);
        return Result.OK(res);
    }
}
