package org.jeecg.modules.demo.utils;

import com.huaban.analysis.jieba.JiebaSegmenter;
import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.text.PDFTextStripperByArea;
import org.jeecg.modules.demo.emergencycompile.entity.Emergency;

import java.io.File;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class RegularEmergency {
    public static Emergency CompileEmergencyPushEntity(String file) throws Exception {
        PDDocument document = PDDocument.load(new File(file));
        Emergency em = new Emergency();
        String pdfFileInText;
        if (!document.isEncrypted()) {
            PDFTextStripperByArea stripper = new PDFTextStripperByArea();
            stripper.setSortByPosition(true);
            PDFTextStripper tStripper = new PDFTextStripper();

            pdfFileInText = tStripper.getText(document);
            em = judgeEmergency(pdfFileInText);
        }
        document.close();
        return em;
    }
    private static Emergency judgeEmergency(String text){
        Emergency em = new Emergency();
        JiebaSegmenter segmenter = new JiebaSegmenter();
        String regEx = "[\n\r\t`~!@#$%^&*()+=|{}':;',\\[\\]<>/?~！@#￥%……&*（）——+|{}【】‘；：”“’。， 、？^p]";
        String line = text.replaceAll(regEx, "").replaceAll("　", "").replaceAll(" ", "");
        List<String> strings = segmenter.sentenceProcess(line);
        if (em.getName() == null){
            Pattern p = Pattern.compile("(?<!\\s).+(?=\\n)");
            Matcher m = p.matcher(text);
            if (m.lookingAt()) em.setName(m.group().replace(" ",""));
        }
        if (em.getAddress() == null){
            Pattern p = Pattern.compile(".*?省|.*?市|.*?区|.*?镇|.*?村");
            Matcher m = p.matcher(text);
            StringBuilder add = new StringBuilder();
            while (m.find()) if (m.group().length()<5)add.append(m.group());
            em.setAddress(String.valueOf(add));
        }
        for (String i : strings){
            if (!em.isDeath() && i.equals("死亡"))em.setDeath(true);
            if (!em.isInjury() && i.equals("受伤"))em.setInjury(true);
            if (!em.isLoss() && i.equals("经济损失"))em.setInjury(true);
            if (em.getEmergencyType()==null && i.equals("事故"))em.setEmergencyType("事故灾难");
        }
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
                System.out.println(i);
                Pattern p2 = Pattern.compile("\\d");
                Matcher m2 = p2.matcher(i);
                while (m2.find()) em.setLossNum(Integer.parseInt(m2.group()));
            }
        }
        em.setContent(line);
        em.setTime(new Date());
        return em;
    }
}
