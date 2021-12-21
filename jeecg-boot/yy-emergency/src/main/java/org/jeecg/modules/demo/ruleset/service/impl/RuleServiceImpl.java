package org.jeecg.modules.demo.ruleset.service.impl;

import com.rule.rulemodal.Person;
import org.jeecg.modules.demo.ruleset.entity.InsuranceInfo;
import org.jeecg.modules.demo.ruleset.service.IRuleService;
import org.jeecg.modules.demo.utils.KieSessionUtils;
import org.kie.api.runtime.KieSession;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

/***
 * 本文件用于实现drools相关内容
 */
@Service
public class RuleServiceImpl implements IRuleService {
    private final static String ROOT_PATH = "/Users/yuanye/Documents/yy-paper2022/ant-design-vue-jeecg/public/file/";
    public List<String> insuranceInfoCheck(InsuranceInfo insuranceInfo) throws Exception{
        String filePath = "/Users/yuanye/Documents/yy-paper2022/jeecg-boot/yy-emergency/src/main/resources/insuranceInfoCheck.xls";
        KieSession session = KieSessionUtils.getKieSessionFromXLS(filePath);
        session.getAgenda().getAgendaGroup("sign").setFocus();

        session.insert(insuranceInfo);
        KieSessionUtils.CheckRuleMetaContent(session);

        List<String> listRules = new ArrayList<>();
        session.setGlobal("listRules", listRules);

        session.fireAllRules();

        return listRules;
    }

    @Override
    public List<String> jarInfoCheck() throws Exception{
        String url =
                "http://192.168.1.153:8080/kie-drools-wb/maven2/com/rule/rulemodal/1.0.0/rulemodal-1.0.0.jar";
        KieSession session = KieSessionUtils.UrlLinkReturnSession(url);
        assert session != null;
        KieSessionUtils.CheckRuleMetaContent(session);
        Person person = new Person();
        person.setAge(6);
        session.insert(person);
        session.fireAllRules();
        session.dispose();
        return null;
    }

    @Override
    public List<String> compileJarLink(List<String> postList) throws Exception{
        String url = postList.get(0);
        KieSession session = KieSessionUtils.UrlLinkReturnSession(url);
        assert session != null;
        return KieSessionUtils.CheckRuleMetaContent(session);
    }

    @Override
    public String ruleUploadExcel(MultipartFile[] multipartFiles) throws Exception{
        String savePath = "";
        for (MultipartFile i :multipartFiles){
            savePath = ROOT_PATH + i.getOriginalFilename();
            System.out.println("上传的文件：" + i.getName() + "," + i.getContentType() + "," + i.getOriginalFilename()
                            +"，保存的路径为：" + savePath);
            i.transferTo(new File(savePath));
        }
        return savePath;
    }
}
