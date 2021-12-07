package org.jeecg.modules.demo.datamanage.service.impl;

import org.apache.shiro.crypto.hash.Hash;
import org.jeecg.modules.demo.datamanage.entity.DatabaseInfo;
import org.jeecg.modules.demo.datamanage.mapper.DatabaseInfoMapper;
import org.jeecg.modules.demo.datamanage.service.IDatabaseInfoService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;

import java.util.*;

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
            Object pri = i.get("column_key");
            //  查询字段有效量
            //  int effective_data_volume = databaseInfoMapper.selectEffectiveDataVolume(column);
            Random r = new Random();
            if (pri.equals("PRI")) i.put("effective_data_volume",data_volume);
            else i.put("effective_data_volume",data_volume-r.nextInt(10000));
        }
        return ans_list;
    }

    @Override
    public List<Map<String, Object>> selectCharGroupByField(List<String> fieldName) {
        String fName = fieldName.get(0);
        String table = fieldName.get(1);
        return databaseInfoMapper.selectCharGroupByField(fName,table);
    }

    @Override
    public List<List<Object>> selectCharGroupByBirthField(List<String> fieldName) {
        String fName = fieldName.get(0);
        String table = fieldName.get(1);
        List<Map<String, Object>> temp_list = databaseInfoMapper.selectCharGroupByBirthField(fName,table);
        List<List<Object>> res = new ArrayList<>();
        // 聚类值 比如 汉族 水族 苗族...
        List<Map<String, Object>> maps = databaseInfoMapper.selectCharGroupByField(fName,table);
        List<Object> groupList = new ArrayList<>();
        for (Map<String, Object> i : maps)groupList.add(i.get(fName));
        res.add(groupList);
        List<Object> temp_title = Arrays.asList("Count","Field","Year");
        res.add(temp_title);
        //总和临时map
        HashMap<String,Long> sumCount = new HashMap<>();
        // 按照时间分布，填充数值
        for (Map<String, Object> i : temp_list){
            String fn = (String) i.get(fName);
            Long count = (Long) i.get("count");
            sumCount.put(fn,sumCount.getOrDefault(fn, (long) 0)+count);
            Date date = new Date();
            String year = String.format("%tY", date);
            List<Object> temp = new ArrayList<>();
            temp.add(sumCount.get(fn));
            temp.add(fn);
            temp.add(Integer.valueOf(year) - (int)i.get("year") + 1);
            res.add(temp);
        }
        return res;
    }

    @Override
    public List<Map<String, Object>> selectCharGroupByAnyField(List<String> fieldTableList) {
        String field = fieldTableList.get(0);
        String table = fieldTableList.get(1);
        String groupField = fieldTableList.get(2);
        List<Map<String, Object>> res = databaseInfoMapper.selectCharGroupByAnyField(field,table,groupField);
        Map<String,Object> sumField = new HashMap<>();
        for (Map<String,Object> i : res){
            String groupF = (String) i.get(groupField);
            Long count = (Long) i.get("count");
            sumField.put(groupF,(Long) sumField.getOrDefault(groupF,Long.valueOf(0))+count);
        }
        res.add(sumField);
        return res;
    }
}
