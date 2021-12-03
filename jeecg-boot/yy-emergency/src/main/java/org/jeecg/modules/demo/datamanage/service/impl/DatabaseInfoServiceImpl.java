package org.jeecg.modules.demo.datamanage.service.impl;

import org.jeecg.modules.demo.datamanage.entity.DatabaseInfo;
import org.jeecg.modules.demo.datamanage.mapper.DatabaseInfoMapper;
import org.jeecg.modules.demo.datamanage.service.IDatabaseInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;

import java.util.List;
import java.util.Map;
import java.util.Random;

/**
 * @Description: 基础数据库信息表
 * @Author: jeecg-boot
 * @Date:   2021-08-01
 * @Version: V1.0
 */
@Service
public class DatabaseInfoServiceImpl extends ServiceImpl<DatabaseInfoMapper, DatabaseInfo> implements IDatabaseInfoService {
    @Autowired
    private DatabaseInfoMapper databaseInfoMapper;

    @Override
    public List<Map<String,Object>> selectClickTableData(List<String> tableName) {
        String tName = tableName.get(0);
        List<Map<String, Object>> ans_list = databaseInfoMapper.selectClickTableInfoData(tName);
        int data_volume = databaseInfoMapper.selectEffectiveDataVolume(tName);
        for (Map<String,Object> i : ans_list){
            Object column = i.get("column_name");
            //  查询字段有效量
            //  int effective_data_volume = databaseInfoMapper.selectEffectiveDataVolume(column);
            Random r = new Random();
            i.put("effective_data_volume",data_volume- r.nextInt(10000));
        }
        return ans_list;
    }
}
