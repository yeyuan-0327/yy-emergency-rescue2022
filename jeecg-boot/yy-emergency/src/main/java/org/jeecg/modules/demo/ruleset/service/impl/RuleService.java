package org.jeecg.modules.demo.ruleset.service.impl;

import com.rule.rulemodal.PersonTest;
import org.drools.core.io.impl.UrlResource;
import org.jeecg.modules.demo.ruleset.entity.InsuranceInfo;
import org.jeecg.modules.demo.ruleset.service.IRuleService;
import org.jeecg.modules.demo.ruleset.utils.KieSessionUtils;
import org.kie.api.KieServices;
import org.kie.api.builder.KieModule;
import org.kie.api.builder.KieRepository;
import org.kie.api.definition.KiePackage;
import org.kie.api.definition.rule.Rule;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;
import org.springframework.stereotype.Service;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

@Service
public class RuleService implements IRuleService {
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
                "http://192.168.1.146:8080/kie-drools-wb/maven2/com/rule/rulemodal/1.0.0/rulemodal-1.0.0.jar";

        KieServices kieServices = KieServices.Factory.get();

        //通过Resource资源对象加载jar包
        UrlResource resource = (UrlResource) kieServices.getResources().newUrlResource(url);
        //通过Workbench提供的服务来访问maven仓库中的jar包资源，需要先进行Workbench的认证
        resource.setUsername("kie");
        resource.setPassword("kie");
        resource.setBasicAuthentication("enabled");

        //将资源转换为输入流，通过此输入流可以读取jar包数据
        InputStream inputStream = resource.getInputStream();

        //创建仓库对象，仓库对象中保存Drools的规则信息
        KieRepository repository = kieServices.getRepository();

        //通过输入流读取maven仓库中的jar包数据，包装成KieModule模块添加到仓库中
        KieModule kieModule =
                repository.
                        addKieModule(kieServices.getResources().newInputStreamResource(inputStream));

        //基于KieModule模块创建容器对象，从容器中可以获取session会话
        KieContainer kieContainer = kieServices.newKieContainer(kieModule.getReleaseId());
        KieSession session = kieContainer.newKieSession();
        KieSessionUtils.CheckRuleMetaContent(session);
        PersonTest person = new PersonTest();
        person.setAge(6);
        session.insert(person);
        session.fireAllRules();
        session.dispose();
        return null;
    }
}
