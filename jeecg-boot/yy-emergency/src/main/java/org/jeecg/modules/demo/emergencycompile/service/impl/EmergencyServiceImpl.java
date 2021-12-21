package org.jeecg.modules.demo.emergencycompile.service.impl;

import org.jeecg.modules.demo.emergencycompile.entity.Emergency;
import org.jeecg.modules.demo.emergencycompile.service.IEmergencyCompileService;
import org.jeecg.modules.demo.utils.KieSessionUtils;
import org.jeecg.modules.demo.utils.MultipartFileUtils;
import org.jeecg.modules.demo.utils.RegularEmergency;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;



@Service
public class EmergencyServiceImpl implements IEmergencyCompileService {
    private final static String ROOT_PATH = "/Users/yuanye/Documents/yy-paper2022/jeecg-boot/yy-emergency/src/main/java/org/jeecg/modules/demo/emergencycompile/file/";

    @Override
    public Object uploadPdf(MultipartFile[] multipartFiles) throws Exception{
        MultipartFile file = multipartFiles[0];
        String filePath = MultipartFileUtils.saveFile(ROOT_PATH,file);
        System.out.println(filePath);
        // pdf文件
        Emergency em = RegularEmergency.CompileEmergencyPushEntity(filePath);
        KieSessionUtils.ruleFireFindLevel(em);
        System.out.println(em);
        return em;
    }
}
