package org.jeecg.modules.demo.datamanage.mapper;

import java.util.List;
import java.util.Map;

import com.baomidou.dynamic.datasource.annotation.DS;
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

    List<Map<String, Object>> selectCharGroupByField(@Param("fName")String fName,
                                                     @Param("table")String table);

    List<Map<String, Object>> selectCharGroupByBirthField(@Param("fName")String fName,
                                                          @Param("table")String table);

    List<Map<String, Object>> selectCharGroupByAnyField(@Param("field")String field,
                                                        @Param("table")String table,
                                                        @Param("groupField")String groupField);

    List<Map<String, Object>> fetchDimFactRelationPointFact();

    List<Map<String, Object>> fetchDimFactRelationPointDim();

    List<Map<String, Object>> fetchDimFactRelationLink();

    @DS("dw-gp")
    List<Map<String, Object>> fetchDwDataColumn(@Param("table")String table_name);

    @DS("dw-gp")
    List<Map<String, Object>> fetchDwData(@Param("table")String table_name);

    @DS("dw-gp")
    List<Map<String, Object>> factDataTable(@Param("field")String field,
                                            @Param("table")String table_name);
}
