package org.jeecg.modules.demo.emergencycompile.service;

import org.springframework.web.multipart.MultipartFile;

public interface IEmergencyCompileService {
    Object uploadPdf(MultipartFile[] multipartFiles) throws Exception;
}
