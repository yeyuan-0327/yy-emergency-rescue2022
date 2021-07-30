package org.jeecg.modules.demo.datamange.entity;

import java.io.Serializable;
import java.io.UnsupportedEncodingException;
import java.util.Date;
import java.math.BigDecimal;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;
import lombok.Data;
import com.fasterxml.jackson.annotation.JsonFormat;
import org.springframework.format.annotation.DateTimeFormat;
import org.jeecgframework.poi.excel.annotation.Excel;
import org.jeecg.common.aspect.annotation.Dict;
import io.swagger.annotations.ApiModel;
import io.swagger.annotations.ApiModelProperty;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;

/**
 * @Description: 基础数据库信息表
 * @Author: jeecg-boot
 * @Date:   2021-07-30
 * @Version: V1.0
 */
@Data
@TableName("database_info")
@Accessors(chain = true)
@EqualsAndHashCode(callSuper = false)
@ApiModel(value="database_info对象", description="基础数据库信息表")
public class DatabaseInfo implements Serializable {
    private static final long serialVersionUID = 1L;

	/**主键*/
	@TableId(type = IdType.ASSIGN_ID)
    @ApiModelProperty(value = "主键")
    private java.lang.String id;
	/**表名*/
	@Excel(name = "表名", width = 15)
    @ApiModelProperty(value = "表名")
    private java.lang.String name;
	/**中文名*/
	@Excel(name = "中文名", width = 15)
    @ApiModelProperty(value = "中文名")
    private java.lang.String chineseName;
	/**数据库类型*/
	@Excel(name = "数据库类型", width = 15, dicCode = "database_project")
	@Dict(dicCode = "database_project")
    @ApiModelProperty(value = "数据库类型")
    private java.lang.String databaseProject;
	/**描述信息*/
	@Excel(name = "描述信息", width = 15)
    @ApiModelProperty(value = "描述信息")
    private java.lang.String content;
	/**创建日期*/
	@JsonFormat(timezone = "GMT+8",pattern = "yyyy-MM-dd HH:mm:ss")
    @DateTimeFormat(pattern="yyyy-MM-dd HH:mm:ss")
    @ApiModelProperty(value = "创建日期")
    private java.util.Date createTime;
}
