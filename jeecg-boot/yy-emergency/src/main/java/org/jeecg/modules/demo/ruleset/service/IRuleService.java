package org.jeecg.modules.demo.ruleset.service;

import org.jeecg.modules.demo.ruleset.entity.InsuranceInfo;
import org.springframework.web.multipart.MultipartFile;

import java.util.List;

public interface IRuleService {
    List<String> insuranceInfoCheck(InsuranceInfo insuranceInfo) throws Exception;

    List<String> jarInfoCheck() throws Exception;

    List<String> compileJarLink(List<String> postList) throws Exception;

    String ruleUploadExcel(MultipartFile[] multipartFiles) throws Exception;
}
