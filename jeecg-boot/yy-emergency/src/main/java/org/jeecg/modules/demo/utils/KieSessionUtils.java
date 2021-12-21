package org.jeecg.modules.demo.utils;

import org.drools.core.io.impl.UrlResource;
import org.drools.decisiontable.InputType;
import org.drools.decisiontable.SpreadsheetCompiler;
import org.jeecg.modules.demo.emergencycompile.entity.Emergency;
import org.kie.api.KieServices;
import org.kie.api.builder.KieModule;
import org.kie.api.builder.KieRepository;
import org.kie.api.builder.Message;
import org.kie.api.builder.Results;
import org.kie.api.definition.KiePackage;
import org.kie.api.definition.rule.Rule;
import org.kie.api.io.ResourceType;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;
import org.kie.internal.utils.KieHelper;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;

public class KieSessionUtils {
    private KieSessionUtils() {

    }
    // 把xls文件解析为String
    private static String getDRL(String realPath) throws FileNotFoundException {
        File file = new File(realPath); // 例如：C:\\abc.xls
        InputStream is = new FileInputStream(file);
        SpreadsheetCompiler compiler = new SpreadsheetCompiler();
        return compiler.compile(is, InputType.XLS);
    }

    // drl为含有内容的字符串
    private static KieSession createKieSessionFromDRL(String drl) throws Exception{
        KieHelper kieHelper = new KieHelper();
        kieHelper.addContent(drl, ResourceType.DRL);
        Results results = kieHelper.verify();
        if (results.hasMessages(Message.Level.WARNING, Message.Level.ERROR)) {
            List<Message> messages = results.getMessages(Message.Level.WARNING, Message.Level.ERROR);
            for (Message message : messages) {
                System.out.println("Error: "+message.getText());
            }
            // throw new IllegalStateException("Compilation errors were found. Check the logs.");
        }
        return kieHelper.build().newKieSession();
    }

    // realPath为Excel文件绝对路径
    public static KieSession getKieSessionFromXLS(String realPath) throws Exception {
        return createKieSessionFromDRL(getDRL(realPath));
    }

    // 显示规则文件中每一条的规则名
    public static List<String> CheckRuleMetaContent(KieSession session){
        Collection<KiePackage> kiePackages = session.getKieBase().getKiePackages();
        List<String> ans = new ArrayList<>();
        for (KiePackage kp:kiePackages){
            Collection<Rule> rules = kp.getRules();
            for(Rule rule:rules) {
                ans.add("包"+rule.getPackageName()+"规则内容为：");
                ans.add(rule.getName());
            }
        }
        return ans;
    }

    // 通过jar链接返回session
    public static KieSession UrlLinkReturnSession(String url) throws Exception{
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
        return kieContainer.newKieSession();
    }

    // 通过解析后传递过来的险情对象返回险情等级
    public static void ruleFireFindLevel(Emergency em){
        KieServices kieServices = KieServices.Factory.get();
        KieContainer kieClasspathContainer = kieServices.getKieClasspathContainer();
        KieSession kieSession = kieClasspathContainer.newKieSession();
        kieSession.getAgenda().getAgendaGroup(em.getEmergencyType()).setFocus();
        kieSession.insert(em);
        kieSession.fireAllRules();
        kieSession.dispose();
    }
}
