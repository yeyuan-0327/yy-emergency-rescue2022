package com.emergencyCompile;

import com.huaban.analysis.jieba.JiebaSegmenter;
import com.modal.ComparisonOperatorEntity;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.text.PDFTextStripperByArea;
import org.jeecg.modules.demo.emergencycompile.entity.Emergency;
import org.junit.Test;
import org.kie.api.KieServices;
import org.kie.api.runtime.KieContainer;
import org.kie.api.runtime.KieSession;

import java.io.File;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class TestEmergencyCompile {
    @Test
    public void uploadPdf() throws Exception{
        String filePath = "/Users/yuanye/Documents/yy-paper2022/jeecg-boot/yy-emergency/src/main/java/org/jeecg/modules/demo/emergencycompile/file/险情测试文件.pdf";
        PDDocument document = PDDocument.load(new File(filePath));
        if (!document.isEncrypted()) {

            PDFTextStripperByArea stripper = new PDFTextStripperByArea();
            stripper.setSortByPosition(true);

            PDFTextStripper tStripper = new PDFTextStripper();

            String pdfFileInText = tStripper.getText(document);
            // split by whitespace
            // String[] lines = pdfFileInText.split("\\r?\\n");
            Emergency em = new Emergency();
            if (em.getAddress() == null){
                Pattern p = Pattern.compile(".*?省|.*?市|.*?区|.*?镇|.*?村");
                Matcher m = p.matcher(pdfFileInText);
                StringBuilder add = new StringBuilder();
                while (m.find()) if (m.group().length()<5)add.append(m.group());
                em.setAddress(String.valueOf(add));
            }
            if (em.getName() == null){
                Pattern p = Pattern.compile("(?<!\\s).+(?=\\n)");
                Matcher m = p.matcher(pdfFileInText);
                if (m.lookingAt()) em.setName(m.group().replace(" ",""));
            }
            //
            JiebaSegmenter segmenter = new JiebaSegmenter();
            String regEx = "[\n\r\t`~!@#$%^&*()+=|{}':;',\\[\\]<>/?~！@#￥%……&*（）——+|{}【】‘；：”“’。， 、？^p]";
            String line = pdfFileInText.replaceAll(regEx, "").replaceAll("　", "").replaceAll(" ", "");
            List<String> strings = segmenter.sentenceProcess(line);
            //
            for (String i : strings){
                if (!em.isDeath() && i.equals("死亡"))em.setDeath(true);
                if (!em.isInjury()&& i.equals("受伤"))em.setInjury(true);
                if (!em.isLoss()&& i.equals("经济损失"))em.setInjury(true);
                if (em.getEmergencyType()==null && i.equals("事故"))em.setEmergencyType("事故灾难");
            }
            //
            if (em.isDeath()){
                Set<String> strSet = new HashSet<>();
                Pattern p = Pattern.compile("(\\d⼈死亡)|(死亡\\d⼈)");
                Matcher m = p.matcher(line);
                while(m.find()) strSet.add(m.group());
                for (String i : strSet){
                    Pattern p2 = Pattern.compile("\\d");
                    Matcher m2 = p2.matcher(i);
                    while (m2.find()) em.setDeathNum(Integer.parseInt(m2.group()));
                }
            }
            if (em.isInjury()){
                Set<String> strSet = new HashSet<>();
                Pattern p = Pattern.compile("(\\d⼈受伤)|(受伤\\d⼈)");
                Matcher m = p.matcher(line);
                while(m.find()) strSet.add(m.group());
                for (String i : strSet){
                    Pattern p2 = Pattern.compile("\\d");
                    Matcher m2 = p2.matcher(i);
                    while (m2.find()) em.setInjuryNum(Integer.parseInt(m2.group()));
                }
            }
            if (em.isLoss()){
                Set<String> strSet = new HashSet<>();
                Pattern p = Pattern.compile("(\\d万(直接)?经济损失)|((直接)?经济损失\\d万)|(\\d+经济损失)|(经济损失\\d+)");
                Matcher m = p.matcher(line);
                while(m.find()) strSet.add(m.group());
                for (String i : strSet){
                    Pattern p2 = Pattern.compile("\\d");
                    Matcher m2 = p2.matcher(i);
                    while (m2.find()) em.setLossNum(Integer.parseInt(m2.group()));
                }
            }
            em.setContent(line);
            em.setTime(new Date());
            ruleFireFindLevel(em);
            System.out.println(em);
        }

    }
    public static String getEncoding(String str) {
        String encode = "GB2312";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s = encode;
                return s;
            }
        } catch (Exception exception) {
        }
        encode = "ISO-8859-1";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s1 = encode;
                return s1;
            }
        } catch (Exception exception1) {
        }
        encode = "UTF-8";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s2 = encode;
                return s2;
            }
        } catch (Exception exception2) {
        }
        encode = "GBK";
        try {
            if (str.equals(new String(str.getBytes(encode), encode))) {
                String s3 = encode;
                return s3;
            }
        } catch (Exception exception3) {
        }
        return "";
    }

    public static String gb2312ToUtf8(String str) {

        String urlEncode = "" ;

        try {

            urlEncode = URLEncoder.encode (str, "UTF-8" );

        } catch (UnsupportedEncodingException e) {

            e.printStackTrace();

        }

        return urlEncode;

    }

    @Test
    public void test3(){
        KieServices kieServices = KieServices.Factory.get();
        KieContainer kieClasspathContainer = kieServices.getKieClasspathContainer();
        KieSession kieSession = kieClasspathContainer.newKieSession("KSession-rule");

        ComparisonOperatorEntity comparisonOperatorEntity = new ComparisonOperatorEntity();
        comparisonOperatorEntity.setNames("张三");
        List<String> list = new ArrayList<>();
        list.add("张三");
        list.add("李四");
        comparisonOperatorEntity.setList(list);

        //将数据提供给规则引擎，规则引擎会根据提供的数据进行规则匹配，如果规则匹配成功则执行规则
        kieSession.insert(comparisonOperatorEntity);

        kieSession.fireAllRules();
        kieSession.dispose();
    }

    private static void ruleFireFindLevel(Emergency em){
        KieServices kieServices = KieServices.Factory.get();
        KieContainer kieClasspathContainer = kieServices.getKieClasspathContainer();
        KieSession kieSession = kieClasspathContainer.newKieSession();
        kieSession.getAgenda().getAgendaGroup(em.getEmergencyType()).setFocus();
        kieSession.insert(em);
        kieSession.fireAllRules();
        kieSession.dispose();
    }
}
