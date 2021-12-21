package org.jeecg.modules.demo.utils;

import org.springframework.web.multipart.MultipartFile;

import java.io.File;

public class MultipartFileUtils {
    public static String saveFile(String rootPath, MultipartFile file) throws Exception {
        String savePath = rootPath + file.getOriginalFilename();
        File existsFile = new File(savePath);
        if (!existsFile.exists()){
            System.out.println("上传的文件：" + file.getName() + "," + file.getContentType() + "," + file.getOriginalFilename()
                    +"，保存的路径为：" + savePath);
            file.transferTo(new File(savePath));
        }
        return savePath;
    }
}
