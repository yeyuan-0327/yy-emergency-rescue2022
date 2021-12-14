package org.jeecg.modules.demo.ruleset.service.impl;

import com.rule.rulemodal.Person;
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

/***
 * 本文件用于实现drools相关内容
 */
@Service
public class RuleServiceImpl implements IRuleService {
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
}
