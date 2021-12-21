package org.jeecg.modules.demo.emergencycompile.controller;

import lombok.extern.slf4j.Slf4j;
import org.jeecg.common.api.vo.Result;
import org.jeecg.modules.demo.emergencycompile.service.IEmergencyCompileService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

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
            System.out.println("pdf文件上传api");
        }
        return Result.OK(res);
    }
}
