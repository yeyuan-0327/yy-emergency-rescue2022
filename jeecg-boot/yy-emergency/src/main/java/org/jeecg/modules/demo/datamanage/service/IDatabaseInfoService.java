package org.jeecg.modules.demo.datamanage.service;

import org.jeecg.modules.demo.datamanage.entity.DatabaseInfo;
import com.baomidou.mybatisplus.extension.service.IService;

import java.util.List;
import java.util.Map;

/**
 * @Description: 基础数据库信息表
 * @Author: jeecg-boot
 * @Date:   2021-08-01
 * @Version: V1.0
 */
public interface IDatabaseInfoService extends IService<DatabaseInfo> {
    List<Map<String,Object>> selectClickTableData(List<String> tableName);

    List<Map<String, Object>> selectCharGroupByField(List<String> fieldName);

    List<List<Object>> selectCharGroupByBirthField(List<String> fieldName);

    List<Map<String, Object>> selectCharGroupByAnyField(List<String> fieldTableName);
}
