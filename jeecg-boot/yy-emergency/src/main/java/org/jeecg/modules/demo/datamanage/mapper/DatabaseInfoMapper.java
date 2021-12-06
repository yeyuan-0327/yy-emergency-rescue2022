package org.jeecg.modules.demo.datamanage.mapper;

import java.util.List;
import java.util.Map;

import org.apache.ibatis.annotations.Param;
import org.jeecg.modules.demo.datamanage.entity.DatabaseInfo;
import com.baomidou.mybatisplus.core.mapper.BaseMapper;

/**
 * @Description: 基础数据库信息表
 * @Author: jeecg-boot
 * @Date:   2021-08-01
 * @Version: V1.0
 */
public interface DatabaseInfoMapper extends BaseMapper<DatabaseInfo> {

    List<Map<String,Object>> selectClickTableInfoData(@Param("tableName")String tableName);

    int selectEffectiveDataVolume(@Param("tableName")String tName);

    List<Map<String, Object>> selectCharGroupByField(@Param("fName")String fName);
}
