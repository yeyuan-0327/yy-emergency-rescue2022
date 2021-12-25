package org.jeecg.modules.demo.emergencycompile.controller;

import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.api.vo.Result;
import org.jeecg.modules.demo.emergencycompile.entity.Task;
import org.jeecg.modules.demo.emergencycompile.service.IEmergencyCompileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

@RequestMapping("/emergencyCompile")
@RestController
@Slf4j
public class EmergencyCompileController {
    @Autowired
    IEmergencyCompileService iEmergencyCompileService;

    @RequestMapping(value = "/emergencyUpload/uploadEmergencyFile", method = RequestMethod.POST)
    public Result<?> uploadFile(@RequestBody MultipartFile[] multipartFiles) throws Exception{
        String fileType = "pdf";
        Object res = new Object();
        if (fileType.equals("pdf")) {
            res = iEmergencyCompileService.uploadPdf(multipartFiles);
        }
        return Result.OK(res);
    }

    @RequestMapping(value = "/emergencyUpload/ruleFireLevelTask", method = RequestMethod.POST)
    public Result<?> ruleFireLevelTask(@RequestBody LinkedHashMap<String,Object> postList) {
        Object res = iEmergencyCompileService.ruleFireLevelTask(postList);
        return Result.OK(res);
    }

    @RequestMapping(value = "/emergencyUpload/confirmEmergencyTaskPublish", method = RequestMethod.POST)
    public Result<?> confirmEmergencyTaskPublish(@RequestBody LinkedHashMap<String,Object> postList) {
        int last_id = iEmergencyCompileService.confirmEmergencyTaskPublish(postList);
        return Result.OK(last_id);
    }

    @GetMapping("/emergencyUpload/emergencyList")
    public Result<?> getEmergencyList() {
        List<Map<String, Object>> res = iEmergencyCompileService.getEmergencyList();
        return Result.OK(res);
    }

    @RequestMapping(value = "/taskCreate/getEmergenciesByType", method = RequestMethod.POST)
    public Result<?> getEmergenciesByType(@RequestBody List<String> postList) {
        List<Map<String, Object>> res = iEmergencyCompileService.getEmergenciesByType(postList);
        return Result.OK(res);
    }

    @RequestMapping(value = "/taskCreate/getEmergencyById", method = RequestMethod.POST)
    public Result<?> getEmergencyById(@RequestBody List<String> postList) {
        Object res = iEmergencyCompileService.getEmergencyById(postList);
        return Result.OK(res);
    }

    @RequestMapping(value = "/taskCreate/writeTask", method = RequestMethod.POST)
    public Result<?> writeTask(@RequestBody LinkedHashMap<String,Object> postList) {
        int last_id = iEmergencyCompileService.writeTask(postList);
        return Result.OK(last_id);
    }

    @RequestMapping(value = "/emergencyStatue/getTaskByEmergencyId", method = RequestMethod.POST)
    public Result<?> getTaskByEmergencyId(@RequestBody List<String> postList) {
        List<Map<String, Object>> res = iEmergencyCompileService.getTaskByEmergencyId(postList);
        return Result.OK(res);
    }

    @RequestMapping(value = "/emergencyStatue/taskDeleteById", method = RequestMethod.POST)
    public Result<?> taskDeleteById(@RequestBody List<String> postList) {
        boolean res = iEmergencyCompileService.taskDeleteById(postList);
        return Result.OK(res);
    }
}
